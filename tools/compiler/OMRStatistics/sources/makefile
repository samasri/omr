#Updating paths
CC1_MAINARG = -Xclang -load -Xclang ../$(SO) -Xclang -plugin-arg-$(PL) -Xclang OMR_STAT_PRINT_HIERARCHY -Xclang -plugin-arg-$(PL) -Xclang OMR_STAT_PRINT_OVERLOADS -Xclang -add-plugin -Xclang $(PL)

OMR = ../../../../
include ../crossCompilationDefines.mk
		
execute: $(SO)
ifeq ($(ARCH), amd64)
	@for file in $(TARGETS) ; do \
		echo "(Arch: AMD64)": Compiling $$file ;\
		$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "../output/amd64"  $(DEFINES_AMD64) $(PLUGIN_INCLUDES_AMD64) -c $$file ;\
	done
endif
ifeq ($(ARCH), i386)
	@for file in $(TARGETS) ; do \
		echo "(Arch: I386)": Compiling $$file ;\
		$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "../output/i386"  $(DEFINES_I386) $(PLUGIN_INCLUDES_I386) -c $$file ;\
	done
endif
ifeq ($(ARCH), p)
	@for file in $(TARGETS) ; do \
		echo "(Arch: Power)": Compiling $$file ;\
		$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "../output/p"  $(DEFINES_P) $(PLUGIN_INCLUDES_P) -c $$file ;\
	done
endif
ifeq ($(ARCH), z)
	@for file in $(TARGETS) ; do \
		echo "(Arch: Z)": Compiling $$file ;\
		$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "../output/z"  $(DEFINES_Z) $(PLUGIN_INCLUDES_Z) -c $$file ;\
	done
endif
	
$(SO):
	make $(SO) -C ../