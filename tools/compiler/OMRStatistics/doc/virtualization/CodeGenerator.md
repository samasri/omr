# Overridden Functions
1. emitDataSnippets()
2. yankIndexScalingOp()
3. apply16BitLabelRelativeRelocation(int32_t *,TR::LabelSymbol *)
4. getSupportsBitOpCodes()
5. supportsMergingGuards()
6. alwaysGeneratesAKnownCleanSign(TR::Node *)
7. generateSwitchToInterpreterPrePrologue(TR::Instruction *,uint8_t,uint8_t)
8. supportsNegativeFusedMultiplyAdd()
9. hasComplexAddressingMode()
10. allocateRecompilationInfo()
11. createLinkageForCompilation()
12. jitAddPicToPatchOnClassUnload(void *,void *)
13. beginInstructionSelection()
14. getMinimumNumberOfNodesBetweenMonitorsForTLE()
15. reserveNTrampolines(int32_t)
16. pickRegister(class TR_RegisterCandidate *,TR::Block **,class TR_BitVector &,TR_GlobalRegisterNumber &,TR_LinkHead *)
17. isFenceInstruction(TR::Instruction *)
18. getMinShortForLongCompareNarrower()
19. lowerTreesPropagateBlockToNode(TR::Node *)
20. processInstruction(TR::Instruction *,class TR_BitVector **,int32_t &,int32_t &,_Bool)
21. getLinkageGlobalRegisterNumber(int8_t,TR::DataType)
22. needToAvoidCommoningInGRA()
23. materializesHeapBase()
24. hasTMEvaluator()
25. getMaximumNumbersOfAssignableFPRs()
26. generateDebugCounterBump(TR::Instruction *,TR::DebugCounterBase *,TR::Register *,TR::RegisterDependencyConditions *)
27. getSupportsConstantOffsetInAddressing(int64_t)
28. incRefCountForOpaquePseudoRegister(TR::Node *,TR::CodeGenerator *,TR::Compilation *)
29. shouldYankCompressedRefs()
30. canTransformUnsafeSetMemory()
31. processIncomingParameterUsage(class TR_BitVector **,int32_t)
32. supportsUnneededLabelRemoval()
33. canUseImmedInstruction(int64_t)
34. apply16BitLoadLabelRelativeRelocation(TR::Instruction *,TR::LabelSymbol *,TR::LabelSymbol *,int32_t)
35. doRematerialization()
36. hasDataSnippets()
37. addProjectSpecializedPairRelocation(uint8_t *,uint8_t *,uint8_t *,TR_ExternalRelocationTargetKind,char *,uintptr_t,TR::Node *)
38. generateDebugCounterBump(TR::Instruction *,TR::DebugCounterBase *,int32_t,class TR_ScratchRegisterManager &)
39. isTargetSnippetOrOutOfLine(TR::Instruction *,TR::Instruction **,TR::Instruction **)
40. enableAESInHardwareTransformations()
41. canBeAffectedByStoreTagStalls()
42. generateDebugCounterBump(TR::Instruction *,TR::DebugCounterBase *,int32_t,TR::RegisterDependencyConditions *)
43. removeUnavailableRegisters(class TR_RegisterCandidate *,TR::Block **,class TR_BitVector &)
44. needsNormalizationBeforeShifts()
45. suppressInliningOfRecognizedMethod(TR::RecognizedMethod)
46. nodeMayCauseException(TR::Node *)
47. createStackAtlas()
48. codegenSupportsLoadlessBNDCheck()
49. branchesAreExpensive()
50. emitTargetAddressSnippets()
51. allowGlobalRegisterAcrossBranch(class TR_RegisterCandidate *,TR::Node *)
52. needRelocationsForStatics()
53. supportsInliningOfIsInstance()
54. supportsHighWordFacility()
55. isRotateAndMask(TR::Node *)
56. getSupportsTenuredObjectAlignment()
57. arrayInitMinimumNumberOfBytes()
58. isPreservedRegister(int32_t)
59. canFoldLargeOffsetInAddressing()
60. createLinkage(enum TR_LinkageConventions)
61. getInternalPtrMapBit()
62. prepareForGRA()
63. buildInterpreterEntryPoint()
64. isAddressScaleIndexSupported(int32_t)
65. constLoadNeedsLiteralFromPool(TR::Node *)
66. lowerTreesPostTreeTopVisit(TR::TreeTop *,vcount_t)
67. opCodeIsNoOpOnThisPlatform(TR::ILOpCode &)
68. arithmeticNeedsLiteralFromPool(TR::Node *)
69. shouldValueBeInACommonedNode(int64_t)
70. getMaximumNumberOfFPRsAllowedAcrossEdge(TR::Node *)
71. arrayTranslateTableRequiresAlignment(_Bool,_Bool)
72. isObjectOfSizeWorthAligning(uint32_t)
73. supports32bitAiadd()
74. propagateSignThroughBCDLeftShift(TR::DataType)
75. alwaysGeneratesAKnownPositiveCleanSign(TR::Node *)
76. getMaximumNumbersOfAssignableVRs()
77. mulDecompositionCostIsJustified(int,char [],char [],int64_t)
78. getRegisterMapInfoBitsMask()
79. supportsLengthMinusOneForMemoryOpts()
80. supportsDebugCounters(TR::DebugCounterInjectionPoint)
81. excludeInvariantsFromGRAEnabled()
82. apply32BitLabelTableRelocation(int32_t *,TR::LabelSymbol *)
83. jitAddUnresolvedAddressMaterializationToPatchOnClassRedefinition(void *)
84. getSizeOfCombinedBuffer()
85. splitBlockEntry(TR::Instruction *)
86. getMaximumNumberOfGPRsAllowedAcrossEdge(TR::Block *)
87. needClassAndMethodPointerRelocations()
88. inlineDirectCall(TR::Node *,TR::Register *&)
89. createHWPRecords()
90. isBranchInstruction(TR::Instruction *)
91. doInstructionSelection()
92. apply24BitLabelRelativeRelocation(int32_t *,TR::LabelSymbol *)
93. getSupportsNewObjectAlignment()
94. generateDebugCounterBump(TR::Instruction *,TR::DebugCounterBase *,TR::Register *,class TR_ScratchRegisterManager &)
95. preLowerTrees()
96. apply32BitLabelRelativeRelocation(int32_t *,TR::LabelSymbol *)
97. computeRegisterSaveDescription(class TR_BitVector *,_Bool)
98. startInternalControlFlow(TR::Instruction *)
99. allowSplitWarmAndColdBlocks()
100. registerAssumptions()
101. updateSnippetMapWithRSD(TR::Instruction *,int32_t)
102. prepareRegistersForAssignment()
103. getMinByteForLongCompareNarrower()
104. nopsAlsoProcessedByRelocations()
105. setNextAvailableBlockIndex(int32_t)
106. lowerTreesPreTreeTopVisit(TR::TreeTop *,vcount_t)
107. lowerTreeIfNeeded(TR::Node *,int32_t,TR::Node *,TR::TreeTop *)
108. processRelocations()
109. estimateBinaryLength(TR::MemoryReference *)
110. IsInMemoryType(TR::DataType)
111. setOnDemandLiteralPoolRun(_Bool)
112. codegenMulDecomposition(int64_t)
113. wantToPatchClassPointer(const class TR_OpaqueClassBlock *,const uint8_t *)
114. getSupportsOpCodeForAutoSIMD(TR::ILOpCode,TR::DataType)
115. hasTargetAddressSnippets()
116. getMaximumNumbersOfAssignableGPRs()
117. getPreferredLoopUnrollFactor()
118. lowerTreesPostChildrenVisit(TR::Node *,TR::TreeTop *,vcount_t)
119. endInternalControlFlow(TR::Instruction *)
120. generateBinaryEncodingPrologue(struct TR_PPCBinaryEncodingData *)
121. apply16BitLabelRelativeRelocation(int32_t *,TR::LabelSymbol *,int8_t,_Bool)
122. isInternalControlFlowReg(TR::Register *)
123. setVMThreadRequired(_Bool)
124. generateNop(TR::Node *,TR::Instruction *,enum TR_NOPKind)
125. arrayTranslateMinimumNumberOfElements(_Bool,_Bool)
126. setUnavailableRegistersUsage(TR_Array &,TR_Array &)
127. isLabelInstruction(TR::Instruction *)
128. getNextAvailableBlockIndex()
129. mustGenerateSwitchToInterpreterPrePrologue()
130. dumpTargetAddressSnippets(TR::FILE *)
131. considerTypeForGRA(TR::SymbolReference *)
132. jitAdd32BitPicToPatchOnClassUnload(void *,void *)
133. isAlignmentInstruction(TR::Instruction *)
134. apply12BitLabelRelativeRelocation(int32_t *,TR::LabelSymbol *,_Bool)
135. getGlobalFPRsPreservedAcrossCalls()
136. isReturnInstruction(TR::Instruction *)
137. allowGuardMerging()
138. canNullChkBeImplicit(TR::Node *)
139. isLiteralPoolOnDemandOn()
140. supportsDirectIntegralLoadStoresFromLiteralPool()
141. splitEdge(TR::Instruction *,_Bool,_Bool,TR::Instruction *,TR::list<TR::Instruction *> *,_Bool)
142. supportsDirectJNICallsForAOT()
143. canTransformUnsafeCopyToArrayCopy()
144. CodeGenerator()
145. supportsSinglePrecisionSQRT()
146. usesImplicit64BitGPRs(TR::Node *)
147. setEstimatedLocationsForDataSnippetLabels(int32_t)
148. setCurrentBlockIndex(int32_t)
149. supportsPassThroughCopyToNewVirtualRegister()
150. arrayTranslateAndTestMinimumNumberOfIterations()
151. bitwiseOpNeedsLiteralFromPool(TR::Node *,TR::Node *)
152. ilOpCodeIsSupported(TR::ILOpCodes)
153. wantToPatchClassPointer(const class TR_OpaqueClassBlock *,const TR::Node *)
154. materializesLargeConstants()
155. addProjectSpecializedRelocation(uint8_t *,uint8_t *,uint8_t *,TR_ExternalRelocationTargetKind,char *,uintptr_t,TR::Node *)
156. jitAddPicToPatchOnClassRedefinition(void *,void *,_Bool)
157. internalPointerSupportImplemented()
158. generateCatchBlockBBStartPrologue(TR::Node *,TR::Instruction *)
159. getMaximumNumberOfGPRsAllowedAcrossEdge(TR::Node *)
160. doRegisterAssignment(enum TR_RegisterKinds)
161. getGlobalHPRFromGPR(TR_GlobalRegisterNumber)
162. lowerTreesPreChildrenVisit(TR::Node *,TR::TreeTop *,vcount_t)
163. getCurrentBlockIndex()
164. jitAdd32BitPicToPatchOnClassRedefinition(void *,void *,_Bool)
165. isGlobalRegisterAvailable(TR_GlobalRegisterNumber,TR::DataType)
166. supportsTrapsInTMRegion()
167. supportsFusedMultiplyAdd()
168. lowerTreesWalk(TR::Node *,TR::TreeTop *,vcount_t)
169. bndsChkNeedsLiteralFromPool(TR::Node *)
170. getMaximumNumberOfVRFsAllowedAcrossEdge(TR::Node *)
171. enableLiteralPoolRegisterForGRA()
172. setEstimatedLocationsForTargetAddressSnippetLabels(int32_t)
173. doBinaryEncoding()
174. doPeephole()
175. supportsMethodEntryPadding()
176. getGlobalGPRFromHPR(TR_GlobalRegisterNumber)
177. supportsComplexAddressing()
178. getGlobalRegisterNumber(uint32_t)
179. addProjectSpecializedRelocation(TR::Instruction *,uint8_t *,uint8_t *,TR_ExternalRelocationTargetKind,char *,uintptr_t,TR::Node *)
180. getSupportsEncodeUtf16BigWithSurrogateTest()
181. getVMThreadGlobalRegisterNumber()
182. buildRegisterMapForInstruction(class TR_GCStackMap *)
183. supportsLongRegAllocation()
184. considerTypeForGRA(TR::DataType)
185. considerTypeForGRA(TR::Node *)
186. getSupportsEncodeUtf16LittleWithSurrogateTest()
187. getGlobalGPRsPreservedAcrossCalls()
188. apply64BitLoadLabelRelativeRelocation(TR::Instruction *,TR::LabelSymbol *)
189. isSnippetMatched(TR::Snippet *,int32_t,TR::SymbolReference *)
190. apply32BitLoadLabelRelativeRelocation(TR::Instruction *,TR::LabelSymbol *,TR::LabelSymbol *,int32_t)
191. supportsAtomicAdd()
192. setUpForInstructionSelection()
193. dumpDataSnippets(TR::FILE *)
194. lowerTree(TR::Node *,TR::TreeTop *)
195. supportsOnDemandLiteralPool()
196. alwaysGeneratedSign(TR::Node *)
197. codegenSupportsUnsignedIntegerDivide()
198. endInstructionSelection()
199. isOutOfLineHotPath()

