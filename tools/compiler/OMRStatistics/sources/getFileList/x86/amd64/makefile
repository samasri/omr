#AMD64 includes

# JIT_OMR_DIRTY_DIR: path to 'compiler' dir starting from where clang is going to compile the files, that is: from OMRStatistics/sources
HOST_ARCH = x
TARGET_ARCH = amd64

include $(JIT_MAKE_DIR)/files/common.mk
LIST = $(JIT_PRODUCT_BACKEND_SOURCES) $(JIT_PRODUCT_SOURCE_FILES) 

ifdef FIXED_SRCBASE
TARGETS = $(addprefix $(FIXED_SRCBASE)/, $(LIST))
endif
ifndef FIXED_SRCBASE
TARGETS = $(addprefix , $(LIST))
endif

export TARGETS

default:
	@echo "test"
	@echo $(JIT_MAKE_DIR)
	make -C ../../../