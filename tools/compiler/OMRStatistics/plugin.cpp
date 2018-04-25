/*******************************************************************************
 *
 * (c) Copyright IBM Corp. 2000, 2016
 *
 *  This program and the accompanying materials are made available
 *  under the terms of the Eclipse Public License v1.0 and
 *  Apache License v2.0 which accompanies this distribution.
 *
 *      The Eclipse Public License is available at
 *      http://www.eclipse.org/legal/epl-v10.html
 *
 *      The Apache License v2.0 is available at
 *      http://www.opensource.org/licenses/apache2.0.php
 *
 * Contributors:
 *    Multiple authors (IBM Corp.) - initial implementation and documentation
 *******************************************************************************/


#ifndef OMRSTATISTICS_HPP
#define OMRSTATISTICS_HPP

#include "llvm/Config/llvm-config.h"

#include "clang/Basic/SourceManager.h"
#include "clang/Basic/SourceLocation.h"
#include "clang/Frontend/FrontendPluginRegistry.h"
#include "clang/AST/AST.h"
#include "clang/AST/ASTConsumer.h"
#include "clang/AST/ASTTypeTraits.h"
#include "clang/AST/RecursiveASTVisitor.h"
#include "clang/AST/Attr.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Analysis/CallGraph.h"
#include "llvm/Support/raw_ostream.h"
#include "clang/Lex/Lexer.h"

#include "plugin.hpp"
#include <sstream>

OMRStatistics::FunctionDeclInfo::FunctionDeclInfo(bool isImplicit, bool isVirtual, std::string location) {
	this->isImplicit = isImplicit;
	this->isVirtual = isVirtual;
	this->location = location;
}

std::map<std::string, std::unordered_set<std::string*>> OMRStatistics::HMRecorder::getClass2Methods() {
	return class2Methods;
	}

void OMRStatistics::HMRecorder::setClass2Methods(std::map<std::string, std::unordered_set<std::string*>> class2Methods) {
	this->class2Methods = class2Methods;
	}

std::map<std::string, std::vector<std::string>*> OMRStatistics::HMRecorder::getClassHierarchy() {return classHierarchy;}

void OMRStatistics::HMRecorder::setClassHierarchy(std::map<std::string, std::vector<std::string>*> classHierarchy) {
	this->classHierarchy = classHierarchy;
}

std::map<std::string, OMRStatistics::FunctionDeclInfo*> OMRStatistics::HMRecorder::getFunctionDeclInfo() {
	return functionDeclInfo;
}

void OMRStatistics::HMRecorder::setFunctionDeclInfo(std::map<std::string, FunctionDeclInfo*>) {
	this->functionDeclInfo = functionDeclInfo;
}

std::map<std::string, bool> OMRStatistics::HMRecorder::getIsExtensible() {
	return isExtensible;
}

void OMRStatistics::HMRecorder::setIsExtensible(std::map<std::string, bool> isExtensible) {
	this->isExtensible = isExtensible;
	}

std::vector<OMRStatistics::FunctionCall*> OMRStatistics::HMRecorder::getFunctionCalls() {
	return functionCalls;
}

void OMRStatistics::HMRecorder::setFunctionCalls(std::vector<FunctionCall*> calls) {
	functionCalls = calls;
}

bool OMRStatistics::HMRecorder::checkExtensibility(const CXXRecordDecl* declIn) {
	const CXXRecordDecl* decl = declIn;
  
	for (Decl::attr_iterator A = decl->attr_begin(), E = decl->attr_end(); A != E; ++A) {
		if (isa<AnnotateAttr>(*A)) {
			AnnotateAttr *annotation = dyn_cast<AnnotateAttr>(*A);
			if (annotation->getAnnotation() == "OMR_Extensible") return true;
		}
	}
  
  return false;
}

std::string OMRStatistics::HMRecorder::getFuncSig(CXXMethodDecl* currentDecl) {
	std::string funcSig = currentDecl->getNameAsString();
	ArrayRef<clang::ParmVarDecl*> functions = currentDecl->parameters();
	if(functions.size() == 0) funcSig += "()";
	else {
		funcSig += "(";
		for(clang::ParmVarDecl* param : functions) {
			funcSig += param->getOriginalType().getAsString() + ",";
		}
		funcSig.replace(funcSig.end()-1, funcSig.end(), "");
		funcSig += ")";
	}
	return funcSig;
}

void OMRStatistics::HMRecorder::handleFailedAssert(std::string className, std::string funcSig, std::pair<std::map<std::string, FunctionDeclInfo*>::iterator, bool> result, std::string loc) {
	//If assert fails: (There are more than 2 declarations of a unique function)
		llvm::outs() << className << "::" << funcSig << "\n";
		llvm::outs() << "\tExisting Location: " << result.first->second->location << "\n";
		llvm::outs() << "\tNew Location: " << loc << "\n";
}

