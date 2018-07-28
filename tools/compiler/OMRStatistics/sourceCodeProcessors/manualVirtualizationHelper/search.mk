include list

default:
	@echo "No default target for this make, please specify the right target"

omr:
	@rm -f results.omr
	@echo "Searching the OMR source code for self() calls..."
	@for sig in $(LIST) ; do \
		echo $$sig: >> results.omr ;\
		grep -r $$sig $(OMR_PATH) >> results.omr ;\
		echo --------------------  >> results.omr ;\
	done

openj9:
	@rm -f results.openj9
	@echo "Searching the OpenJ9 source code for self() calls..."
	@ for sig in $(LIST) ; do \
		echo $$sig:  >> results.openj9 ;\
		grep -r $$sig $(OPENJ9_PATH) >> results.openj9 ;\
		echo --------------------  >> results.openj9 ;\
	done