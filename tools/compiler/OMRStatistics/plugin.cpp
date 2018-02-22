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
#include "clang/AST/Attr.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/AST/RecursiveASTVisitor.h"
#include "llvm/Support/raw_ostream.h"

#include "plugin.hpp"
#include <sstream>

OMRStatistics::FunctionDeclInfo::FunctionDeclInfo(bool isImplicit, bool isVirtual) {
	this->isImplicit = isImplicit;
	this->isVirtual = isVirtual;
}

std::map<std::string, std::unordered_set<std::string*>> OMRStatistics::HMRecorder::getClass2Methods() {return Class2Methods;}

void OMRStatistics::HMRecorder::setClass2Methods(std::map<std::string, std::unordered_set<std::string*>> Class2Methods) {this->Class2Methods = Class2Methods;}

std::map<std::string, std::vector<std::string>*> OMRStatistics::HMRecorder::getClassHierarchy() {return classHierarchy;}

void OMRStatistics::HMRecorder::setClassHierarchy(std::map<std::string, std::vector<std::string>*> classHierarchy) {this->classHierarchy = classHierarchy;}

std::map<std::string, OMRStatistics::FunctionDeclInfo*> OMRStatistics::HMRecorder::getfunctionDeclInfo() {
	return functionDeclInfo;
}

void OMRStatistics::HMRecorder::setfunctionDeclInfo(std::map<std::string, FunctionDeclInfo*>) {
	this->functionDeclInfo = functionDeclInfo;
}

std::map<std::string, bool> OMRStatistics::HMRecorder::getIsExtensible() {
	return isExtensible;
}

void OMRStatistics::HMRecorder::setIsExtensible(std::map<std::string, bool> isExtensible) {this->isExtensible = isExtensible;}

bool OMRStatistics::HMRecorder::checkExtensibility(const CXXRecordDecl* declIn) {
	const CXXRecordDecl* decl = declIn;
  
	//while (decl) {
	for (Decl::attr_iterator A = decl->attr_begin(), E = decl->attr_end(); A != E; ++A) {
		if (isa<AnnotateAttr>(*A)) {
			AnnotateAttr *annotation = dyn_cast<AnnotateAttr>(*A);
			if (annotation->getAnnotation() == "OMR_Extensible") return true;
		}
	}
	//decl = decl->getPreviousDecl();
	// }
  
  return false;
}
	   
