#Updating paths
CC1_MAINARG = -Xclang -load -Xclang ../$(SO) -Xclang -plugin-arg-$(PL) -Xclang OMR_STAT_PRINT_HIERARCHY -Xclang -plugin-arg-$(PL) -Xclang OMR_STAT_PRINT_OVERLOADS -Xclang -add-plugin -Xclang $(PL)
LINTER_FLAGS = -std=c++0x -w -fsyntax-only -ferror-limit=0 $(LINTER_FLAGS_EXTRA)

OMR = ../../../../
include ../crossCompilationDefines.mk

# Includes and defines are generated differently between omr and openJ9
ifdef J9SRC
INCLUDES = $(patsubst %,-I'%',$(CXX_INCLUDES))
DEFINES = $(patsubst %,-D%,$(CXX_DEFINES))

else

ifeq ($(ARCH), amd64)
INCLUDES = $(PLUGIN_INCLUDES_AMD64)
DEFINES = $(DEFINES_AMD64)
endif
ifeq ($(ARCH), i386)
INCLUDES = $(PLUGIN_INCLUDES_I386)
DEFINES = $(DEFINES_I386)
endif
ifeq ($(ARCH), p)
INCLUDES = $(PLUGIN_INCLUDES_P)
DEFINES = $(DEFINES_P)
endif
ifeq ($(ARCH), z)
INCLUDES = $(PLUGIN_INCLUDES_Z)
DEFINES = $(DEFINES_Z)
endif

endif

execute: $(SO)
ifeq ($(ARCH), amd64)
	@for file in $(TARGETS) ; do \
		echo "(Arch: AMD64)": Compiling $$file ;\
		$(CXX) $(LINTER_FLAGS) $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "../output/amd64"  $(DEFINES) $(INCLUDES) -c $$file ;\
	done
endif
ifeq ($(ARCH), i386)
	@for file in $(TARGETS) ; do \
		echo "(Arch: I386)": Compiling $$file ;\
		$(CXX) $(LINTER_FLAGS) $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "../output/i386"  $(DEFINES) $(INCLUDES) -c $$file ;\
	done
endif
ifeq ($(ARCH), p)
	@for file in $(TARGETS) ; do \
		echo "(Arch: Power)": Compiling $$file ;\
		$(CXX) $(LINTER_FLAGS) $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "../output/p"  $(DEFINES) $(INCLUDES) -c $$file ;\
	done
endif
ifeq ($(ARCH), z)
	@for file in $(TARGETS) ; do \
		echo "(Arch: Z)": Compiling $$file ;\
		$(CXX) $(LINTER_FLAGS) $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "../output/z"  $(DEFINES) $(INCLUDES) -c $$file ;\
	done
endif
	
$(SO):
	make $(SO) -C ../