void OMRStatistics::HMRecorder::assertFuncDeclNb(std::string className, std::string funcSig, std::pair<std::map<std::string, FunctionDeclInfo*>::iterator, bool> searchItr, CXXMethodDecl* currentDecl) {
	if(!searchItr.second) {
		std::string loc = printLoc(currentDecl);
		size_t colonIndexOld = searchItr.first->second->location.find(':');
		size_t colonIndexNew = loc.find(':');
		std::string oldLoc = searchItr.first->second->location.substr(0, colonIndexOld);
		std::string newLoc = loc.substr(0, colonIndexNew);
		
		if (oldLoc.compare(newLoc) != 0) {
			std::string extensionOld = oldLoc.substr(oldLoc.size() - 3, 3);
			std::string extensionNew = newLoc.substr(newLoc.size() - 3, 3);
			bool oldIsHPP = extensionOld.compare("hpp") == 0;
			bool oldIsCPP = extensionOld.compare("cpp") == 0;
			bool newIsHPP = extensionNew.compare("hpp") == 0;
			bool newIsCPP = extensionNew.compare("cpp") == 0;
			assert((oldIsHPP && newIsCPP) || (oldIsCPP && newIsHPP));
			//handleFailedAssert(className, funcSig, searchItr, loc);
			if(oldIsCPP && newIsHPP) searchItr.first->second->location = loc;
		}
	}
}

void OMRStatistics::HMRecorder::processCallExpressions(CXXMethodDecl* currentDecl) {
	if(currentDecl->hasBody()) {
		std::string caller = currentDecl->getQualifiedNameAsString();
		CompoundStmt* stmt = (CompoundStmt*) (currentDecl->getBody());
		Stmt** bodyItr = stmt->body_begin();
		for(unsigned i = 0; i < stmt->size(); i++) { //iterate all statements in the function body
			Stmt* currentStmt = bodyItr[i];
			std::string stmtType = currentStmt->getStmtClassName();
			if(stmtType.compare("CXXMemberCallExpr") == 0) {
				//Get location of currentStmt, which is the call location
				CXXMemberCallExpr* callExpr = (CXXMemberCallExpr*) currentStmt;
				std::string receiver = callExpr->getMethodDecl()->getQualifiedNameAsString();
				
				FunctionCall* call = new FunctionCall(currentDecl, callExpr->getMethodDecl());
				functionCalls.emplace_back(call);
			}
		}
	}
}

void OMRStatistics::HMRecorder::recordFunctions(const CXXRecordDecl* inputClass) {
	std::string className = inputClass->getQualifiedNameAsString();
	if(HMConsumer::shouldIgnoreClassName(className)) return;
	//Iterate through every method in the class
	for(auto A = inputClass->method_begin(), E = inputClass->method_end(); A != E; ++A) {
		CXXMethodDecl* currentDecl = *A;
		//Get function name with parameter types (AKA: recreate function signature)
		std::string* funcSig = new std::string(HMRecorder::getFuncSig(currentDecl));
		
		//Save function information
		FunctionDeclInfo* info = new FunctionDeclInfo(currentDecl->isImplicit(), currentDecl->isVirtual(), printLoc(currentDecl));
		//Assert only one decl of the func is found
		auto result = functionDeclInfo.emplace(className + "::" + *funcSig, info);
		assertFuncDeclNb(className, *funcSig, result, currentDecl);
		
		auto iterator = class2Methods.find(className);
		if(iterator != class2Methods.end()) { //If the class was already encountered before, pull methods vector from class2Methods
			std::unordered_set<std::string*>* methods = &(iterator->second);
			methods->insert(funcSig);
		}
		else { //If the class is new
			std::unordered_set<std::string*> methods;
			methods.insert(funcSig);
			class2Methods.emplace(className, methods);
		}
		
		//Check for function calls
		processCallExpressions(currentDecl);
	}
}

std::string OMRStatistics::HMRecorder::printLoc(const clang::CXXRecordDecl* d) {
	std::string result;
	result = d->getLocStart().printToString(d->getASTContext().getSourceManager());
	return result;
}

std::string OMRStatistics::HMRecorder::printLoc(const CXXMethodDecl* d) {
	std::string result;
	result = d->getLocStart().printToString(d->getASTContext().getSourceManager());
	return result;
}

std::string OMRStatistics::HMRecorder::printLoc(clang::CXXMethodDecl* d) {
	std::string result;
	result = d->getLocStart().printToString(d->getASTContext().getSourceManager());
	return result;
}

size_t OMRStatistics::HMRecorder::findLastStringIn(std::string input, char key) {
	size_t pos = input.size();
	for(size_t i = 0; i < input.size(); i++) {
		char c = input.at(i);
		if(c == key) pos = i - 1;
	}
	
	assert((pos != input.size()) && "No key in input");
	return pos;
}

void OMRStatistics::HMRecorder::addNeglectedClasses() {
	for (auto itr : isExtensible)
		if (classesAddedToHierarchy.find(itr.first) == classesAddedToHierarchy.end())
			// This is an ignored class since its found in the isExtensible keyset but not in classesAddedToHierarchy
			recordParents(itr.first,"");
}

