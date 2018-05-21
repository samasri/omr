#Z includes

# JIT_OMR_DIRTY_DIR and JIT_RPODUCT_DIR: path to 'compiler' dir starting from where clang is going to compile the files, that is: from OMRStatistics/sources
JIT_MAKE_DIR = ../../../../../../fvtest/compilertest/build
HOST_ARCH = z
TARGET_ARCH = z

include ../../$(JIT_PRODUCT_DIR)/build/files/common.mk
LIST = $(JIT_PRODUCT_BACKEND_SOURCES) $(JIT_PRODUCT_SOURCE_FILES) 
TARGETS = $(addprefix , $(LIST))
export TARGETS


default:
	make -C ../../