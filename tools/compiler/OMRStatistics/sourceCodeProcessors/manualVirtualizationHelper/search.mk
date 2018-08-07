include list
# 'list' above should become functions-searchForCalls

default:
	@echo "No default target for this make, please specify the right target"

omr:
	@rm -f callResults.omr defResults.omr
	@echo "Searching the OMR source code for self() calls..."
	@for sig in $(CALLS_LIST) ; do \
		echo $$sig: >> callResults.omr ;\
		grep -r $$sig $(OMR_PATH) >> callResults.omr ;\
		echo --------------------  >> callResults.omr ;\
	done
	@for sig in $(DEFS_LIST) ; do \
		echo $$sig: >> defResults.omr ;\
		grep -r "$$sig" $(OMR_PATH) >> defResults.omr ;\
		echo --------------------  >> defResults.omr ;\
	done

openj9:
	@rm -f callResults.openj9 defResults.openj9
	@echo "Searching the OpenJ9 source code for self() calls..."
	@ for sig in $(CALLS_LIST) ; do \
		echo $$sig:  >> callResults.openj9 ;\
		grep -r $$sig $(OPENJ9_PATH) >> callResults.openj9 ;\
		echo --------------------  >> callResults.openj9 ;\
	done
	@ for sig in $(DEFS_LIST) ; do \
		echo $$sig:  >> defResults.openj9 ;\
		grep -r "$$sig" $(OPENJ9_PATH) >> defResults.openj9 ;\
		echo --------------------  >> defResults.openj9 ;\
	done