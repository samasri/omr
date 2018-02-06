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
-I $(OMR)/fvtest \
-I $(OMR)/compiler/x/amd64 \
-I $(OMR)/compiler/x \
-I $(OMR)/compiler \
-I $(OMR)/ \
-I $(OMR)/third_party/gtest-1.7.0 \
-I $(OMR)/third_party/gtest-1.7.0/include \
-I $(OMR)/compiler/

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
	@echo Executing with OMRStatistics...
	@echo "-----------------------------------------"
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) $(DEFINES) $(PLUGIN_INCLUDES) -c $(OMR)/compiler/codegen/OMRCodeGenerator.cpp
	#-Xclang -plugin-arg-$(PL) -Xclang "./tests/CodeGenOut"
	#Add above between CC1_MAINARG and DEFINES

sample2: $(SO)
	@echo Executing with OMRStatistics...
	@echo "-----------------------------------------"
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./i386CodeGenOut" $(DEFINES) $(PLUGIN_INCLUDES) -c $(OMR)/compiler/x/i386/codegen/OMRCodeGenerator.cpp

# Run test cases
include tests.mk

#Running on different architectures
include crossCompilationDefines.mk

include sources/common_amd64.mk
include sources/common_i386.mk
include sources/common_p.mk
include sources/common_z.mk
include sources/common_arm.mk

LIST_AMD64 = $(JIT_PRODUCT_BACKEND_SOURCES_AMD64) $(JIT_PRODUCT_SOURCE_FILES_AMD64) 
LIST_I386 = $(JIT_PRODUCT_BACKEND_SOURCES_I386) $(JIT_PRODUCT_SOURCE_FILES_I386) 
LIST_P = $(JIT_PRODUCT_BACKEND_SOURCES_P) $(JIT_PRODUCT_SOURCE_FILES_P) 
LIST_Z = $(JIT_PRODUCT_BACKEND_SOURCES_Z) $(JIT_PRODUCT_SOURCE_FILES_Z) 
LIST_ARM = $(JIT_PRODUCT_BACKEND_SOURCES_P) $(JIT_PRODUCT_SOURCE_FILES_ARM) 

targets_amd64 = $(addprefix , $(LIST_AMD64))
targets_i386 = $(addprefix , $(LIST_I386))
targets_p = $(addprefix , $(LIST_P))
targets_z = $(addprefix , $(LIST_Z))
targets_arm = $(addprefix , $(LIST_ARM))

writeCSV: $(SO)
	@make output/lastCreated

output/lastCreated: $(SO)
	@rm -f output/z.*
	@make executeAllClasses
	@touch output/lastCreated
	@echo "Done"

executeAllClasses: $(SO) $(targets_z)

$(targets_z):
	@echo "Compiling $@"
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "output/z"  $(DEFINES_Z) $(PLUGIN_INCLUDES_Z) -c $@