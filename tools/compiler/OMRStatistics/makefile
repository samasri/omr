# Path to OMR main directory
OMR = ../../../
# Path to clang bin (if using Ubuntu, use the clang that is provided by Ubuntu packages, rebuilding clang from source code and running it doesn't work for some reason)
CXX = clang++-3.8
# Path to compiler that compiles the plugin
GXX = clang++-3.8

# Get defines and includes for all architectures
include crossCompilationDefines.mk
COMPILATION_INCLUDES = -I/home/se-team/Desktop/llvm-clang/3.8-llvm/tools/clang/include/ -I/home/se-team/Desktop/llvm-clang/3.8-build/tools/clang/include/

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
	@$(GXX) `llvm-config-3.8 --cxxflags` -std=c++0x -Wno-strict-aliasing -c -o $(O) $(CPP) $(COMPILATION_INCLUDES) -g
	@$(GXX) -shared `llvm-config-3.8 --ldflags` -o $(SO) $(O)
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
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/BitVecAnalOut" $(DEFINES_AMD64) $(PLUGIN_INCLUDES_AMD64) -c $(OMR)/compiler/optimizer/BitVectorAnalysis.cpp
	

# Test cases targets
include tests.mk

#Running on all architectures
ARCHS = amd64 i386 p z
OUTPUTS = hierarchy weirdHierarchy allClasses overloads allFunctions overrides functionLocation avg

# JIT_OMR_DIRTY_DIR: path to 'compiler' dir starting from where clang is going to compile the files, that is: from OMRStatistics/sources
JIT_OMR_DIRTY_DIR = ../../../../compiler
JIT_PRODUCT_DIR = ../../../../fvtest/compilertest

# Exporting variables so that other makefiles (trigerred by execute.py in output/lastCreated)
export SO
export CXX
export CC1_MAINARG
export PL
export ARCHS
export JIT_OMR_DIRTY_DIR
export JIT_PRODUCT_DIR

produceVisualizations: $(SO)
	@make output/lastCreated --no-print-directory

output/lastCreated: $(SO)
	@rm -f output/amd64.*
	@rm -f output/i386.*
	@rm -f output/p.*
	@rm -f output/z.*
	@rm -f output/allFunctions
	@rm -f output/allClasses
	@rm -f output/weirdHierarchy
	@rm -f output/sanityCheck
	@rm -f output/functionLocation
	
	@python sources/execute.py amd64
	@python sources/execute.py i386
	@python sources/execute.py p
	@python sources/execute.py z
	
	@make copyOriginal
	@make trimOutput
	@make createTotalOutput
	@make moveOutputToVisualization
	
	@python visualization/Overloads/makeHTML.py visualization/Overloads/overloads
	@python visualization/Hierarchy/makeDot.py
	@dot -Tpdf visualization/Hierarchy/graph.dot -o visualization/Hierarchy/graph.pdf
	
	@touch output/lastCreated
	@echo "------------Visualizations are ready------------"

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
	@python output/sanityCheck.py output > output/sanityCheck
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
	@mv output/overloads visualization/Overloads/overloads
	@mv output/overrides visualization/Overrides/overrides
	@mv output/hierarchy visualization/Hierarchy/hierarchy

executeAMD64: $(SO)
	@for file in $(TARGETS_AMD64) ; do \
	echo "(Arch: amd64)": Compiling $$file; \
	$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "output/amd64"  $(DEFINES_AMD64) $(PLUGIN_INCLUDES_AMD64) -c $$file ;\
	done

executeI386: $(SO)
	@for file in $(TARGETS_I386) ; do \
	echo "(Arch: i386)": Compiling $$file; \
	$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "output/i386"  $(DEFINES_I386) $(PLUGIN_INCLUDES_I386) -c $$file ;\
	done

executeP: $(SO)
	@for file in $(TARGETS_P) ; do \
	echo "(Arch: Power)": Compiling $$file; \
	$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "output/p"  $(DEFINES_P) $(PLUGIN_INCLUDES_P) -c $$file ;\
	done

executeZ: $(SO)
	@for file in $(TARGETS_Z) ; do \
	echo "(Arch: Z)": Compiling $$file; \
	$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "output/z"  $(DEFINES_Z) $(PLUGIN_INCLUDES_Z) -c $$file ;\
	done