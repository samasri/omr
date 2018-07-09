include list

default:
	@echo "No default target for this make, please specify the right target"

omr :
	@echo "Searching the OMR source code for self() calls..."
	@for sig in $(LIST) ; do \
		echo $$sig: ; \
		grep -r $$sig $(OMR_PATH); \
		echo -------------------- ; \
	done

openj9 :
	@echo "Searching the OpenJ9 source code for self() calls..."
	@ for sig in $(LIST) ; do \
		echo $$sig: ; \
		grep -r $$sig $(OPENJ9_PATH); \
		echo -------------------- ; \
	done