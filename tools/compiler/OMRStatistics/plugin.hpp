#undef NDEBUG
#include <string>
#include <queue>
#include <map>
#include <list>
#include <algorithm>
#include <assert.h>
#include <fstream>
#include <iostream>
#include <unordered_set>

using namespace llvm;
using namespace clang;

namespace OMRStatistics {
	//Includes information needed from the HMRecorder when processing the info by the HMConsumer
	struct FunctionDeclInfo {
		bool isImplicit;
		bool isVirtual;
		std::string location;
		FunctionDeclInfo(bool isImplicit, bool isVirtual, std::string location);
	};
	
	class HMRecorder : public RecursiveASTVisitor<HMRecorder> {
	private:
		//Mapping between each class and all its methods
		std::map<std::string, std::unordered_set<std::string*>> class2Methods;
		//Mapping between each class and whether its extensible or not
		std::map<std::string, bool> isExtensible;
		//Mapping between each function signature and if its implicit or not
		std::map<std::string, FunctionDeclInfo*> functionDeclInfo;
		//Parent-child relationship mapping (child --> parents)
		std::map<std::string, std::vector<std::string>*> classHierarchy;
	
	public:
		//Getters and setters
		std::map<std::string, std::unordered_set<std::string*>> getClass2Methods();
		void setClass2Methods(std::map<std::string, std::unordered_set<std::string*>>);
		std::map<std::string, std::vector<std::string>*> getClassHierarchy();
		void setClassHierarchy(std::map<std::string, std::vector<std::string>*>);
		std::map<std::string, FunctionDeclInfo*> getFunctionDeclInfo();
		void setFunctionDeclInfo(std::map<std::string, FunctionDeclInfo*>);
		std::map<std::string, bool> getIsExtensible();
		void setIsExtensible(std::map<std::string, bool>);
		
		explicit HMRecorder(ASTContext *Context) { }
		
		//Checks if a specific declaration contains "OMR_EXTENSIBLE" or not
		bool checkExtensibility(const CXXRecordDecl*);
		//Loop through the methods of the given class and input them in Class2Methods
		void recordFunctions(const CXXRecordDecl* inputClass);
		//Given a child and parent class names, it adds them to the classHierarchy map
		bool recordParents(std::string childClassName, std::string parentClassName);
		//Loop through all parents of the given class, recording their relationships in classHierarchy
		void recordParents(const CXXRecordDecl *decl);
		//Called by clang for every class declaration
		bool VisitCXXRecordDecl(const CXXRecordDecl*);
		//Prints the location of a specific declaration
		static std::string printLoc(const clang::CXXRecordDecl*);
		static std::string printLoc(const CXXMethodDecl*);
		size_t findLastStringIn(std::string input, char key);
		std::string printLoc(clang::CXXMethodDecl*);
	};
	
	class MethodTracker;
	
	//Represents a class in a class hierarchy
	struct LinkedNode {
		std::vector<LinkedNode*>* parents = nullptr; //Pointer to the parent class
		std::string name; //Name of the class
		
		LinkedNode(std::string name);
	};
	
	struct Hierarchy {
		LinkedNode* base; //Base class of hierarchy
		std::string name; //Base name, to identify the class
		
		//Vector of maps: Each map in the vector represents a unique subhierarchy
		//The Map connects every method to the array of hierarchy classes where it occurred
		std::vector<std::map<std::string, std::vector<MethodTracker>*>*> methodName2MethodTrackerVec;
		
		//overriding operators for faster comparisons
		bool operator==(const Hierarchy& other);
		bool operator==(const std::string other);
		bool operator!=(const Hierarchy& other);
		bool operator!=(const std::string other);
		
	};
	
	class MethodTracker {
	public:
		std::string methodName;
		std::string methodSignature;
		int nbOfOccurences; //Tracks how many times this function was overriden
		std::vector<std::string>* classesOverriden; //Tracks the classes where this method was overridden
		bool firstOccurence; //Specifies if this is the first occurrence of this function name or not (for overload)
		std::string baseClassName; //The first occurrence of this signature, this value includes namespace
		bool isImplicit; //Indicates whether this declaration is an implicit one or not
		bool isVirtual; //Indicates whether this function is a case of dynamic or static polymorphism
		