bool OMRStatistics::HMRecorder::recordParents(std::string childClassName, std::string parentClassName) {
	if(parentClassName.compare(childClassName) != 0) {
		auto itr = classHierarchy.find(childClassName);
		auto end = classHierarchy.end();
		
		std::vector<std::string>* parents;
		
		if(itr == end) {//classHierarchy does not have the current class, add it to classHierarchy
			parents = new std::vector<std::string>();
			classHierarchy.emplace(childClassName, parents);
		}
		
		else {
			parents = itr->second;
			//Check if parent is already recorded (redeclarations in source code)
			auto b = parents->begin();
			auto e = parents->end();
			if(std::find(b, e, parentClassName) != e) return false;
		}
		
		parents->push_back(parentClassName);
			
		return true;
	}
	
	return false;
}

void OMRStatistics::HMRecorder::recordParents(const CXXRecordDecl *decl) {
	if(!decl) return;
	std::string currentClassName = decl->getQualifiedNameAsString();
	if(HMConsumer::shouldIgnoreClassName(currentClassName)) return;
	
	//Record extensibility of the declaration
	bool currentIsExtensible =  checkExtensibility(decl);
	if(isExtensible.find(currentClassName) == isExtensible.end()) 
		isExtensible.emplace(currentClassName, currentIsExtensible);
	else if(isExtensible[currentClassName] == false) 
		isExtensible[currentClassName] = currentIsExtensible;
	
	CXXRecordDecl::base_class_const_iterator BI, BE, BC;
	
	BI = decl->bases_begin();
	BE = decl->bases_end();
	int parentCounter = 0;
	for(BC = BI; BC != BE; BC++) { //iterate through all parents
		clang::QualType parentClassType = BC->getType();
		CXXRecordDecl* parentDecl = parentClassType->getAsCXXRecordDecl();
		
		std::string parentClassName = (parentDecl) ? parentDecl->getQualifiedNameAsString() : parentClassType.getAsString(); //Prioritize having the name of the CXX record over general QualTypes
		if(!parentDecl) continue;
		
		if(HMConsumer::shouldIgnoreClassName(parentClassName)) continue;
		parentCounter++;
		recordParents(currentClassName, parentClassName);
		classesAddedToHierarchy.emplace(currentClassName);
		classesAddedToHierarchy.emplace(parentClassName);
		if(parentDecl) recordParents(parentDecl);
		//TODO: recursively call this function on all classes, even if the class not a CXXDecl (even if it is a template)
	}
}

bool OMRStatistics::HMRecorder::VisitCXXRecordDecl(const CXXRecordDecl *decl) {
	if(!decl || !decl->isClass() || !decl->hasDefinition()) return true;
	recordFunctions(decl);
	recordParents(decl);
	
	return true;
}

OMRStatistics::LinkedNode::LinkedNode(std::string name) {
	this->parents = new std::vector<LinkedNode*>();
	this->name = name;
}

bool OMRStatistics::Hierarchy::operator==(const Hierarchy& other) {
	return (base->name.compare(other.base->name) == 0);
}

bool OMRStatistics::Hierarchy::operator==(const std::string other) {
	return (base->name.compare(other) == 0);
}

bool OMRStatistics::Hierarchy::operator!=(const Hierarchy& other) {
	return !(*this == other);
}

bool OMRStatistics::Hierarchy::operator!=(const std::string other) {
	return !(*this == other);
}

//Tracks the occurrences of each method, what classes, when overridden, and when overloaded
OMRStatistics::MethodTracker::MethodTracker(std::string className, std::string methodSignature, bool firstOccurence, bool isImplicit, bool isVirtual) {
	methodName = HMConsumer::getFuncName(methodSignature);
	this->methodSignature = methodSignature;
	nbOfOccurences = 1;
	classesOverriden = new std::vector<std::string>();
	this->firstOccurence = firstOccurence;
	baseClassName = className;
	this->isImplicit = isImplicit;
	this->isVirtual = isVirtual;
}

void OMRStatistics::MethodTracker::addOccurence(std::string className) {
	nbOfOccurences++;
	classesOverriden->push_back(className);
}


bool OMRStatistics::MethodTracker::operator==(const MethodTracker& other) {
	return (methodSignature.compare(other.methodSignature) == 0);
}

bool OMRStatistics::MethodTracker::operator==(const std::string other) {
	return (methodSignature.compare(other) == 0);
}

OMRStatistics::FunctionCall::FunctionCall(CXXMethodDecl* caller, CXXMethodDecl* receiver) {
	this->receiverDecl = receiver;
	this->callerDecl = caller;
}

void OMRStatistics::FunctionCall::setCallee(CXXMethodDecl* cd) {
	this->receiverDecl = cd;
}

CXXMethodDecl* OMRStatistics::FunctionCall::getCallee() {
	return this->receiverDecl;
}

void OMRStatistics::FunctionCall::setCaller(CXXMethodDecl* cd) {
	this->callerDecl = cd;
}

CXXMethodDecl* OMRStatistics::FunctionCall::getCaller() {
	return this->callerDecl;
}

std::string OMRStatistics::FunctionCall::receiverClass() {
	return receiverDecl->getParent()->getQualifiedNameAsString();
}

std::string OMRStatistics::FunctionCall::callerClass() {
	return callerDecl->getParent()->getQualifiedNameAsString();
}

