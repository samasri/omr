#include <string>
#include <queue>
#include <map>
#include <list>
#include <algorithm>
#include <assert.h>
#include <iostream>
#include <unordered_set>


using namespace llvm;
using namespace clang;

namespace OMRStatistics {
	
	class ExtensibleClassCheckingVisitor : public RecursiveASTVisitor<ExtensibleClassCheckingVisitor> {
	
	public:
		//Mapping between each class and all its methods
		std::map<std::string, std::vector<std::string>> Class2Methods;
		//Parent-child relationship mapping (child --> parent)
		std::map<std::string, std::string> classHierarchy;
		
		explicit ExtensibleClassCheckingVisitor(ASTContext *Context) { }
		//Loop through the methods of the given class and input them in the given map
		void recordFunctions(const CXXRecordDecl* inputClass, std::map<std::string, std::vector<std::string>> &map);
		//Loop through all parents of the given class, recording their relationships in the given map
		void recordParents(const CXXRecordDecl *decl, std::map<std::string, std::string> &map);
		//Called by clang for every class declaration
		bool VisitCXXRecordDecl(const CXXRecordDecl *decl);
	};
	
	class MethodTracker;
	
	//Represents a class in a class hierarchy
	struct LinkedNode {
		LinkedNode* parent = nullptr; //Pointer to the parent class
		std::string name; //Name of the class
	};
	
	struct Hierarchy {
		LinkedNode* base = new LinkedNode(); //Base class of hierarchy
		LinkedNode* top = new LinkedNode(); //Top (most parent) class of hierarchy
		std::string name; //Base name, to identify the class
		//Maps every method to the array of hierarchy classes where it occurred
		std::vector<MethodTracker>* methodTrackers = new std::vector<MethodTracker>(); //TODO: Evaluate, what is better, to store it as an array of objects or array of pointers to the objects?
		//Stores the names of each methodTracker in the hierarchy for faster searching
		std::unordered_set<std::string>* methodNames = new std::unordered_set<std::string>; 
		
		~Hierarchy();
		
		//overriding operators for faster comparisons
		bool operator==(const Hierarchy& other);
		bool operator==(const std::string other);
		bool operator!=(const Hierarchy& other);
		bool operator!=(const std::string other);
		
	};
	
	class MethodTracker {
	public:
		std::string methodName;
		int nbOfOccurences; //Tracks the number of occurences for this method in the hierarchy
		std::unordered_set<std::string>* classesOverriden; //Tracks the classes where this method was overriden
		std::map<std::string, int>* class2NbOfTimesOverloaded; //Records how many times is this function overloaded in each class (class --> # of overloads in that class)
		Hierarchy* myHierarchy; //Hierarchy were this method is occurring
		bool isOverloaded; //If the method is overloaded at any point during any class in that hierarchy
		
		MethodTracker(Hierarchy* hierarchy, std::string methodName, std::string className);
		//Add an occurence for this method
		void addOccurence(std::string className);
		
		//Overloading operators for faster comparisons
		bool operator==(const MethodTracker& other);
		bool operator==(const std::string other);
	};
	
	//This struct is the resultant OMRCheckingConsumer::isFoundInHierarchy
	struct HierarchySearchResult {
		//If true, the target node should be the new base of the class hierarchy
		bool changeBase;
		//If true, the target node should be the new top of the class hierarchy
		bool changeTop;
		//If the search was successfull (1) or not (0)
		bool isFound;
		//Index of the hierarchy in the hierarchies vector that needs to be changed
		int index;
	};
	
	class OMRCheckingConsumer : public ASTConsumer {
	public:
		//An array of linked nodes forming the class hierarchy. Every record in this array represents a class hierarchy in OMR
		std::vector<Hierarchy*> hierarchies;
		
		explicit OMRCheckingConsumer(llvm::StringRef filename) { }
		//Search the tips (base and top) of each class hierarchy for the input class name
		//TODO: This is not a very good architecture, the isFoundInHierarchy function is deciding where should the class be, so the naming should be changed to make this function more independant and less related to fillHierarchies
		HierarchySearchResult* isFoundInHierarchy(std::string child, std::string parent);
		//Process the classHierarchy map from ExtensibleClassCheckingVisitor to fill the hierarchies map.
		void fillHierarchies(std::map<std::string, std::string> &map);
		//After finishing the hierarchy, some hierarchies will be broken into 2 sub-hierarchies since the algorithm in fillHierarchies couldn't handle all the corner cases, this method checks for two hierarchies that should be connected and connects them
		void refineHierarchies();
		//Search for the MethodTracker with the inputted function name in the inputted hierarchy
		MethodTracker* searchForTracker(Hierarchy* hierarchy, std::string method);
		//Iterates through the entries of Class2Methods in the ExtensibleClassCheckingVisitor and creates MethodTrackers out of them
		void collectMethodInfo(ExtensibleClassCheckingVisitor &visitor);
		
		//Printining methods to check the results (and debugging sometimes)
		//Print the class hierarchies collected previously, this method works on the hierarchies vector, hence fillHierarchies should be called before it
		void printHierarchy();
		//Iterates through the MethodTrackers in each Hierarchy and prints the information in an organized way
		void printMethodInfo();
		//Prints Class2Methods in ExtensibleClassCheckingVisitor
		void printClass2Method(std::map<std::string, std::vector<std::string>> &map);
		
		virtual void HandleTranslationUnit(ASTContext &Context);
	};
	
	class CheckingAction : public PluginASTAction {
	protected:
		std::unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance &CI, llvm::StringRef filename);
		//Required function -- pure virtual in parent
		bool ParseArgs(const CompilerInstance &CI, const std::vector<std::string>& args);
		//Required function -- pure virtual in parent
		void PrintHelp(llvm::raw_ostream& ros) {}
	};
}