		MethodTracker(std::string className, std::string methodSignature, bool firstOccurence, bool isImplicit, bool isVirtual);
		//Add an occurrence for this method
		void addOccurence(std::string className);
		
		//Overriding operators for faster comparisons
		bool operator==(const MethodTracker& other);
		bool operator==(const std::string other);
	};
	
	//This struct is the resultant HMConsumer::isFoundInHierarchies
	struct HierarchySearchResult {
		//If true, the target node should be the new base of the class hierarchy
		bool changeBase;
		//If true, the target node should be the new top of the class hierarchy
		bool changeTop;
		//If the search was successfull (1) or not (0)
		bool isFound;
		//Index of the hierarchy in the hierarchies vector that needs to be changed
		LinkedNode* nodeAddress;
	};
	
	struct Config {
		bool hierarchy = false;
		bool overloading = false;
		std::string outputDir = "-1";
	};
	
	class HMConsumer : public ASTConsumer {
	private:
		Config conf;
		//An array of linked nodes forming the class hierarchy. Every record in this array represents a class hierarchy in OMR
		std::vector<Hierarchy*> hierarchies;
		std::map<std::string, LinkedNode*> class2Address;
	public:
		
		explicit HMConsumer(llvm::StringRef filename, Config conf);
		//Searches all hierarchies for the one with the given base, and changes it to the new given base
		Hierarchy* modifyBase(LinkedNode* oldBase, LinkedNode* newBase);
		// Deletes the hierarchy that has the given base (if found)
		void deleteHierarchy(LinkedNode* base);
		//Checks if the given class name is a base of any hierarchies
		bool isBase(std::string className);
		//Process the classHierarchy map from HMRecorder to fill the hierarchies map.
		void fillHierarchies(std::map<std::string, std::vector<std::string>*> &map);
		//Get method name from its signature
		static std::string getName(std::string methodSignature);
		//Search for the MethodTracker with the inputted function name in the inputted hierarchy
		MethodTracker* searchForTracker(std::map<std::string, std::vector<MethodTracker>*>* methodName2MethodTracker, std::string method, bool* sameName);
		//Iterates through the entries of Class2Methods in the HMRecorder and creates MethodTrackers out of them
		void collectMethodInfo(HMRecorder &visitor);
		//Converts the hierarchy to an array of nodes, starting from the top to the base
		std::vector<std::vector<LinkedNode*>*>* getTopToBaseAsArray(OMRStatistics::Hierarchy* hierarchy);
		void getTopToBaseAsArray(LinkedNode* node, std::vector<LinkedNode*>* array, std::vector<std::vector<LinkedNode*>*>* subHierarchies);
		
		//Printing output files
		void printHierarchies(HMRecorder&, llvm::raw_ostream*);
		void printWeirdHierarchies(HMRecorder&, llvm::raw_ostream*);
		void printAllClasses(HMRecorder&, llvm::raw_ostream*);
		void printAllFunctions(llvm::raw_ostream*);
		void printOverrides(llvm::raw_ostream*);
		void printAverageOverrides(HMRecorder&, llvm::raw_ostream*);
		void printFunctionLocations(HMRecorder&, llvm::raw_ostream*);
		
		//Helper printing functions
		void printHierarchy(std::string, LinkedNode*, llvm::raw_ostream*);
		static bool shouldIgnoreClassName(std::string);
		std::vector<std::string>* seperateClassNameSpace(std::string input);
		size_t findLastStringIn(std::string input, std::string key);
		void printTracker(llvm::raw_ostream*, MethodTracker&);
		void printTracker(llvm::raw_ostream*, std::string, std::string, std::string, std::string, bool, bool);
		
		
		virtual void HandleTranslationUnit(ASTContext &Context);
	};
	
	class CheckingAction : public PluginASTAction {
	private:
		Config conf;
	protected:
		std::unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance &CI, llvm::StringRef filename);
		int findLastCharIn(std::string input, char key);
		//Required function -- pure virtual in parent
		bool ParseArgs(const CompilerInstance &CI, const std::vector<std::string>& args);
		//Required function -- pure virtual in parent
		void PrintHelp(llvm::raw_ostream& ros) {}
	};
}