# Functions declared as pure virtual
* OMR::CodeGenerator::buildRegisterMapForInstruction(TR_GCStackMap*)
* OMR::CodeGenerator::doBinaryEncoding()
* OMR::CodeGenerator::doRegisterAssignment(TR_RegisterKinds)

# Functions provided with empty implementation
* OMR::X86::CodeGenerator::generateSwitchToInterpreterPrePrologue(TR::Instruction *prev, uint8_t alignment, uint8_t alignmentMargin)

# Problematic functions
* createLinkage(enum TR_LinkageConventions)
* createLinkageForCompilation()
The problem description and our suggested solution for it can be found in [this issue](https://github.com/eclipse/omr/issues/3235).

# Removing `self()` from member function calls
Removing all occurences of `self()` caused the following cases to happen:
* The following sentence appeared: `TR::Compilation* comp = comp()`. This is not allowed in C++. Hence, the `comp` local variable was renamed to `compilation`.
* Similarly, the following sentence appeared `TR::Machine* machine = machine();`. Hence, `machine` local variable was renamed to `thisMachine`.
* `OMR::Z::CodeGenerator::insertInstructionPrefetches()` is being called in `OMR::CodeGenerator::doInstructionSelection()` (guarded by `#ifdef` directives). When removing the `self()`, the function had to be added with an empty implementation in `OMR::CodeGenerator` for the code to compilate successfully.