std::string OMRStatistics::FunctionCall::receiverFuncQualSig() {
	return receiverClass() + "::" + receiverFuncSig();
}

std::string OMRStatistics::FunctionCall::callerFuncQualSig() {
	return callerClass() + "::" + callerFuncSig();
}

std::string OMRStatistics::FunctionCall::receiverFuncSig() {
	return HMRecorder::getFuncSig(receiverDecl);
}

std::string OMRStatistics::FunctionCall::callerFuncSig() {
	return HMRecorder::getFuncSig(callerDecl);
}

std::string OMRStatistics::FunctionCall::receiverLoc(ASTContext& Context) {
	SourceManager &manager = Context.getSourceManager();
	return receiverDecl->getSourceRange().getBegin().printToString(manager);
}

std::string OMRStatistics::FunctionCall::callerLoc(ASTContext& Context) {
	SourceManager &manager = Context.getSourceManager();
	return callerDecl->getSourceRange().getBegin().printToString(manager);
}

OMRStatistics::HMConsumer::HMConsumer(llvm::StringRef filename, Config conf) {
	this->conf = conf;
}

OMRStatistics::Hierarchy* OMRStatistics::HMConsumer::modifyBase(LinkedNode* oldBase, LinkedNode* newBase) {
	for (auto hierarchy : hierarchies) 
		if(hierarchy->base == oldBase) {
			hierarchy->base = newBase;
			return hierarchy;
		}
	return nullptr;
}

void OMRStatistics::HMConsumer::deleteHierarchy(LinkedNode* base) {
	
	// Search for hierarchy to delete
	auto itr = hierarchies.begin();
	auto end = hierarchies.end();
	
	while (itr != end) {
		auto hierarchy = *itr;
		if(hierarchy->base == base) {
			hierarchies.erase(itr);
			delete hierarchy;
			return;
		}
		itr++;
	}
}

bool OMRStatistics::HMConsumer::isBase(std::string className) {
	for(Hierarchy* hierarchy : hierarchies)
		if(hierarchy->base->name.compare(className) == 0) 
			return true;
	return false;
}

void OMRStatistics::HMConsumer::addSingleClass(std::string className, std::vector<Hierarchy*> &hierarchies) {
	Hierarchy* newHierarchy = new Hierarchy();
	newHierarchy->isSingle = true;
	hierarchies.push_back(newHierarchy);
	LinkedNode* childNode = new LinkedNode(className);
	newHierarchy->base = childNode;
	class2Address.emplace(childNode->name, childNode);
}

void OMRStatistics::HMConsumer::fillHierarchies(std::map<std::string, std::vector<std::string>*> &map) {
	for(auto current : map) {
		std::string childName = current.first;
		std::vector<std::string>* parents = current.second;
		
		//For classes with no parents or children, create a new hierarchy with only this class
		if(parents->at(0).compare("") == 0) {
			addSingleClass(childName, hierarchies);
		}
		else {
			for(std::string parentName : *parents) {
				auto childItr = class2Address.find(childName);
				auto parentItr = class2Address.find(parentName);
				auto end = class2Address.end();
				
				if(childItr != end && parentItr != end) { // If both child and parent nodes are found in hierarchy list
					LinkedNode* childNode = childItr->second;
					LinkedNode* parentNode = parentItr->second;
					if(isBase(parentName)) { //parent has no children
						childNode->parents->push_back(parentNode);
						deleteHierarchy(parentNode);
					}
					else //if parent has children
						childNode->parents->push_back(parentNode);
				}
				else if(childItr != end) { // If child node is found in hierarchy list
					LinkedNode* childNode = childItr->second;
					LinkedNode* parentNode = new LinkedNode(parentName);
					class2Address.emplace(parentNode->name, parentNode);
					childNode->parents->push_back(parentNode);
				}
				
				else if(parentItr != end) { // If parent node is found in hierarchy list
					LinkedNode* parentNode = parentItr->second;
					LinkedNode* childNode = new LinkedNode(childName);
					class2Address.emplace(childNode->name, childNode);
					childNode->parents->push_back(parentNode);
					if(isBase(parentName)) 
						modifyBase(parentNode, childNode);
					else { // parent has one or more children
						Hierarchy* newHierarchy = new Hierarchy();
						newHierarchy->base = childNode;
						hierarchies.push_back(newHierarchy);
					}
				}
				
				//If both nodes not found in hierarchy list
				else /*if(childItr == end && parentItr == end)*/ {
					Hierarchy* newHierarchy = new Hierarchy();
					hierarchies.push_back(newHierarchy);
					LinkedNode* childNode = new LinkedNode(childName);
					LinkedNode* parentNode = new LinkedNode(parentName);
					childNode->parents->push_back(parentNode);
					newHierarchy->base = childNode;
					class2Address.emplace(parentNode->name, parentNode);
					class2Address.emplace(childNode->name, childNode);
				}
			}
		}
	}
}

