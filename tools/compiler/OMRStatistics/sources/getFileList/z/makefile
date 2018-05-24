#Z includes

# JIT_OMR_DIRTY_DIR and JIT_RPODUCT_DIR: path to 'compiler' dir starting from where clang is going to compile the files, that is: from OMRStatistics/sources
HOST_ARCH = z
TARGET_ARCH = z

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
	make -C ../../