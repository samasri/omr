# Path to OMR main directory
OMR = ../../../
# Path to clang bin (if using Ubuntu, use the clang that is provided by Ubuntu packages, rebuilding clang from source code and running it doesn't work for some reason)
CXX = clang++
# Path to compiler that compiles the plugin
GXX = g++
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
CC1_MAINARG = -Xclang -load -Xclang $(SO) -Xclang -add-plugin -Xclang $(PL)

# Test my plugin on the CodeGenerator classes
default: $(SO)
	@echo Executing with the new plugin...
	@echo "-----------------------------------------"
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) $(DEFINES) $(PLUGIN_INCLUDES) -c $(SF) 

$(SO): $(CPP) $(CPP:.cpp=.hpp)
	@echo "Building my plugin..."
	@$(GXX) `llvm-config --cxxflags` -std=c++0x -Wno-strict-aliasing -c -o $(O) $(CPP) $(COMPILATION_INCLUDES) -g
	@$(GXX) -shared `llvm-config --ldflags` -o $(SO) $(O)
	@rm $(O)

# Run test cases
test: tests/Test.class test1 test2 test3 test4 test5
	@java -cp tests Test

tests/Test.class: tests/Test.java
	@javac tests/Test.java

test1: $(SO)
	@echo Executing Test 1...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) $(DEFINES) $(PLUGIN_INCLUDES) -c tests/test1.cpp > tests/test1.out


test2: $(SO)
	@echo Executing Test 2...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) $(DEFINES) $(PLUGIN_INCLUDES) -c tests/test2.cpp > tests/test2.out

test3: $(SO)
	@echo Executing Test 3...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) $(DEFINES) $(PLUGIN_INCLUDES) -c tests/test3.cpp > tests/test3.out

test4: $(SO)
	@echo Executing Test 4...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) $(DEFINES) $(PLUGIN_INCLUDES) -c tests/test4.cpp > tests/test4.out

test5: $(SO)
	@echo Executing Test 5...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) $(DEFINES) $(PLUGIN_INCLUDES) -c tests/test5.cpp > tests/test5.out