OMRStatistics::MethodTracker* OMRStatistics::HMConsumer::searchForTracker(std::map<std::string, std::vector<MethodTracker>*>* methodName2MethodTracker, std::string method, bool* sameName) {
	std::string methodName = getFuncName(method);
	//Search for method trackers with same name
	auto e1 = methodName2MethodTracker->end();
	auto itr1 = methodName2MethodTracker->find(methodName);
	if (itr1 != e1) {
		*sameName = true;
		//Search for the method tracker with the same signature
		std::vector<MethodTracker>* trackersMatchingName = itr1->second;
		auto b2 = trackersMatchingName->begin();
		auto e2 = trackersMatchingName->end();
		auto itr2 = std::find(b2, e2, method);
		if (itr2 != e2) {
			MethodTracker* t = trackersMatchingName->data() + (itr2-b2); //Change the iterator to the actual pointer to the target MethodTracker
			
			return t; 
		}
	}
	
	return nullptr;
}

std::string OMRStatistics::HMConsumer::getFuncName(std::string methodSignature) {
	//Get method name from signature
	std::size_t pos = methodSignature.find("(");
	assert(pos != std::string::npos && "method name is invalid");
	return methodSignature.substr(0, pos);
}

void OMRStatistics::HMConsumer::collectMethodInfo(HMRecorder &recorder) {
	auto map = recorder.getClass2Methods();
	std::map<std::string, FunctionDeclInfo*> functionDeclInfo = recorder.getFunctionDeclInfo();
	
	for(auto hierarchy : hierarchies) {
		//iterate hierarchy from top to base
		std::vector<std::vector<LinkedNode*>*>* subHierarchies = getTopToBaseAsArray(hierarchy);	
		assert(subHierarchies && subHierarchies->size() > 0 && "Passed an empty hierarchy to getTopToBaseAsArray");
		
		//Iterate through each subHierarchy's classes
		for(std::vector<LinkedNode*>* subHierarchy : *subHierarchies) {
			//Create new methodTracker for subHierarchy
			auto methodName2MethodTracker = new std::map<std::string, std::vector<MethodTracker>*>();
			hierarchy->methodName2MethodTrackerVec.push_back(methodName2MethodTracker);
			
			//Process each method in every class of the subHierarchy
			for(LinkedNode* current : *subHierarchy) {
				std::string className = current->name;
				//llvm::outs() << className << ":\n";
				auto itr = map.find(className);
				if(itr == map.end()) continue;
				std::unordered_set<std::string*> methods = itr->second;
				for(std::string* methodPtr : methods) {
					std::string method = *methodPtr;
					//llvm::outs() << "\t" << method << "\n";
					bool sameName = false;
					MethodTracker* tracker = searchForTracker(methodName2MethodTracker, method, &sameName);
					if(tracker) //This is an override
						tracker->addOccurence(className);
					else {
						std::string methodName = getFuncName(method);
						bool isFirstOccurence = true;
						std::vector<MethodTracker>* trackers;
						if(sameName) { //This is an overload
							isFirstOccurence = false;
							trackers = methodName2MethodTracker->find(methodName)->second;
						}
						else { //This is a completely new functions
							trackers = new std::vector<MethodTracker>();
							methodName2MethodTracker->emplace(methodName, trackers);
						}
						MethodTracker newTracker(className, method, isFirstOccurence, functionDeclInfo[className + "::" + method]->isImplicit, functionDeclInfo[className + "::" + method]->isVirtual);
						trackers->emplace_back(newTracker);
					}
				}
			}
		}
	}
}

std::vector<std::vector<OMRStatistics::LinkedNode*>*>* OMRStatistics::HMConsumer::getTopToBaseAsArray(OMRStatistics::Hierarchy* hierarchy) {
	std::vector<LinkedNode*>* array = new std::vector<LinkedNode*>();
	std::vector<std::vector<LinkedNode*>*>* subHierarchies = new std::vector<std::vector<LinkedNode*>*>;
	getTopToBaseAsArray(hierarchy->base, array, subHierarchies);
	
	for(std::vector<LinkedNode*>* subHierarchy : *subHierarchies) {
		//Switch nodes in each subHierarchy
		int switch2 = subHierarchy->size() - 1;
		for(unsigned long switch1 = 0; switch1 < subHierarchy->size()/2; switch1++) {
			LinkedNode* temp = subHierarchy->at(switch1);
			subHierarchy->at(switch1) = subHierarchy->at(switch2);
			subHierarchy->at(switch2) = temp;
			switch2--;
		}
	}
	delete array;
	return subHierarchies;
}

void OMRStatistics::HMConsumer::getTopToBaseAsArray(LinkedNode* node, std::vector<OMRStatistics::LinkedNode*>* array, std::vector<std::vector<LinkedNode*>*>* subHierarchies) {
	array->push_back(node);
	if(node->parents->size() == 0) { //This node is a top of a base hierarchy
		auto arrayCpy = new std::vector<LinkedNode*>();
		for(LinkedNode* n : *array) arrayCpy->push_back(n); //Make a permanent copy of array
		subHierarchies->push_back(arrayCpy);
		array->pop_back();
		return;
	}
	for(LinkedNode* parent : *node->parents) 
		getTopToBaseAsArray(parent, array, subHierarchies);
	array->pop_back();
	return;
}

