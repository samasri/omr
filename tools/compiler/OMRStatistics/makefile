# Path to OMR main directory
OMR = ../../../
# Path to clang bin (if using Ubuntu, use the clang that is provided by Ubuntu packages, rebuilding clang from source code and running it doesn't work for some reason)
CXX = clang++-3.8
# Path to compiler that compiles the plugin
GXX = clang++-3.8 #g++
# All defines in one variable
DEFINES = '-D__sync()=' '-D__lwsync()=' '-D__isync()=' -DBITVECTOR_BIT_NUMBERING_MSB -DUT_DIRECT_TRACE_REGISTRATION -DJITTEST -DTEST_PROJECT_SPECIFIC -DTR_HOST_X86 -DTR_HOST_64BIT -DBITVECTOR_64BIT -DLINUX -DTR_TARGET_X86 -DTR_TARGET_64BIT -DSUPPORTS_THREAD_LOCAL -D_LONG_LONG -DJ9HAMMER -DDEBUG
# All includes in one variable
COMPILATION_INCLUDES = -I/home/se-team/Desktop/llvm-clang/3.8-llvm/tools/clang/include/ -I/home/se-team/Desktop/llvm-clang/3.8-build/tools/clang/include/
PLUGIN_INCLUDES = -I $(OMR)/include_core \
-I $(OMR)/fvtest/compilertest/x/amd64 \
-I $(OMR)/fvtest/compilertest/x \
-I $(OMR)/fvtest/compilertest \
-I $(OMR)/fvtest -I $(OMR)/compiler/x/amd64 \
-I $(OMR)/compiler/x \
-I $(OMR)/compiler \
-I $(OMR)/ \
-I $(OMR)/third_party/gtest-1.7.0 \
-I $(OMR)/third_party/gtest-1.7.0/include \
-I $(OMR)/compiler/
# Path to source file whom AST will be parsed by the plugin
SF = $(OMR)/compiler/codegen/OMRCodeGenerator.cpp
# Path to shared object file. NOTE: when adding this to plugin always remember to put ./ before the path. Failing to do so will give you a 'shared object not found' error which will drive you crazy!!
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
	@echo Executing with the new plugin...
	@echo "-----------------------------------------"
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/out" $(DEFINES) $(PLUGIN_INCLUDES) -c $(SF) 


# Run test cases
test: testHierarchy1 testHierarchy2 testHierarchy3 testHierarchy4 testOverride1 testOverride2 testOverload1 testOverload2 testOverrideOverloadMix testOverrideOverloadMix-DifferentNamespaces testControversialCase1 testControversialCase2 testControversialCase3
	 @python tests/diff.py
	 @rm tests/*.hierarchy
	 @rm tests/*.overrides
	 @rm tests/*.overloads

testHierarchy1: $(SO)
	@echo Executing Hierarchy Test 1...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Hierarchy1" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Hierarchy1.cpp


testHierarchy2: $(SO)
	@echo Executing Hierarchy Test 2...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Hierarchy2" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Hierarchy2.cpp

testHierarchy3: $(SO)
	@echo Executing Hierarchy Test 3...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Hierarchy3" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Hierarchy3.cpp
	
testHierarchy4: $(SO)
	@echo Executing Hierarchy Test 4...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Hierarchy4" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Hierarchy4.cpp

testOverride1: $(SO)
	@echo Executing Override Test 1...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Override1" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Override1.cpp

testOverride2: $(SO)
	@echo Executing Override Test 2...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Override2" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Override2.cpp

testOverload1: $(SO)
	@echo Executing Overload Test 1...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Overload1" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Overload1.cpp

testOverload2: $(SO)
	@echo Executing Overload Test 2...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Overload2" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Overload2.cpp

testOverrideOverloadMix: $(SO)
	@echo Executing OverrideOverloadMix Test...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/OverrideOverloadMix" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/OverrideOverloadMix.cpp
	
testOverrideOverloadMix-DifferentNamespaces: $(SO)
	@echo Executing OverrideOverloadMix Test...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/OverrideOverloadMix-DifferentNamespaces" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/OverrideOverloadMix-DifferentNamespaces.cpp
	
testControversialCase1: $(SO)
	@echo Executing Controversial Test Case 1...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/ControversialCase1" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/ControversialCase1.cpp
	
testControversialCase2: $(SO)
	@echo Executing Controversial Test Case 2...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/ControversialCase2" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/ControversialCase2.cpp
	
testControversialCase3: $(SO)
	@echo Executing Controversial Test Case 3...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/ControversialCase3" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/ControversialCase3.cpp

include sources/common.mk

#TODO: define $(HOST_ARCH) & $(TARGET_ARCH)
LIST = $(JIT_PRODUCT_BACKEND_SOURCES) $(JIT_PRODUCT_SOURCE_FILES) 

targets = $(addprefix , $(LIST))
writeCSV: $(targets)
	python trim.py
	mv csvTrimmed csv

$(targets):
	@echo "Compiling $@"
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) $(DEFINES) $(PLUGIN_INCLUDES) -c $@ >> csv
