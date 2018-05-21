#I386 includes

JIT_MAKE_DIR = ../../../$(JIT_PRODUCT_DIR)/build
HOST_ARCH = x
TARGET_ARCH = i386

include ../../../$(JIT_PRODUCT_DIR)/build/files/common.mk
LIST = $(JIT_PRODUCT_BACKEND_SOURCES) $(JIT_PRODUCT_SOURCE_FILES) 
TARGETS = $(addprefix , $(LIST))
export TARGETS

default:
	make -C ../../../