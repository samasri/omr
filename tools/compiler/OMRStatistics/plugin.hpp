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
	
	class HMRecorder : public RecursiveASTVisitor<HMRecorder> {
	private:
		//Mapping between each class and all its methods
		std::map<std::string, std::unordered_set<std::string*>> Class2Methods;
		//Parent-child relationship mapping (child --> parents)
		std::map<std::string, std::vector<std::string>*> classHierarchy;
	
	public:
		std::vector<std::string*>* debug = new std::vector<std::string*>();
		//Getters and setters
		std::map<std::string, std::unordered_set<std::string*>> getClass2Methods();
		void setClass2Methods(std::map<std::string, std::unordered_set<std::string*>> Class2Methods);
		std::map<std::string, std::vector<std::string>*> getclassHierarchy();
		void setclassHierarchy(std::map<std::string, std::vector<std::string>*> classHierarchy);
		
		explicit HMRecorder(ASTContext *Context) { }
		
		//Loop through the methods of the given class and input them in Class2Methods
		void recordFunctions(const CXXRecordDecl* inputClass);
		//Given a child and parent class names, it adds them to the classHierarchy map
		bool recordParents(std::string childClassName, std::string parentClassName);
		//Loop through all parents of the given class, recording their relationships in classHierarchy
		void recordParents(const CXXRecordDecl *decl);
		//Called by clang for every class declaration
		bool VisitCXXRecordDecl(const CXXRecordDecl *decl);
		//Prints the location of a specific declaration
		static std::string printLoc(const clang::CXXRecordDecl*);
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
		//Maps every method to the array of hierarchy classes where it occurred
		std::vector<std::map<std::string, std::vector<MethodTracker>*>> methodName2MethodTrackerVec;
		//Stores the names of each methodTracker in the hierarchy for faster searching
		//std::unordered_set<std::string>* methodNames = new std::unordered_set<std::string>; 
		
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
		
		MethodTracker(std::string className, std::string methodSignature, bool firstOccurence);
		//Add an occurence for this method
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
		MethodTracker* searchForTracker(Hierarchy* hierarchy, std::string method, bool* sameName);
		//Iterates through the entries of Class2Methods in the HMRecorder and creates MethodTrackers out of them
		void collectMethodInfo(HMRecorder &visitor);
		//Converts the hierarchy to an array of nodes, starting from the top to the base
		std::vector<std::vector<LinkedNode>>* getTopToBaseAsArray(OMRStatistics::Hierarchy* hierarchy);
		
		//Printing methods to check the results
		//Print the class hierarchies collected previously, this method works on the hierarchies vector, hence fillHierarchies should be called before it
		void printHierarchy(std::string, LinkedNode*, std::string, llvm::raw_ostream*);
		void printHierarchies(llvm::raw_ostream*);
		
		//Printing the method information
		
		//Judges whether we should ignore this namespace (if its not related to the project, like std classes)
		static bool shouldIgnoreNamespace(std::string nameSpace);
		static bool shouldIgnoreClassName(std::string nameSpace);
		
		std::vector<std::string>* seperateClassNameSpace(std::string input);
		size_t findLastStringIn(std::string input, std::string key);
		void printOverloads(llvm::raw_ostream* out);
		void printOverrides(llvm::raw_ostream* out);
		//Prints Class2Methods in HMRecorder
		void printClass2Method(std::map<std::string, std::vector<std::string>> &map);
		
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