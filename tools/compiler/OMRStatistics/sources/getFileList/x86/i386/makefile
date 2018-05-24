#I386 includes

HOST_ARCH = x
TARGET_ARCH = i386

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
	make -C ../../../