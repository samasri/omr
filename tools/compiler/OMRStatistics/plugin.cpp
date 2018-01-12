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

std::map<std::string, std::unordered_set<std::string*>> OMRStatistics::ExtensibleClassCheckingVisitor::getClass2Methods() {return Class2Methods;}

void OMRStatistics::ExtensibleClassCheckingVisitor::setClass2Methods(std::map<std::string, std::unordered_set<std::string*>> Class2Methods) {this->Class2Methods = Class2Methods;}

std::map<std::string, std::string> OMRStatistics::ExtensibleClassCheckingVisitor::getclassHierarchy() {return classHierarchy;}

void OMRStatistics::ExtensibleClassCheckingVisitor::setclassHierarchy(std::map<std::string, std::string> classHierarchy) {this->classHierarchy = classHierarchy;}
	   
void OMRStatistics::ExtensibleClassCheckingVisitor::recordFunctions(const CXXRecordDecl* inputClass) {
	std::string className = inputClass->getQualifiedNameAsString();
	//Iterate through every method in the class
	for(auto A = inputClass->method_begin(), E = inputClass->method_end(); A != E; ++A) {
		
		//Get function name with parameter types (AKA: recreate function signature)
		std::string* function = new std::string((*A)->getNameAsString());
		ArrayRef<clang::ParmVarDecl*> functions = A->parameters();
		if(functions.size() == 0) *function += "()";
		else {
			*function += "(";
			for(clang::ParmVarDecl* param : functions) *function += param->getOriginalType().getAsString() + ",";
			function->replace(function->end()-1, function->end(), "");
			*function += ")";
		}
		
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

void OMRStatistics::ExtensibleClassCheckingVisitor::recordParents(const CXXRecordDecl *decl) {
	//Initializing variables preparing for the iterations
	const CXXRecordDecl * currentClass = decl;
	CXXRecordDecl::base_class_const_iterator BI, BE;
	std::string currentClassName = currentClass->getQualifiedNameAsString();
	std::string childClassName = currentClass->getQualifiedNameAsString();
	
	//Looping through parents
	while(1) {
		if(!currentClass) break;
		currentClassName = currentClass->getQualifiedNameAsString();
		
		//Record parent-child relationship
		if(currentClassName.compare(childClassName) != 0) {
			auto iterator = classHierarchy.find(childClassName);
			auto end = classHierarchy.end();
			
			// if class is already in Class2Methods and is mapped to a parent different than the current one then something is wrong
			assert(iterator != end && (iterator->second.compare(currentClassName) != 0) && "Class has more than one unique parent"); 
			
			if(iterator == end) //classHierarchy does not have the current class, add it to classHierarchy
				classHierarchy.emplace(childClassName, currentClassName);
				
			childClassName = currentClassName;
		}
		
		//Go to parent class
		BI = currentClass->bases_begin();
		BE = currentClass->bases_end();
		if(BI != BE) currentClass = BI->getType()->getAsCXXRecordDecl();
		else break;
	}
}

bool OMRStatistics::ExtensibleClassCheckingVisitor::VisitCXXRecordDecl(const CXXRecordDecl *decl) {
	if(!decl || !decl->isClass() || !decl->hasDefinition()) return true;
	
	recordFunctions(decl);
	recordParents(decl);
	
	return true;
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
OMRStatistics::MethodTracker::MethodTracker(std::string className, std::string methodSignature, bool firstOccurence) {
	methodName = OMRCheckingConsumer::getName(methodSignature);
	this->methodSignature = methodSignature;
	nbOfOccurences = 1;
	classesOverriden = new std::vector<std::string>();
	this->firstOccurence = firstOccurence;
	baseClassName = className;
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

OMRStatistics::OMRCheckingConsumer::OMRCheckingConsumer(llvm::StringRef filename, Config conf) {
	this->conf = conf;
}

OMRStatistics::Hierarchy* OMRStatistics::OMRCheckingConsumer::modifyBase(LinkedNode* oldBase, LinkedNode* newBase) {
	for (auto hierarchy : hierarchies) 
		if(hierarchy->base == oldBase) {
			hierarchy->base = newBase;
			return hierarchy;
		}
	return nullptr;
}

void OMRStatistics::OMRCheckingConsumer::deleteHierarchy(LinkedNode* base) {
	
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

void OMRStatistics::OMRCheckingConsumer::fillHierarchies(std::map<std::string, std::string> &map) {
	for(auto current : map) {
		std::string currentClassName = current.first;
		std::string currentParentName = current.second;
		LinkedNode* newNode = new LinkedNode();
		auto result1 = class2Address.find(currentClassName);
		auto result2 = class2Address.find(currentParentName);
		auto end = class2Address.end();
		
		if(result1 != end && result2 != end) { // If both child and parent nodes are found in hierarchy list
			result1->second->parent = result2->second;
			deleteHierarchy(result2->second);
		}
		else if(result1 != end) { // If child node is found in hierarchy list
			LinkedNode* child = result1->second;
			newNode->name = currentParentName;
			child->parent = newNode;
			class2Address.emplace(newNode->name, newNode);
		}
		
		else if(result2 != end) { // If parent node is found in hierarchy list
			LinkedNode* parent = result2->second;
			newNode->name = currentClassName;
			newNode->parent = parent;
			class2Address.emplace(newNode->name, newNode);
			auto hierarchy = modifyBase(parent, newNode);
			if(!hierarchy) { // No hierarchy with base as parent is found
				Hierarchy* newHierarchy = new Hierarchy();
				newHierarchy->base = newNode;
				hierarchies.push_back(newHierarchy);
			}
		}
		
		//If both nodes not found in hierarchy list
		else /*if(result1 == end && result2 == end)*/ {
			Hierarchy* newHierarchy = new Hierarchy();
			LinkedNode* newChildNode = new LinkedNode();
			newChildNode->name = currentClassName;
			newNode->name = currentParentName;
			newChildNode->parent = newNode;
			newHierarchy->base = newChildNode;
			hierarchies.push_back(newHierarchy);
			class2Address.emplace(newNode->name, newNode);
			class2Address.emplace(newChildNode->name, newChildNode);
		}
	}
}

void OMRStatistics::OMRCheckingConsumer::printHierarchy(Hierarchy* hierarchy) {
	llvm::outs() << "Printing Hierarchy: ";
	if(!hierarchy) {
		llvm::outs() << "<empty>\n";
		return;
	}
	auto current = hierarchy->base;
	while(current->parent) {
		llvm::outs() << current->name << " -->";
		current = current->parent;
	}
	llvm::outs() << current->name << "\n";
}

void OMRStatistics::OMRCheckingConsumer::printHierarchies(llvm::raw_ostream* out) {
	for(Hierarchy* current : hierarchies) {
		std::string singleHierarchy = "";
		LinkedNode* iterator = current->base;
		while(iterator->parent) {
			singleHierarchy += iterator->name + " --> ";
			iterator = iterator->parent;
		}
		singleHierarchy += iterator->name;
		if(shouldIgnoreClassName(singleHierarchy)) continue;
		(*out) << singleHierarchy << "\n";
	}
}

OMRStatistics::MethodTracker* OMRStatistics::OMRCheckingConsumer::searchForTracker(Hierarchy* hierarchy, std::string method, bool* sameName) {
	std::string methodName = getName(method);
	//Search for method trackers with same name
	auto trackers = hierarchy->methodName2MethodTracker;
	auto e1 = trackers.end();
	auto itr1 = trackers.find(methodName);
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

std::string OMRStatistics::OMRCheckingConsumer::getName(std::string methodSignature) {
	//Get method name from signature
	std::size_t pos = methodSignature.find("(");
	assert(pos != std::string::npos && "method name is invalid");
	return methodSignature.substr(0, pos);
}

void OMRStatistics::OMRCheckingConsumer::collectMethodInfo(ExtensibleClassCheckingVisitor &visitor) {
	auto map = visitor.getClass2Methods();
	for(auto hierarchy : hierarchies) {
		LinkedNode* current = hierarchy->base;
		
		//iterate hierarchy from top to base
		std::vector<LinkedNode*> classArray;
		while(current) {
			classArray.push_back(current);
			current = current->parent;
		}
		for(unsigned long i = 0, j = classArray.size() - 1; i < classArray.size()/2; i++) {
			LinkedNode* temp1 = classArray.at(i);
			LinkedNode* temp2 = classArray.at(j);
			classArray.at(i) = temp2;
			classArray.at(j) = temp1;
			j--;
		}
		
		//Iterate through each hierarchy's classes
		for(LinkedNode* current : classArray) {
			std::string className = current->name;
			auto Class2MethodsIterator = map.find(className);
			
			if(Class2MethodsIterator == map.end()) {
				//This case is when the class is in the hierarchy but not recorded in Class2Methods maps, this is usually because the class has no functions
				current = current->parent;
				continue;
			}
			
			//Iterate through the methods and connect them to their classes via MethodTracker objects
			std::unordered_set<std::string*> methods = Class2MethodsIterator->second;
			for(std::string* methodPtr : methods) {
				std::string method = *methodPtr;
				bool sameName = false;
				auto tracker = searchForTracker(hierarchy, method, &sameName);
				//If we found the methodTracker then add the class to it, or else create a new one
				if(tracker) tracker->addOccurence(className);
				else {
					std::string methodName = getName(method);
					bool isFirstOccurence = true;
					std::vector<MethodTracker>* trackers;
					if(sameName) { //MethodTrackers with same name were found, this is an overload
						isFirstOccurence = false;
						trackers = hierarchy->methodName2MethodTracker.find(methodName)->second;
					}
					else { //This is a completely new method
						trackers = new std::vector<MethodTracker>();
						hierarchy->methodName2MethodTracker.emplace(methodName, trackers);
					}
					MethodTracker newTracker(className, method, isFirstOccurence);
					trackers->emplace_back(newTracker);
				}
			}
			
			//Jump to parent class
			current = current->parent;
		}
	}
}

bool OMRStatistics::OMRCheckingConsumer::shouldIgnoreNamespace(std::string nameSpace) {
	if(nameSpace.compare("std") == 0) return true;
	if(nameSpace.compare("__gnu_cxx") == 0) return true;
	return false;
}

bool OMRStatistics::OMRCheckingConsumer::shouldIgnoreClassName(std::string nameSpace) {
	if(nameSpace.find("std::") != std::string::npos) return true;
	if(nameSpace.find("__gnu_cxx::") != std::string::npos) return true;
	return false;
}

std::vector<std::string>* OMRStatistics::OMRCheckingConsumer::seperateClassNameSpace(std::string input) {
	std::string nameSpace = "";
	std::string className = "";
	if(input.find("::") != std::string::npos) {
		size_t pos = input.find("::");
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

void OMRStatistics::OMRCheckingConsumer::printOverloads(llvm::raw_ostream* out) {
	(*out) << "FunctionName, FunctionSignature, IsFirstOccurence, Namespace, ClassName\n";
	for(auto hierarchy : hierarchies) {
		auto trackerMap = hierarchy->methodName2MethodTracker;
		//Iterate map to go through all trackers
		auto b = trackerMap.begin();
		auto e = trackerMap.end();
		auto itr = b;
		while(itr != e) {
			auto hierarchyTrackers = itr->second;
			for(auto tracker : *hierarchyTrackers) { //The code in this block will be accessed by every tracker
				std::vector<std::string>* tuple = seperateClassNameSpace(tracker.baseClassName);
				if(!shouldIgnoreNamespace(tuple->at(0))) {
					(*out) << tracker.methodName << ",";
					(*out) << tracker.methodSignature << ",";
					(*out) << tracker.firstOccurence << ",";
					(*out) << tuple->at(0) << ","; //namespace
					(*out) << tuple->at(1) << "\n";//className
				}
			}
			itr++;
		}
	}
}

void OMRStatistics::OMRCheckingConsumer::printOverrides(llvm::raw_ostream* out) {
	(*out) << "BaseNamespace, BaseClassName, FunctionSignature, OverridingNamespace, OverridingClassName\n";
	for(auto hierarchy : hierarchies) {
		auto trackerMap = hierarchy->methodName2MethodTracker;
		//Iterate map to go through all trackers
		auto b = trackerMap.begin();
		auto e = trackerMap.end();
		auto itr = b;
		while(itr != e) {
			auto hierarchyTrackers = itr->second;
			for(auto tracker : *hierarchyTrackers) { //The code in this block will be accessed by every tracker
				std::string baseClassName = tracker.baseClassName;
				for(std::string className : *tracker.classesOverriden) {
					std::vector<std::string>* baseClassNameTuple = seperateClassNameSpace(baseClassName);
					std::vector<std::string>* classNameTuple = seperateClassNameSpace(className);
					if(!shouldIgnoreNamespace(baseClassNameTuple->at(0)) || !shouldIgnoreNamespace(classNameTuple->at(0))) {
						(*out) << baseClassNameTuple->at(0) << ","; //namespace
						(*out) << baseClassNameTuple->at(1) << ",";//className
						(*out) << tracker.methodSignature << ",";
						(*out) << classNameTuple->at(0) << ","; //namespace
						(*out) << classNameTuple->at(1) << "\n";//className
					}
					baseClassName = className;
				}
			}
			itr++;
		}
	}
}

void OMRStatistics::OMRCheckingConsumer::printClass2Method(std::map<std::string, std::vector<std::string>> &map) {
	for(auto pair : map) {
		std::string className = pair.first;
		std::vector<std::string> methods = pair.second;
		for(std::string method : methods) {
			llvm::outs() << className << " --> " << method << "\n";
		}
	}
}

void OMRStatistics::OMRCheckingConsumer::HandleTranslationUnit(ASTContext &Context) {
	ExtensibleClassCheckingVisitor extchkVisitor(&Context);
	extchkVisitor.TraverseDecl(Context.getTranslationUnitDecl());
	
	auto classHierarchy = extchkVisitor.getclassHierarchy();
	fillHierarchies(classHierarchy);
	collectMethodInfo(extchkVisitor);
	
	llvm::raw_ostream* hierarchyOutput = nullptr;
	llvm::raw_ostream* overloadOutput = nullptr;
	llvm::raw_ostream* overrideOutput = nullptr;
	bool useLLVMOuts = true;
	
	if(conf.outputDir.compare("-1") != 0) {
		useLLVMOuts = false;
		//Open files to output (if file does not exist, create file in given directory)
		std::error_code EC;
		
		hierarchyOutput = new llvm::raw_fd_ostream(conf.outputDir + ".hierarchy", EC, llvm::sys::fs::F_Append);
		assert(!EC);
		
		overloadOutput = new llvm::raw_fd_ostream(conf.outputDir + ".overloads", EC, llvm::sys::fs::F_Append);
		assert(!EC);
		
		overrideOutput = new llvm::raw_fd_ostream(conf.outputDir + ".overrides", EC, llvm::sys::fs::F_Append);
		assert(!EC);
	}
	else {
		hierarchyOutput = &(llvm::outs());
		overloadOutput = &(llvm::outs());
		overrideOutput = &(llvm::outs());
		llvm::outs() << "Passing here\n";
	}
	
	
	/*if(conf.hierarchy)*/ printHierarchies(hierarchyOutput);
	/*if(conf.overloading)*/ printOverloads(overloadOutput);
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
	return std::unique_ptr<ASTConsumer>(new OMRCheckingConsumer(filename, conf));
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