bool OMRStatistics::HMConsumer::shouldIgnoreClassName(std::string className) {
	if(className.find("std::") != std::string::npos) return true;
	if(className.find("__gnu_cxx::") != std::string::npos) return true;
	return false;
}

std::vector<std::string>* OMRStatistics::HMConsumer::seperateClassNameSpace(std::string input) {
	std::string nameSpace = "";
	std::string className = "";
	if(input.find("::") != std::string::npos) {
		size_t pos = findLastStringIn(input, "::");
		nameSpace = input.substr(0, pos);
		int classNameSize = input.length() - pos - 2;
		className = input.substr(pos+2, classNameSize);
	}
	else className = input;
	std::vector<std::string>* tuple = new std::vector<std::string>();
	tuple->push_back(nameSpace);
	tuple->push_back(className);
	return tuple;
}

size_t OMRStatistics::HMConsumer::findLastStringIn(std::string input, std::string key) {
	if(key.size() != 2) return -1; //This function only support keys of length 2
	if(input.size() < 2) return -1;
	
	size_t pos = input.size();
	char previous = input.at(0);
	for(size_t i = 1; i < input.size(); i++) {
		char c = input.at(i);
		if(previous == key.at(0) && c == key.at(1)) pos = i - 1;
		previous = c;
	}
	
	assert((pos != input.size()) && "No key in input");
	return pos;
}

std::vector<OMRStatistics::FunctionCall*>* OMRStatistics::HMConsumer::getFunctionCalls(ASTContext& Context) {
	//This function is inspired from the the following github project: https://github.com/maximesong/program-analysis
	//More specifically the following code block: https://github.com/maximesong/program-analysis/blob/b1d228e0fd0abb196939a0503c6326dc4ebbf692/src/consumers.cpp#L74-L108
	CallGraph cg;
	cg.addToCallGraph(Context.getTranslationUnitDecl());
	std::vector<FunctionCall*>* callerCalleeMap = new std::vector<FunctionCall*>();
	
	/*for (auto itr : cg) {
		//itr type:
		//	llvm::detail::DenseMapPair<const clang::Decl *, clang::CallGraphNode *>
		if(itr.first == NULL) {
			//clang::CallGraphNode* callerNode = itr.second;
			//callerNode->dump();
			continue;
		}
		clang::CallGraphNode* callerNode = itr.second;
		FunctionDecl* callerDecl = cast<FunctionDecl> (callerNode->getDecl());
		std::string callerClass = callerDecl->getQualifiedNameAsString();
		llvm::outs() << "Caller: " << callerClass << "\n";
		for(CallGraphNode* calleeNode : *callerNode) {
			FunctionDecl* receiverDecl = cast<FunctionDecl> (calleeNode->getDecl());
			std::string receiverClass = receiverDecl->getQualifiedNameAsString();
			llvm::outs() << "\tCallee: " << receiverClass << "\n";
			FunctionCall* fi = new FunctionCall(receiverDecl, callerDecl);
			callerCalleeMap->push_back(fi);
		}
		
	}*/
	llvm::outs() << "--------------------\n";
	return callerCalleeMap;
}

void OMRStatistics::HMConsumer::printTracker(llvm::raw_ostream* out, std::string methodName, std::string methodSig, std::string nameSpace, std::string className, bool isImplicit, bool isVirtual) {
	*out << methodName << ";";
	*out << methodSig << ";";
	*out << nameSpace << ";"; 
	*out << className << ";";
	*out << isImplicit << ";";
	*out << isVirtual << "\n";
}

void OMRStatistics::HMConsumer::printTracker(llvm::raw_ostream* out, OMRStatistics::MethodTracker &tracker) {
	if(!shouldIgnoreClassName(tracker.baseClassName)) {
		std::vector<std::string>* baseClass = seperateClassNameSpace(tracker.baseClassName);
		printTracker(out, tracker.methodName, tracker.methodSignature, baseClass->at(0), baseClass->at(1), tracker.isImplicit, tracker.isVirtual);
		for(std::string classOccurrenceQualName : *tracker.classesOverriden) {
			std::vector<std::string>* classOccurrence = seperateClassNameSpace(classOccurrenceQualName);
			printTracker(out, tracker.methodName, tracker.methodSignature, classOccurrence->at(0), classOccurrence->at(1), tracker.isImplicit, tracker.isVirtual);
		}
	}
}

void OMRStatistics::HMConsumer::printAllFunctions(llvm::raw_ostream* out) {
	*out << "FunctionName; FunctionSignature; Namespace; ClassName; isImplicit; isVirtual\n";
	for(auto hierarchy : hierarchies) {
		auto trackerMapVec = hierarchy->methodName2MethodTrackerVec;
		for(auto trackerMap : trackerMapVec) { //Go through the map of each subHierarchy
			//Iterate the subHierarchy map to go through all trackers
			auto b = trackerMap->begin();
			auto e = trackerMap->end();
			auto itr = b;
			while(itr != e) {
				auto hierarchyTrackers = *(itr->second);
				//Go through each tracker (signature) for a specific method name and report the overloads
				for(auto tracker : hierarchyTrackers) {
					printTracker(out, tracker);
				}
				itr++;
			}
		}
	}
}

