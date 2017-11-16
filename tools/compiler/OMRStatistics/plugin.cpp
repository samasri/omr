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
	   
void OMRStatistics::ExtensibleClassCheckingVisitor::recordFunctions(const CXXRecordDecl* inputClass) {
	std::string className = inputClass->getQualifiedNameAsString();
	
	//Iterate through every method in the class
	for(auto A = inputClass->method_begin(), E = inputClass->method_end(); A != E; ++A) {
		temp.push_back((*A)->getLocStart());
		//llvm::outs() << (*A)->getNameAsString() << " --> " << (*A)->isVirtual() << "\n";
		std::string functionName = (*A)->getNameAsString();
		auto iterator = Class2Methods.find(className);
		if(iterator != Class2Methods.end()) { //If the class was already encountered before, pull methods vector from Class2Methods
			std::unordered_set<std::string>* methods = &(iterator->second);
			methods->insert(functionName);
		}
		else { //If the class in new
			std::unordered_set<std::string> methods;
			methods.insert(functionName);
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

OMRStatistics::Hierarchy::~Hierarchy() {
	//Delete the base and top to prevent memory leaks
	delete base;
	delete top;
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

//Tracks the occurences of each method, what classes, when overriden, and when overloaded
OMRStatistics::MethodTracker::MethodTracker(Hierarchy* hierarchy, std::string methodName, std::string className) {
	//Instantiations
	this->methodName = methodName;
	classesOverriden = new std::unordered_set<std::string>();
	class2NbOfTimesOverloaded = new std::map<std::string, int>();		nbOfOccurences = 1;
	myHierarchy = hierarchy;
	isOverloaded = 0;
	
	addOccurence(className);
	
	//Recording that we have a tracker for that function in the corresponding hierarchy
	myHierarchy->methodNames->emplace(methodName);
	myHierarchy->methodTrackers->push_back(*this);
}

void OMRStatistics::MethodTracker::addOccurence(std::string className) {
	nbOfOccurences++;
	
	//Search classesOverriden for the current class where the method occurred
	auto itr = class2NbOfTimesOverloaded->find(className);
	auto end = class2NbOfTimesOverloaded->end();
	int nbOfOverloads = itr->second;
	//If method already appeared in this class, then this is an overload
	if(itr != end) {
		itr->second = nbOfOverloads + 1;
		isOverloaded = 1;
	}
	else {
		//This is the first occurrence for this method in this class
		classesOverriden->insert(className);
		class2NbOfTimesOverloaded->emplace(className, 0);
	}
}


bool OMRStatistics::MethodTracker::operator==(const MethodTracker& other) {
	return (methodName.compare(other.methodName) == 0);
}

bool OMRStatistics::MethodTracker::operator==(const std::string other) {
	return (methodName.compare(other) == 0);
}

//Search the top of each class hierarchy for the input class name
OMRStatistics::HierarchySearchResult* OMRStatistics::OMRCheckingConsumer::isFoundInHierarchies(std::string child, std::string parent) {
	HierarchySearchResult* result = new HierarchySearchResult();
	int counter = 0;
			
	for(Hierarchy* hierarchy : hierarchies) {
		//Search if the parent is the same as one of the base nodes of one of the class hierarchies, this means the base of that hierarchy should be changed
		if(hierarchy->base->name.compare(parent) == 0) {
			result->changeBase = 1;
			result->isFound = 1;
			result->index = counter;
			return result;
		}
		
		//Search if child is the same as top node in the class hierarchy, this means the node should be added on top of that hierarchy
		else if(hierarchy->top->name.compare(child) == 0) {
			result->changeTop = 1;
			result->isFound = 1;
			result->index = counter;
			return result;
		}
		counter++;
	}
	
	result->isFound = false;
	return result;
}

void OMRStatistics::OMRCheckingConsumer::refineHierarchies() {
	//Record all bases and tops at that point
	std::unordered_set<std::string>
		*bases = new std::unordered_set<std::string>(), 
		*tops = new std::unordered_set<std::string>();
	for(auto hierarchy : hierarchies) {
		bases->emplace(hierarchy->base->name);
		tops->emplace(hierarchy->top->name);
	}
	
	//Merge any broken hierarchies
	for(auto hierarchyItr = hierarchies.begin(), end = hierarchies.end(); hierarchyItr != end; hierarchyItr++) {
		Hierarchy* hierarchy = *hierarchyItr;
		std::string base = hierarchy->base->name;
		std::string top = hierarchy->top->name;
		
		//If we find it in the bases vector, then this top is a base for another hierarchy
		if(bases->find(top) != bases->end()) { 
			//Find that hierarchy
			for(auto hierarchy2Itr = hierarchies.begin(); hierarchy2Itr != end; hierarchy2Itr++) {
				Hierarchy* hierarchy2 = *hierarchy2Itr;
				//Merge it with the other hierarchy
				if(hierarchy2->base->name.compare(top) == 0) {
					hierarchy->top->parent = hierarchy2->base;
					hierarchy->top = hierarchy2->top;
					hierarchies.erase(hierarchy2Itr);
					bases->erase(hierarchy2->base->name);
					//Set hierarchy2 pointers to null so that we do not delete the actual LinkedNodes when deleting the object
					hierarchy2->top = nullptr;
					hierarchy2->base = nullptr;
					delete hierarchy2;
				}
			}
		}
		
	}
}

void OMRStatistics::OMRCheckingConsumer::fillHierarchies(std::map<std::string, std::string> &map) {
	for(auto current : map) {
		std::string currentClassName = current.first;
		std::string currentParentName = current.second;
		LinkedNode* newNode = new LinkedNode();
		
		//Search for the class in one of the recorded hierarchies so far
		HierarchySearchResult* result = isFoundInHierarchies(currentClassName, currentParentName);
		
		//Case when returned node should be the new base node of a hierarchy
		if(result->isFound) {
			Hierarchy* hierarchyToModify = hierarchies.at(result->index);
			if(result->changeBase) {
				newNode->name = currentClassName;
				newNode->parent = hierarchyToModify->base;
				hierarchyToModify->base = newNode;
			}
			//Case when returned node should be the parent
			if(result->changeTop) {
				newNode->name = currentParentName;
				hierarchyToModify->top->parent = newNode;
				hierarchyToModify->top = newNode;
			} 
			delete result;
		}
		//Case where the node was not found in any class hierarchy
		else {
			Hierarchy* newHierarchy = new Hierarchy();
			LinkedNode* newChildNode = new LinkedNode();
			newChildNode->name = currentClassName;
			newNode->name = currentParentName;
			newChildNode->parent = newNode;
			newHierarchy->base = newChildNode;
			newHierarchy->top = newNode;
			hierarchies.push_back(newHierarchy);
		}
	}
	refineHierarchies();
}

void OMRStatistics::OMRCheckingConsumer::printHierarchy() {
	for(Hierarchy* current : hierarchies) {
		std::string singleHierarchy = "";
		LinkedNode* iterator = current->base;
		while(iterator->parent) {
			singleHierarchy += iterator->name + " --> ";
			iterator = iterator->parent;
		}
		singleHierarchy += iterator->name;
		llvm::outs() << singleHierarchy << "\n";
	}
}

OMRStatistics::MethodTracker* OMRStatistics::OMRCheckingConsumer::searchForTracker(Hierarchy* hierarchy, std::string method) {
	auto trackers = hierarchy->methodTrackers;
	auto b = trackers->begin();
	auto e = trackers->end();
	auto itr = std::find(b, e, method);
	if (itr != e) return trackers->data() + (itr-b); //Change the iterator to the actual pointer to the target MethodTracker
	return nullptr;
}

void OMRStatistics::OMRCheckingConsumer::collectMethodInfo(ExtensibleClassCheckingVisitor &visitor) {
	for(auto hierarchy : hierarchies) {
		LinkedNode* current = hierarchy->base;
		auto map = visitor.Class2Methods;
		//Iterate through each hierarchy's classes
		while(current) {
			std::string className = current->name;
			auto Class2MethodsIterator = map.find(className);
			if(Class2MethodsIterator == map.end()) {
				//This case is when the class is in the hierarchy but not recorded in Class2Methods maps, this is usually because the class has no functions
				current = current->parent;
				continue;
			}
			
			std::unordered_set<std::string> methods = Class2MethodsIterator->second;
			//Iterate through the methods and connect them to their classes via MethodTracker objects
			for(std::string method : methods) {
				auto tracker = searchForTracker(hierarchy, method); 
				//If we found the methodTracker then add the class to it, or else create a new one
				if(tracker) tracker->addOccurence(className);
				else new MethodTracker(hierarchy, method, className);
			}
			current = current->parent;
		}
	}
}

void OMRStatistics::OMRCheckingConsumer::printMethodInfo(bool printOverloads, bool printOverrides) {
	
	for(auto hierarchy : hierarchies) {
		auto baseClassName = hierarchy->base->name;
		if(baseClassName.find("TR::") == std::string::npos) continue;
		auto methodTrackers = *(hierarchy->methodTrackers);
		if(methodTrackers.size() != 0) llvm::outs() << baseClassName << ":\n";
		else continue;
		llvm::outs() << "I reach here\n";
		for(auto tracker : methodTrackers) {
			std::string method = tracker.methodName;
			int nbOfOverrides = tracker.classesOverriden->size();
			/*if((nbOfOverrides > 1 && printOverrides) || (tracker.isOverloaded && printOverloads))
				llvm::outs() << "\tMethod name: " << method << "\n";
			else continue;*/
			if(nbOfOverrides > 1 && printOverrides) //Print override record in CSV format (MethodName, Override, className)
				for(std::string className : *(tracker.classesOverriden)) llvm::outs() << method << ",override," << className << "\n";
			if(tracker.isOverloaded && printOverloads) //Print overload record in CSV format (MethodName, Overload, className, nbOfTimesOverloaded)
				for(auto pair : *(tracker.class2NbOfTimesOverloaded)) if(pair.second > 0) llvm::outs() << method << ",overload," << pair.first << ", " << pair.second << "\n";
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
	
	fillHierarchies(extchkVisitor.classHierarchy);
	collectMethodInfo(extchkVisitor);
	
	for(auto a : extchkVisitor.temp) {
		llvm::outs() << a.printToString(Context.getSourceManager()) << "\n";
	}
	
	//Reading config file
	std::string line;
	std::ifstream config("config");
	assert(config.is_open() && "config file not found");
	
	//Read the boolean specifying if we print the hierarchy
	getline(config, line);
	if(line.compare("1") == 0) printHierarchy();
	
	//Read the boolean specifying if we print overloads
	bool printOverloads = false;
	getline(config, line);
	if(line.compare("1") == 0) printOverloads = true;
	
	//Read the boolean specifying if we print overloads
	bool printOverrides = false;
	getline(config, line);
	if(line.compare("1") == 0) printOverrides = true;
	
	//Read the boolean specifying if we print the method info
	if(printOverloads || printOverrides) printMethodInfo(printOverloads, printOverrides);
	
	config.close();
}

std::unique_ptr<ASTConsumer> OMRStatistics::CheckingAction::CreateASTConsumer(CompilerInstance &CI, llvm::StringRef filename) {
	return std::unique_ptr<ASTConsumer>(new OMRCheckingConsumer(filename));
}

bool OMRStatistics::CheckingAction::ParseArgs(const CompilerInstance &CI, const std::vector<std::string>& args) {
	return true;
}
#undef trace
#endif

// Register OMRStatistics checking action in a plugin registry.
static FrontendPluginRegistry::Add<OMRStatistics::CheckingAction>
X("omr-statistics", "OMR statistics");
