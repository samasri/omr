# Path to OMR main directory
OMR = ../../../
# Path to clang bin (if using Ubuntu, use the clang that is provided by Ubuntu packages, rebuilding clang from source code and running it doesn't work for some reason)
CXX = clang++-5.0
LLVM_CONFIG = llvm-config-5.0

# Get defines and includes for all architectures
include crossCompilationDefines.mk


# Path to shared object file. NOTE: when adding this to plugin always remember to put ./ before the path.
SO = ./plugin.so
# Path to source file of the plugin
CPP = plugin.cpp
# Path to object file (temporary)
O = plugin.o
# Plugin name (in the source code)
PL = omr-statistics
# Variables & rules to test the plugin on OMR files
CC1_MAINARG = -Xclang -load -Xclang $(SO) -Xclang -plugin-arg-$(PL) -Xclang OMR_STAT_PRINT_HIERARCHY -Xclang -plugin-arg-$(PL) -Xclang OMR_STAT_PRINT_OVERLOADS -Xclang -add-plugin -Xclang $(PL)


$(SO): $(CPP) $(CPP:.cpp=.hpp)
	@echo "Building my plugin..."
	@$(CXX) `$(LLVM_CONFIG) --cxxflags` -std=c++0x -Wno-strict-aliasing -c -o $(O) $(CPP) -g
	@$(CXX) -shared `$(LLVM_CONFIG) --ldflags` -o $(SO) $(O)
	@rm $(O)

clean: 
	- rm $(SO)

# Test my plugin on the CodeGenerator classes
sample: $(SO)
	@echo Executing with OMRStatistics...
	@echo "-----------------------------------------"
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/CodeGenOut" $(DEFINES_AMD64) $(PLUGIN_INCLUDES_AMD64) -c $(OMR)/compiler/codegen/OMRCodeGenerator.cpp
#-Xclang -plugin-arg-$(PL) -Xclang "./tests/CodeGenOut"
#Add above between CC1_MAINARG and DEFINES

sample2: $(SO)
	@echo Executing with OMRStatistics...
	@echo "-----------------------------------------"
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/t1" $(DEFINES_AMD64) $(PLUGIN_INCLUDES_AMD64) -c $(OMR)compiler/il/symbol/OMRParameterSymbol.cpp
#@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/t2" $(DEFINES_AMD64) $(PLUGIN_INCLUDES_AMD64) -c $(OMR)compiler/ras/Debug.cpp
	

# Test cases targets
include tests.mk

#Running on all architectures
ARCHS = amd64 i386 p z
OUTPUTS = hierarchy weirdHierarchy allClasses allFunctions overrides functionLocation avg functionCalls

# JIT_OMR_DIRTY_DIR: path to 'compiler' dir starting from where clang is going to compile the files, that is: from OMRStatistics/sources
OMR_DIR ?= /home/sam/omr
JIT_OMR_DIRTY_DIR = $(OMR_DIR)/compiler
JIT_PRODUCT_DIR = $(OMR_DIR)/fvtest/compilertest
JIT_MAKE_DIR = $(JIT_PRODUCT_DIR)/build

# Exporting variables so that other makefiles (trigerred by execute.py in output/lastCreated)
export SO
export CXX
export CC1_MAINARG
export PL
export ARCHS
export JIT_OMR_DIRTY_DIR
export JIT_PRODUCT_DIR
export JIT_MAKE_DIR

produceVisualizations: $(SO)
	@make output/lastCreated --no-print-directory

output/lastCreated: $(SO)
	@for output in $(OUTPUTS) ; do \
		rm -f output/$$output ; \
	done \
	
	@python sources/execute.py amd64
	@python sources/execute.py i386
	@python sources/execute.py p
	@python sources/execute.py z
	
	@touch output/lastCreated
	
	@make copyOriginal
	@make trimOutput
	@make createTotalOutput
	@make moveOutputToVisualization
	
	@mkdir -p output/"original (trimmed) result"
	@mv -f output/amd64.* output/"original (trimmed) result"/
	@mv -f output/i386.* output/"original (trimmed) result"/
	@mv -f output/p.* output/"original (trimmed) result"/
	@mv -f output/z.* output/"original (trimmed) result"/
	
	@python visualization/Hierarchy/makeDot.py
	@dot -Tpdf visualization/Hierarchy/graph.dot -o visualization/Hierarchy/graph.pdf
	
	@mkdir -p output/sql
	@python database/getDatabaseSQL.py sql
	
	@echo "------------Visualizations and Database are ready------------"

copyOriginal:
	@echo "Copying original files..."
	@mkdir -p "output/original (untrimmed) results/"
	@for file in $(ARCHS) ; do \
		for output in $(OUTPUTS) ; do \
			cp output/"$$file".$$output "output/original (untrimmed) results" ; \
		done \
	done

trimOutput:
	@echo "Trimming output..."
	@for file in $(ARCHS) ; do \
		python output/trimAllOutputs.py output/"$$file" ; \
		for output in $(OUTPUTS); do \
			rm output/"$$file".$$output ; \
			mv output/"$$file".$$output.trimmed output/"$$file".$$output ; \
		done \
	done

createTotalOutput:
	@echo "Producing output from all archs..."
	@rm -f hierarchy weirdHierarchy overloads allFunctions overrides
	@for file in $(ARCHS) ; do \
		for output in $(OUTPUTS); do \
			cat output/"$$file".$$output >> output/$$output ; \
			python output/trimOneFile.py output/$$output ; \
			mv output/$$output.trimmed output/$$output ; \
		done \
	done

moveOutputToVisualization:
	@echo "Moving output to the right directory for visualization..."
#@mv output/overloads visualization/Overloads/overloads
	@mv output/overrides visualization/Overrides/overrides
	@mv output/hierarchy visualization/Hierarchy/hierarchy

FILE_TARGET = tests/input/MemberFunc.cpp
FILE_TARGET2 = ../../../compiler/codegen/OMRCodeGenerator.cpp
GENERATE_PIC = 1
getCallGraph:
	@clang++ -std=c++0x -ferror-limit=0 $(DEFINES_AMD64) $(PLUGIN_INCLUDES_AMD64) -S -emit-llvm $(FILE_TARGET2) -o - | opt -analyze -dot-callgraph
	@mv callgraph.dot callGraph/callGraph.dot
ifeq ($(GENERATE_PIC), 1)
	@cat callGraph/callGraph.dot | c++filt | sed 's,>,\\>,g; s,-\\>,->,g; s,<,\\<,g' | gawk '/external node/{id=$$1} $$1 != id' > callGraph/callgraph.dot
	@rm callGraph/callGraph.dot
	@dot -Tpng -ocallGraph/callgraph.png callGraph/callgraph.dot
endif