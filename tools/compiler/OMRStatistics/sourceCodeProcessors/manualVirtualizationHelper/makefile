export OMR_PATH = /home/sam/1omr-virtualization/
export OPENJ9_PATH = /home/sam/2openj9-virtualization/runtime/ 
PATH_TO_DB_QUERY = /home/sam/test/manualVirtualizationHelper/db
TARGET_CLASS = 'Compilation'
COMPILER_SUBCOMPONENT = 'compile'

# Make silent by default (no log of entering other makefiles)
ifndef VERBOSE
.SILENT:
endif

default: generateList omr openj9 processSearchResults

generateList:
	@echo "Producing list of signatures from database query..."
	@python produceLists.py $(PATH_TO_DB_QUERY) $(TARGET_CLASS)

omr: generateList
	make -f search.mk omr

openj9: generateList
	make -f search.mk openj9

processSearchResults:
	@echo "Editing source code (Removing self()) of OMR"
	@python processSearchResult.py $(OMR_PATH) $(OPENJ9_PATH) $(COMPILER_SUBCOMPONENT) $(TARGET_CLASS)