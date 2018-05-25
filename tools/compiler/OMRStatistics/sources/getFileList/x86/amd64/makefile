#AMD64 includes

HOST_ARCH = x
HOST_SUBARCH = amd64
TARGET_ARCH = x
TARGET_SUBARCH = amd64

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