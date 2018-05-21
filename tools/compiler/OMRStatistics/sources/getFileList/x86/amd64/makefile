#AMD64 includes

# JIT_OMR_DIRTY_DIR: path to 'compiler' dir starting from where clang is going to compile the files, that is: from OMRStatistics/sources
JIT_MAKE_DIR = ../../../$(JIT_PRODUCT_DIR)/build
HOST_ARCH = x
TARGET_ARCH = amd64

include ../../../$(JIT_PRODUCT_DIR)/build/files/common.mk
LIST = $(JIT_PRODUCT_BACKEND_SOURCES) $(JIT_PRODUCT_SOURCE_FILES) 
TARGETS = $(addprefix , $(LIST))
export TARGETS

default:
	make -C ../../../