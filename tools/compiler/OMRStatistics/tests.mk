#Includes all test cases targets
test: produceVisualizations testHierarchy1 testHierarchy2 testHierarchy3 testHierarchy4 testHierarchy5 testHierarchy6 testTemplates testNestedClasses testOverride1 testOverride2 testOverride3 testOverride4 testOverload1 testOverload2 testOverload3 testOverload4 testOverrideOverloadMix testOverrideOverloadMix-DifferentNamespaces testControversialCase1 testControversialCase2 testControversialCase3 testNoNamespace testVirtualImplicit
	@python tests/tests.py output/amd64.overrides
	@rm tests/*.hierarchy
	@rm tests/*.overrides
	@rm tests/*.overloads

testHierarchy1: $(SO)
	@echo Executing Hierarchy Test 1...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Hierarchy1" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Hierarchy1.cpp


testHierarchy2: $(SO)
	@echo Executing Hierarchy Test 2...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Hierarchy2" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Hierarchy2.cpp

testHierarchy3: $(SO)
	@echo Executing Hierarchy Test 3...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Hierarchy3" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Hierarchy3.cpp
	
testHierarchy4: $(SO)
	@echo Executing Hierarchy Test 4...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Hierarchy4" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Hierarchy4.cpp
	
testHierarchy5: $(SO)
	@echo Executing Hierarchy Test 5...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Hierarchy5" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Hierarchy5.cpp
	
testHierarchy6: $(SO)
	@echo Executing Hierarchy Test 6...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Hierarchy6" $(DEFINES) $(PLUGIN_INCLUDES) -c "tests/input/Hierarchy6 - Multiple Parents.cpp"
	
testTemplates: $(SO)
	@echo Executing Template Test...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Templates" $(DEFINES) $(PLUGIN_INCLUDES) -c "tests/input/Templates.cpp"
	
testNestedClasses: $(SO)
	@echo Executing Nested Classes Test...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/NestedClasses" $(DEFINES) $(PLUGIN_INCLUDES) -c "tests/input/NestedClasses.cpp"

testOverride1: $(SO)
	@echo Executing Override Test 1...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Override1" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Override1.cpp

testOverride2: $(SO)
	@echo Executing Override Test 2...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Override2" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Override2.cpp

testOverride3: $(SO)
	@echo Executing Override Test 3...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Override3" $(DEFINES) $(PLUGIN_INCLUDES) -c "tests/input/Override3 - Multiple Parents.cpp"

testOverride4: $(SO)
	@echo Executing Override Test 4...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Override4" $(DEFINES) $(PLUGIN_INCLUDES) -c "tests/input/Override4 - Multiple Parents2.cpp"

testOverload1: $(SO)
	@echo Executing Overload Test 1...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Overload1" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Overload1.cpp

testOverload2: $(SO)
	@echo Executing Overload Test 2...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Overload2" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Overload2.cpp

testOverload3: $(SO)
	@echo Executing Overload Test 3...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Overload3" $(DEFINES) $(PLUGIN_INCLUDES) -c "tests/input/Overload3 - Multiple Parents.cpp"

testOverload4: $(SO)
	@echo Executing Overload Test 4...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Overload4" $(DEFINES) $(PLUGIN_INCLUDES) -c "tests/input/Overload4 - Multiple Parents2.cpp"

testOverrideOverloadMix: $(SO)
	@echo Executing OverrideOverloadMix Test...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/OverrideOverloadMix" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/OverrideOverloadMix.cpp
	
testOverrideOverloadMix-DifferentNamespaces: $(SO)
	@echo Executing OverrideOverloadMix Test...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/OverrideOverloadMix-DifferentNamespaces" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/OverrideOverloadMix-DifferentNamespaces.cpp
	
testControversialCase1: $(SO)
	@echo Executing Controversial Test Case 1...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/ControversialCase1" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/ControversialCase1.cpp
	
testControversialCase2: $(SO)
	@echo Executing Controversial Test Case 2...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/ControversialCase2" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/ControversialCase2.cpp
	
testControversialCase3: $(SO)
	@echo Executing Controversial Test Case 3...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/ControversialCase3" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/ControversialCase3.cpp

testNoNamespace: $(SO)
	@echo Executing No Namespace Test...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/NoNamespace" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/NoNamespace.cpp

testVirtualImplicit: $(SO)
	@echo Executing Virtual and Implicit Functions Test...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Virtual+Implicit" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Virtual+Implicit.cpp