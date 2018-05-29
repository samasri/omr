#I386 includes

HOST_ARCH = x
HOST_SUBARCH = amd64
TARGET_ARCH = x
TARGET_SUBARCH = i386
export TARGET_BITS = 32

include $(JIT_MAKE_DIR)/files/common.mk
LIST = $(JIT_PRODUCT_BACKEND_SOURCES) $(JIT_PRODUCT_SOURCE_FILES) 

ifdef FIXED_SRCBASE
TARGETS = $(addprefix $(FIXED_SRCBASE)/, $(LIST))
endif
ifndef FIXED_SRCBASE
TARGETS = $(addprefix , $(LIST))
endif

export TARGETS

ifdef J9SRC
include $(JIT_MAKE_DIR)/toolcfg/common.mk

export CXX_DEFINES
export CXX_INCLUDES
endif

default:
	make -C ../../../