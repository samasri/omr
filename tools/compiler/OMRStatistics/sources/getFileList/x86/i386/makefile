#I386 includes

HOST_ARCH = x
TARGET_ARCH = i386

include $(JIT_MAKE_DIR)/files/common.mk
LIST = $(JIT_PRODUCT_BACKEND_SOURCES) $(JIT_PRODUCT_SOURCE_FILES) 
TARGETS = $(addprefix , $(LIST))
export TARGETS

default:
	make -C ../../../