void OMRStatistics::HMRecorder::recordFunctions(const CXXRecordDecl* inputClass) {
	std::string className = inputClass->getQualifiedNameAsString();
	//Iterate through every method in the class
	for(auto A = inputClass->method_begin(), E = inputClass->method_end(); A != E; ++A) {
		//Get function name with parameter types (AKA: recreate function signature)
		std::string* function = new std::string((*A)->getNameAsString());
		ArrayRef<clang::ParmVarDecl*> functions = A->parameters();
		if(functions.size() == 0) *function += "()";
		else {
			*function += "(";
			for(clang::ParmVarDecl* param : functions) {
				*function += param->getOriginalType().getAsString() + ",";
			}
			function->replace(function->end()-1, function->end(), "");
			*function += ")";
		}
		FunctionDeclInfo* info = new FunctionDeclInfo((*A)->isImplicit(), (*A)->isVirtual());
		functionDeclInfo.emplace(*function, info);
		
		auto iterator = Class2Methods.find(className);
		if(iterator != Class2Methods.end()) { //If the class was already encountered before, pull methods vector from Class2Methods
			std::unordered_set<std::string*>* methods = &(iterator->second);
			methods->insert(function);
		}
		else { //If the class in new
			std::unordered_set<std::string*> methods;
			methods.insert(function);
			Class2Methods.emplace(className, methods);
		}
	}
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

std::string OMRStatistics::HMRecorder::printLoc(const clang::CXXRecordDecl* d) {
	std::string result;
	result = d->getLocStart().printToString(d->getASTContext().getSourceManager());
	return result;
}

std::string OMRStatistics::HMRecorder::printLoc(clang::CXXMethodDecl* d) {
	std::string result;
	result = d->getLocStart().printToString(d->getASTContext().getSourceManager()) + "\n";
	return result;
}

void OMRStatistics::HMRecorder::recordParents(const CXXRecordDecl *decl) {
	if(!decl) return;
	std::string currentClassName = decl->getQualifiedNameAsString();
	
	//Record extensibility of the declaration
	bool currentIsExtensible =  checkExtensibility(decl);
	if(isExtensible.find(currentClassName) == isExtensible.end()) 
		isExtensible.emplace(currentClassName, currentIsExtensible);
	else if(isExtensible[currentClassName] == false) 
		isExtensible[currentClassName] = currentIsExtensible;
	
	if(HMConsumer::shouldIgnoreClassName(currentClassName)) return;
	CXXRecordDecl::base_class_const_iterator BI, BE, BC;
	
	BI = decl->bases_begin();
	BE = decl->bases_end();
	for(BC = BI; BC != BE; BC++) { //iterate through all parents
		clang::QualType parentClassType = BC->getType();
		CXXRecordDecl* parentDecl = parentClassType->getAsCXXRecordDecl();
		
		
		std::string parentClassName = (parentDecl) ? parentDecl->getQualifiedNameAsString() : parentClassType.getAsString(); //Prioritize having the name of the CXX record over general QualTypes
		if(!parentDecl) continue;
		if(HMConsumer::shouldIgnoreClassName(parentClassName) || HMConsumer::shouldIgnoreClassName(currentClassName)) continue;
		recordParents(currentClassName, parentClassName);
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
	methodName = HMConsumer::getName(methodSignature);
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

void OMRStatistics::HMConsumer::fillHierarchies(std::map<std::string, std::vector<std::string>*> &map) {
	for(auto current : map) {
		std::string childName = current.first;
		std::vector<std::string>* parents = current.second;
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

OMRStatistics::MethodTracker* OMRStatistics::HMConsumer::searchForTracker(std::map<std::string, std::vector<MethodTracker>*>* methodName2MethodTracker, std::string method, bool* sameName) {
	std::string methodName = getName(method);
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

std::string OMRStatistics::HMConsumer::getName(std::string methodSignature) {
	//Get method name from signature
	std::size_t pos = methodSignature.find("(");
	assert(pos != std::string::npos && "method name is invalid");
	return methodSignature.substr(0, pos);
}

void OMRStatistics::HMConsumer::collectMethodInfo(HMRecorder &recorder) {
	auto map = recorder.getClass2Methods();
	std::map<std::string, FunctionDeclInfo*> functionDeclInfo = recorder.getfunctionDeclInfo();
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
				auto itr = map.find(className);
				if(itr == map.end()) continue;
				std::unordered_set<std::string*> methods = itr->second;
				for(std::string* methodPtr : methods) {
					std::string method = *methodPtr;
					bool sameName = false;
					MethodTracker* tracker = searchForTracker(methodName2MethodTracker, method, &sameName);
					if(tracker)  //This is an override
						tracker->addOccurence(className);
					else {
						std::string methodName = getName(method);
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
						MethodTracker newTracker(className, method, isFirstOccurence, functionDeclInfo[method]->isImplicit, functionDeclInfo[method]->isVirtual);
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

bool OMRStatistics::HMConsumer::shouldIgnoreNamespace(std::string nameSpace) {
	if(nameSpace.compare("std") == 0) return true;
	if(nameSpace.compare("__gnu_cxx") == 0) return true;
	return false;
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
	else if(input.find("TR_") != std::string::npos) {
		nameSpace = "TR";
		int classNameSize = input.length() - 3;
		className = input.substr(3, classNameSize);
	}
	else if(input.find("TRPersistentMemoryAllocator") != std::string::npos) {
		nameSpace = "TR";
		className = "PersistentMemoryAllocator";
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

void OMRStatistics::HMConsumer::printOverloads(llvm::raw_ostream* out) {
	(*out) << "FunctionName; FunctionSignature; IsFirstOccurence; Namespace; ClassName; isImplicit; isVirtual\n";
	for(auto hierarchy : hierarchies) {
		auto trackerMapVec = hierarchy->methodName2MethodTrackerVec;
		for(auto trackerMap : trackerMapVec) { //Go through the map of each subHierarchy
			//Iterate the subHierarchy map to go through all trackers
			auto b = trackerMap->begin();
			auto e = trackerMap->end();
			auto itr = b;
			while(itr != e) {
				auto hierarchyTrackers = *(itr->second);
				if(hierarchyTrackers.size() < 2) { 
				//If methodname has only one signature, then it is not overloaded
					itr++;
					continue;
				}
				//Go through each tracker (signature) for a specific method name and report the overloads
				for(auto tracker : hierarchyTrackers) {
					std::vector<std::string>* tuple = seperateClassNameSpace(tracker.baseClassName);
					if(!shouldIgnoreNamespace(tuple->at(0))) {
						(*out) << tracker.methodName << ";";
						(*out) << tracker.methodSignature << ";";
						(*out) << tracker.firstOccurence << ";";
						(*out) << tuple->at(0) << ";"; //namespace
						(*out) << tuple->at(1) << ";";//className
						(*out) << tracker.isImplicit << ";";
						(*out) << tracker.isVirtual << "\n";
					}
				}
				itr++;
			}
		}
	}
}

void OMRStatistics::HMConsumer::printOverrides(llvm::raw_ostream* out) {
	(*out) << "BaseNamespace; BaseClassName; FunctionSignature; OverridingNamespace; OverridingClassName; isImplicit; isVirtual\n";
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
						if(!shouldIgnoreNamespace(baseClassNameTuple->at(0)) || !shouldIgnoreNamespace(classNameTuple->at(0))) {
							(*out) << baseClassNameTuple->at(0) << ";"; //namespace
							(*out) << baseClassNameTuple->at(1) << ";";//className
							(*out) << tracker.methodSignature << ";";
							(*out) << classNameTuple->at(0) << ";"; //namespace
							(*out) << classNameTuple->at(1) << ";";//className
							(*out) << tracker.isImplicit << ";";
							(*out) << tracker.isVirtual << "\n";
						}
						baseClassName = className;
					}
				}
				itr++;
			}
		}
	}
}

void OMRStatistics::HMConsumer::printHierarchies(llvm::raw_ostream* out) {
	for(Hierarchy* h : hierarchies) {
		printHierarchy("", h->base, "", out);
	}
}

void OMRStatistics::HMConsumer::printHierarchy(std::string history, LinkedNode* node, std::string tabs, llvm::raw_ostream* out) {
	history += node->name + " --> ";
	std::vector<LinkedNode*>* parents = node->parents;
	for(LinkedNode* parent : *parents) {
		printHierarchy(history, parent, tabs + "\t", out);
	}
	if(parents->size() == 0) (*out) << history.substr(0, history.size() - 5) << "\n";
}

void OMRStatistics::HMConsumer::printWeirdHierarchies(HMRecorder& recorder, llvm::raw_ostream* out) {
	std::map<std::string, bool> isExtensible = recorder.getIsExtensible();
	for(auto clas : recorder.getClassHierarchy()) {
		for(auto parent : *clas.second)	if(isExtensible[clas.first] != isExtensible[parent])
			llvm::outs() << clas.first << "(" << isExtensible[clas.first] << ") --> " << parent << "(" << isExtensible[parent] << ")\n";
	}
}

void OMRStatistics::HMConsumer::HandleTranslationUnit(ASTContext &Context) {
	HMRecorder recorder(&Context);
	recorder.TraverseDecl(Context.getTranslationUnitDecl());
	
	std::map<std::string, std::vector<std::string>*> classHierarchy = recorder.getClassHierarchy();
	fillHierarchies(classHierarchy);
	collectMethodInfo(recorder);
	
	llvm::raw_ostream* hierarchyOutput = nullptr;
	llvm::raw_ostream* weirdHierarchyOutput = nullptr;
	llvm::raw_ostream* overloadOutput = nullptr;
	llvm::raw_ostream* overrideOutput = nullptr;
	bool useLLVMOuts = true;
	
	if(conf.outputDir.compare("-1") != 0) {
		useLLVMOuts = false;
		//Open files to output (if file does not exist, create file in given directory)
		std::error_code EC;
		
		hierarchyOutput = new llvm::raw_fd_ostream(conf.outputDir + ".hierarchy", EC, llvm::sys::fs::F_Append);
		assert(!EC);
		
		weirdHierarchyOutput = new llvm::raw_fd_ostream(conf.outputDir + ".weirdHierarchy", EC, llvm::sys::fs::F_Append);
		assert(!EC);
		
		overloadOutput = new llvm::raw_fd_ostream(conf.outputDir + ".overloads", EC, llvm::sys::fs::F_Append);
		assert(!EC);
		
		overrideOutput = new llvm::raw_fd_ostream(conf.outputDir + ".overrides", EC, llvm::sys::fs::F_Append);
		assert(!EC);
	}
	else {
		hierarchyOutput = &(llvm::outs());
		weirdHierarchyOutput = &(llvm::outs());
		overloadOutput = &(llvm::outs());
		overrideOutput = &(llvm::outs());
	}
	
	if(conf.hierarchy)  {
		printHierarchies(hierarchyOutput);
		printWeirdHierarchies(recorder, weirdHierarchyOutput);
	}
	if(conf.overloading) 
		printOverloads(overloadOutput);
	printOverrides(overrideOutput);
	
	//Flush all outputs to their respective files
	hierarchyOutput->flush();
	overloadOutput->flush();
	overrideOutput->flush();
	
	//Free memory
	if(conf.outputDir.compare("-1") != 0) {
		delete hierarchyOutput;
		delete overloadOutput;
		delete overrideOutput;
	}
	 
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