void OMRStatistics::HMConsumer::printOverrides(llvm::raw_ostream* out) {
	*out << "BaseNamespace; BaseClassName; FunctionSignature; OverridingNamespace; OverridingClassName; isImplicit; isVirtual\n";
	for(Hierarchy* hierarchy : hierarchies) {
		std::vector<std::map<std::string, std::vector<MethodTracker>*>*> trackerMapVec = hierarchy->methodName2MethodTrackerVec;
		for(std::map<std::string, std::vector<MethodTracker>*>* trackerMap : trackerMapVec) {
			//Iterate each subHierarchy map to go through all trackers
			auto b = trackerMap->begin();
			auto e = trackerMap->end();
			auto itr = b;
			while(itr != e) {
				std::vector<MethodTracker>* hierarchyTrackers = itr->second;
				for(MethodTracker tracker : *hierarchyTrackers) { //The code in this block will be accessed by every tracker
					std::string baseClassName = tracker.baseClassName;
					for(std::string className : *tracker.classesOverriden) {
						std::vector<std::string>* baseClassNameTuple = seperateClassNameSpace(baseClassName);
						std::vector<std::string>* classNameTuple = seperateClassNameSpace(className);
						if(!shouldIgnoreClassName(baseClassName) || !shouldIgnoreClassName(className)) {
							*out << baseClassNameTuple->at(0) << ";"; //namespace
							*out << baseClassNameTuple->at(1) << ";";//className
							*out << tracker.methodSignature << ";";
							*out << classNameTuple->at(0) << ";"; //namespace
							*out << classNameTuple->at(1) << ";";//className
							*out << tracker.isImplicit << ";";
							*out << tracker.isVirtual << "\n";
						}
						baseClassName = className;
					}
				}
				itr++;
			}
		}
	}
}

void OMRStatistics::HMConsumer::printAverageOverrides(HMRecorder& recorder, llvm::raw_ostream* out) {
	auto isExtensible = recorder.getIsExtensible();
	float averagePercentage = 0;
	int counter = 0;
	for(Hierarchy* h : hierarchies) {
		
		//Only count extensible hierarchies
		std::string baseName = h->base->name;
		if(!isExtensible[baseName]) continue;
		
		auto maps = h->methodName2MethodTrackerVec;
		for(auto map : maps) { //iterating through sub-hierarchies
			int functionCounter = 0;
			int overrideCounter = 0;
			for(auto itr : *map) { //iterating through different function names
				std::string methodName = itr.first;
				for(MethodTracker tracker : *itr.second) { //iterating through methodTrackers of one method name
					functionCounter++;
					if(tracker.nbOfOccurences > 1) overrideCounter++;
				}
			}
			
			float percentage = (float)overrideCounter/(float)functionCounter * 100;
			
			averagePercentage += percentage;
			counter++;
		}
	}
	float avg = averagePercentage/counter;
	std::string avgStr = std::to_string(avg);
	*out << avgStr << "\n";
}

void OMRStatistics::HMConsumer::printFunctionLocations(HMRecorder& recorder, llvm::raw_ostream* out) {
	*out << "FunctionQualifiedName; Location;\n";
	std::map<std::string, FunctionDeclInfo*> functionDeclInfo = recorder.getFunctionDeclInfo();
	for(auto itr : functionDeclInfo) {
		*out << itr.first << ";" << itr.second->location << "\n";
	}
}

void OMRStatistics::HMConsumer::printHierarchies(HMRecorder& recorder, llvm::raw_ostream* out) {
	*out << "isExtensible; Hierarchy\n";
	for(Hierarchy* h : hierarchies) {
		if(h->isSingle) {
			continue;
		}
		std::string isExtensible = (recorder.getIsExtensible()[h->base->name]) ? "1;" : "0;";
		printHierarchy(isExtensible, h->base, out);
	}
}

void OMRStatistics::HMConsumer::printHierarchy(std::string history, LinkedNode* node, llvm::raw_ostream* out) {
	if(node->name.compare("") == 0) {
		//llvm::outs() << "Empty string\n\t" << history << "\n";
	}
	history += node->name + " --> ";
	std::vector<LinkedNode*>* parents = node->parents;
	for(LinkedNode* parent : *parents) {
		printHierarchy(history, parent, out);
	}
	if(parents->size() == 0) *out << history.substr(0, history.size() - 5) << "\n";
}

void OMRStatistics::HMConsumer::printWeirdHierarchies(HMRecorder& recorder, llvm::raw_ostream* out) {
	*out << "childClassName(isExtensible) --> parentClassName(isExtensible)\n";
	std::map<std::string, bool> isExtensible = recorder.getIsExtensible();
	for(auto clas : recorder.getClassHierarchy()) {
		for(auto parent : *clas.second)	if(isExtensible[clas.first] != isExtensible[parent])
			*out << clas.first << "(" << isExtensible[clas.first] << ") --> " << parent << "(" << isExtensible[parent] << ")\n";
	}
}

