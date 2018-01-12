#Includes all test cases targets
test: testHierarchy1 testHierarchy2 testHierarchy3 testHierarchy4 testOverride1 testOverride2 testOverload1 testOverload2 testOverrideOverloadMix testOverrideOverloadMix-DifferentNamespaces testControversialCase1 testControversialCase2 testControversialCase3 testNoNamespace
	 @python tests/diff.py
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

testOverride1: $(SO)
	@echo Executing Override Test 1...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Override1" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Override1.cpp

testOverride2: $(SO)
	@echo Executing Override Test 2...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Override2" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Override2.cpp

testOverload1: $(SO)
	@echo Executing Overload Test 1...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Overload1" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Overload1.cpp

testOverload2: $(SO)
	@echo Executing Overload Test 2...
	@$(CXX) -std=c++0x -w -fsyntax-only -ferror-limit=0 $(CC1_MAINARG) -Xclang -plugin-arg-$(PL) -Xclang "./tests/Overload2" $(DEFINES) $(PLUGIN_INCLUDES) -c tests/input/Overload2.cpp

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