void OMRStatistics::HMConsumer::printAllClasses(HMRecorder& recorder, llvm::raw_ostream* out) {
	*out << "Namespace;ClassName;isExtensible\n";
	std::map<std::string, bool> isExtensible = recorder.getIsExtensible();
	for(auto itr : isExtensible) { //itr: QualifiedClassName --> isExtensible
		if(HMConsumer::shouldIgnoreClassName(itr.first)) continue;
		std::vector<std::string>* tuple = seperateClassNameSpace(itr.first);
		*out << tuple->at(0)/*namespace*/ << ";" << tuple->at(1)/*className*/ << ";" << itr.second << "\n";
	}
}

void OMRStatistics::HMConsumer::printFunctionCalls(ASTContext& ctx, HMRecorder& recorder, llvm::raw_ostream* out) {
	*out << "CallerNamespace;CallerClassName;CallerFuncSig;CalledFuncSignature;ReceiverNamespace;ReceiverClassName\n";
	//std::vector<FunctionCall*>* functionCalls = getFunctionCalls(ctx);
	for(FunctionCall* fc : recorder.getFunctionCalls()) {
		std::vector<std::string>* caller = seperateClassNameSpace(fc->callerClass());
		std::vector<std::string>* receiver = seperateClassNameSpace(fc->receiverClass());
		*out << caller->at(0) << ";" << caller->at(1) << ";" << fc->callerFuncSig() << ";" << fc->receiverFuncSig() << ";" << receiver->at(0) << ";" << receiver->at(1) << "\n";
	}
}

void OMRStatistics::HMConsumer::HandleTranslationUnit(ASTContext &Context) {
	HMRecorder recorder(&Context);
	recorder.TraverseDecl(Context.getTranslationUnitDecl());
	recorder.addNeglectedClasses();
	std::map<std::string, std::vector<std::string>*> classHierarchy = recorder.getClassHierarchy();
	fillHierarchies(classHierarchy);
	collectMethodInfo(recorder);
	
	
	std::vector<std::string> outputFiles = {"hierarchy", "weirdHierarchy", "allClasses", "overloads", "allFunctions", "functionLocation", "overrides", "avg", "functionCalls"};
	std::vector<llvm::raw_ostream*>* outputs = new std::vector<llvm::raw_ostream*>();
	
	bool useLLVMOuts = true;
	
	if(conf.outputDir.compare("-1") != 0) {
		useLLVMOuts = false;
		//Open files to output (if file does not exist, create file in given directory)
		std::error_code EC;
		for(std::string fileExt : outputFiles) {
			outputs->emplace_back(new llvm::raw_fd_ostream(conf.outputDir + "." + fileExt, EC, llvm::sys::fs::F_Append));
			assert(!EC);
		}
	}
	else for(std::string fileExt : outputFiles) outputs->emplace_back(&(llvm::outs()));
	
	if(conf.hierarchy)  {
		printHierarchies(recorder, outputs->at(0)/*hierarchyOutput*/);
		printWeirdHierarchies(recorder, outputs->at(1)/*weirdHierarchyOutput*/);
		printAllClasses(recorder, outputs->at(2)/*allClassesOutput*/);
	}
	if(conf.overloading) {
		printAllFunctions(outputs->at(4)/*allFunctionsOutput*/);
	}
	printFunctionLocations(recorder, outputs->at(5));
	printOverrides(outputs->at(6));
	printAverageOverrides(recorder, outputs->at(7));
	printFunctionCalls(Context, recorder, outputs->at(8)/*functionCallsOutput*/);
	
	//Flush all outputs to their respective files
	for(llvm::raw_ostream* output : *outputs) output->flush();
	
	//Free memory
	if(conf.outputDir.compare("-1") != 0) 
		for(size_t i = 0; i < outputs->size(); i++) delete outputs->at(i);
	 
}

std::unique_ptr<ASTConsumer> OMRStatistics::CheckingAction::CreateASTConsumer(CompilerInstance &CI, llvm::StringRef filename) {
	return std::unique_ptr<ASTConsumer>(new HMConsumer(filename, conf));
}

int OMRStatistics::CheckingAction::findLastCharIn(std::string input, char key) {
	int pos = -1;
	int i = 0;
	for(char c : input) {
		if(c == key) pos = i;
		i++;
	}
	return pos;
}

bool OMRStatistics::CheckingAction::ParseArgs(const CompilerInstance &CI, const std::vector<std::string>& args) {
	for(std::string arg : args) {
		if(arg.compare("OMR_STAT_PRINT_HIERARCHY") == 0 || getenv("OMR_STAT_PRINT_HIERARCHY") != NULL) {
			conf.hierarchy = 1;
		}
		else if(arg.compare("OMR_STAT_PRINT_OVERLOADS") == 0 || getenv("OMR_STAT_PRINT_OVERLOADS") != NULL) conf.overloading = 1;
		else conf.outputDir = arg;
	}
	return true;
}
#undef trace
#endif

// Register OMRStatistics checking action in a plugin registry.
static FrontendPluginRegistry::Add<OMRStatistics::CheckingAction>
X("omr-statistics", "OMR statistics");
