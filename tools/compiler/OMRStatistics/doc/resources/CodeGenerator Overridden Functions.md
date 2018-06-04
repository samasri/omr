| Base Namespace | Base ClassName | Signature | Overriding Namespace | Overriding ClassName |
| --- | --- | --- | --- | --- |
| OMR | CodeGenerator | CodeGenerator() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | allowGlobalRegisterAcrossBranch(class TR_RegisterCandidate *,TR::Node *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | apply32BitLabelRelativeRelocation(int32_t *,TR::LabelSymbol *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | apply32BitLoadLabelRelativeRelocation(TR::Instruction *,TR::LabelSymbol *,TR::LabelSymbol *,int32_t) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | arrayInitMinimumNumberOfBytes() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | arrayTranslateAndTestMinimumNumberOfIterations() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | arrayTranslateMinimumNumberOfElements(_Bool,_Bool) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | beginInstructionSelection() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | buildRegisterMapForInstruction(class TR_GCStackMap *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | canFoldLargeOffsetInAddressing() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | canNullChkBeImplicit(TR::Node *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | canTransformUnsafeCopyToArrayCopy() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | codegenSupportsUnsignedIntegerDivide() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | computeRegisterSaveDescription(class TR_BitVector *,_Bool) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | createLinkage(enum TR_LinkageConventions) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | doBinaryEncoding() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | doRegisterAssignment(enum TR_RegisterKinds) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | doRematerialization() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | dumpDataSnippets(TR::FILE *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | emitDataSnippets() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | endInstructionSelection() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | estimateBinaryLength(TR::MemoryReference *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | generateDebugCounterBump(TR::Instruction *,TR::DebugCounterBase *,int32_t,class TR_ScratchRegisterManager &) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | generateDebugCounterBump(TR::Instruction *,TR::DebugCounterBase *,int32_t,TR::RegisterDependencyConditions *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | generateDebugCounterBump(TR::Instruction *,TR::DebugCounterBase *,TR::Register *,class TR_ScratchRegisterManager &) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | generateDebugCounterBump(TR::Instruction *,TR::DebugCounterBase *,TR::Register *,TR::RegisterDependencyConditions *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | getGlobalFPRsPreservedAcrossCalls() | OMR::X86::AMD64 | CodeGenerator |
| OMR | CodeGenerator | getGlobalGPRsPreservedAcrossCalls() | OMR::X86::AMD64 | CodeGenerator |
| OMR | CodeGenerator | getGlobalRegisters(enum TR_SpillKinds,enum TR_LinkageConventions) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | getLinkageGlobalRegisterNumber(int8_t,TR::DataType) | OMR::X86::AMD64 | CodeGenerator |
| OMR | CodeGenerator | getMaximumNumberOfGPRsAllowedAcrossEdge(TR::Node *) | OMR::X86::AMD64 | CodeGenerator |
| OMR | CodeGenerator | getMaximumNumbersOfAssignableFPRs() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | getMaximumNumbersOfAssignableGPRs() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | getMaximumNumbersOfAssignableVRs() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | getSizeOfCombinedBuffer() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | getSupportsBitOpCodes() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | getSupportsBitPermute() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | getSupportsEncodeUtf16BigWithSurrogateTest() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | getSupportsEncodeUtf16LittleWithSurrogateTest() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | getSupportsIbyteswap() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | getSupportsNewObjectAlignment() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | getSupportsOpCodeForAutoSIMD(TR::ILOpCode,TR::DataType) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | getSupportsTenuredObjectAlignment() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | hasComplexAddressingMode() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | hasDataSnippets() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | hasTMEvaluator() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | internalPointerSupportImplemented() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | isAddressScaleIndexSupported(int32_t) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | isAlignmentInstruction(TR::Instruction *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | isBranchInstruction(TR::Instruction *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | isFenceInstruction(TR::Instruction *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | isLabelInstruction(TR::Instruction *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | isObjectOfSizeWorthAligning(uint32_t) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | isPreservedRegister(int32_t) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | isReturnInstruction(TR::Instruction *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | isTargetSnippetOrOutOfLine(TR::Instruction *,TR::Instruction **,TR::Instruction **) | OMR::X86 | CodeGenerator |
| OMR::X86 | CodeGenerator | longClobberEvaluate(TR::Node *) | OMR::X86::AMD64 | CodeGenerator |
| OMR | CodeGenerator | materializesHeapBase() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | needToAvoidCommoningInGRA() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | nodeResultGPRCount(TR::Node *,struct OMR::CodeGenerator::TR_RegisterPressureState *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | opCodeIsNoOpOnThisPlatform(TR::ILOpCode &) | OMR::X86::AMD64 | CodeGenerator |
| OMR | CodeGenerator | processIncomingParameterUsage(class TR_BitVector **,int32_t) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | processInstruction(TR::Instruction *,class TR_BitVector **,int32_t &,int32_t &,_Bool) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | removeUnavailableRegisters(class TR_RegisterCandidate *,TR::Block **,class TR_BitVector &) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | setEstimatedLocationsForDataSnippetLabels(int32_t) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | simulateNodeEvaluation(TR::Node *,struct OMR::CodeGenerator::TR_RegisterPressureState *,struct OMR::CodeGenerator::TR_RegisterPressureSummary *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | splitBlockEntry(TR::Instruction *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | splitEdge(TR::Instruction *,_Bool,_Bool,TR::Instruction *,TR::list<TR::Instruction *> *,_Bool) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | supportsAtomicAdd() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | supportsComplexAddressing() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | supportsDebugCounters(TR::DebugCounterInjectionPoint) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | supportsDirectJNICallsForAOT() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | supportsInliningOfIsInstance() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | supportsMergingGuards() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | supportsPassThroughCopyToNewVirtualRegister() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | supportsSinglePrecisionSQRT() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | updateSnippetMapWithRSD(TR::Instruction *,int32_t) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | willBeEvaluatedAsCallByCodeGen(TR::Node *,TR::Compilation *) | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | ~CodeGenerator() | OMR::X86 | CodeGenerator |
| OMR | CodeGenerator | codegenMulDecomposition(int64_t) | OMR::X86::I386 | CodeGenerator |
| OMR | CodeGenerator | getRegisterMapInfoBitsMask() | OMR::X86::I386 | CodeGenerator |
| OMR | CodeGenerator | getVMThreadGlobalRegisterNumber() | OMR::X86::I386 | CodeGenerator |
| OMR | CodeGenerator | pickRegister(class TR_RegisterCandidate *,TR::Block **,class TR_BitVector &,TR_GlobalRegisterNumber &,TR_LinkHead<class TR_RegisterCandidate> *) | OMR::X86::I386 | CodeGenerator |
| OMR | CodeGenerator | apply16BitLabelRelativeRelocation(int32_t *,TR::LabelSymbol *) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | apply16BitLoadLabelRelativeRelocation(TR::Instruction *,TR::LabelSymbol *,TR::LabelSymbol *,int32_t) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | apply24BitLabelRelativeRelocation(int32_t *,TR::LabelSymbol *) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | apply64BitLoadLabelRelativeRelocation(TR::Instruction *,TR::LabelSymbol *) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | branchesAreExpensive() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | calculateRegisterPressure() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | canTransformUnsafeSetMemory() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | doPeephole() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | generateNop(TR::Node *,TR::Instruction *,enum TR_NOPKind) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | getCurrentBlockIndex() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | getInternalPtrMapBit() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | getMaximumNumberOfFPRsAllowedAcrossEdge(TR::Node *) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | getNextAvailableBlockIndex() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | getPreferredLoopUnrollFactor() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | getSupportsConstantOffsetInAddressing(int64_t) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | getSupportsTLE() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | ilOpCodeIsSupported(TR::ILOpCodes) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | isGlobalRegisterAvailable(TR_GlobalRegisterNumber,TR::DataType) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | isOutOfLineHotPath() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | isRotateAndMask(TR::Node *) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | isSnippetMatched(TR::Snippet *,int32_t,TR::SymbolReference *) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | materializesLargeConstants() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | mulDecompositionCostIsJustified(int,char [],char [],int64_t) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | needsNormalizationBeforeShifts() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | setCurrentBlockIndex(int32_t) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | setNextAvailableBlockIndex(int32_t) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | shouldValueBeInACommonedNode(int64_t) | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | supportsFusedMultiplyAdd() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | supportsNegativeFusedMultiplyAdd() | OMR::Power | CodeGenerator |
| OMR | CodeGenerator | IsInMemoryType(TR::DataType) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | apply12BitLabelRelativeRelocation(int32_t *,TR::LabelSymbol *,_Bool) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | apply16BitLabelRelativeRelocation(int32_t *,TR::LabelSymbol *,int8_t,_Bool) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | apply32BitLabelTableRelocation(int32_t *,TR::LabelSymbol *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | arithmeticNeedsLiteralFromPool(TR::Node *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | arrayTranslateTableRequiresAlignment(_Bool,_Bool) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | bitwiseOpNeedsLiteralFromPool(TR::Node *,TR::Node *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | bndsChkNeedsLiteralFromPool(TR::Node *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | canBeAffectedByStoreTagStalls() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | canUseImmedInstruction(int64_t) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | codegenSupportsLoadlessBNDCheck() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | considerTypeForGRA(TR::DataType) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | considerTypeForGRA(TR::Node *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | considerTypeForGRA(TR::SymbolReference *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | constLoadNeedsLiteralFromPool(TR::Node *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | doInstructionSelection() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | dumpTargetAddressSnippets(TR::FILE *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | emitTargetAddressSnippets() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | enableLiteralPoolRegisterForGRA() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | endInternalControlFlow(TR::Instruction *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | excludeInvariantsFromGRAEnabled() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | getGlobalGPRFromHPR(TR_GlobalRegisterNumber) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | getGlobalHPRFromGPR(TR_GlobalRegisterNumber) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | getGlobalRegisterNumber(uint32_t) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | getMaximumNumberOfGPRsAllowedAcrossEdge(TR::Block *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | getMaximumNumberOfVRFsAllowedAcrossEdge(TR::Node *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | getMinByteForLongCompareNarrower() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | getMinShortForLongCompareNarrower() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | hasTargetAddressSnippets() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | isInternalControlFlowReg(TR::Register *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | isLiteralPoolOnDemandOn() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | lowerTreeIfNeeded(TR::Node *,int32_t,TR::Node *,TR::TreeTop *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | lowerTreesPropagateBlockToNode(TR::Node *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | lowerTreesWalk(TR::Node *,TR::TreeTop *,vcount_t) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | nodeMayCauseException(TR::Node *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | preLowerTrees() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | prepareForGRA() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | prepareRegistersForAssignment() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | setEstimatedLocationsForTargetAddressSnippetLabels(int32_t) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | setOnDemandLiteralPoolRun(_Bool) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | setUnavailableRegistersUsage(TR_Array<class TR_BitVector> &,TR_Array<class TR_BitVector> &) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | setVMThreadRequired(_Bool) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | shouldYankCompressedRefs() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | startInternalControlFlow(TR::Instruction *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | supports32bitAiadd() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | supportsDirectIntegralLoadStoresFromLiteralPool() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | supportsHighWordFacility() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | supportsLengthMinusOneForMemoryOpts() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | supportsLongRegAllocation() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | supportsOnDemandLiteralPool() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | supportsTrapsInTMRegion() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | usesImplicit64BitGPRs(TR::Node *) | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | yankIndexScalingOp() | OMR::Z | CodeGenerator |
| OMR | CodeGenerator | addProjectSpecializedPairRelocation(uint8_t *,uint8_t *,uint8_t *,TR_ExternalRelocationTargetKind,char *,uintptr_t,TR::Node *) | J9 | CodeGenerator |
| OMR | CodeGenerator | addProjectSpecializedRelocation(TR::Instruction *,uint8_t *,uint8_t *,TR_ExternalRelocationTargetKind,char *,uintptr_t,TR::Node *) | J9 | CodeGenerator |
| OMR | CodeGenerator | addProjectSpecializedRelocation(uint8_t *,uint8_t *,uint8_t *,TR_ExternalRelocationTargetKind,char *,uintptr_t,TR::Node *) | J9 | CodeGenerator |
| OMR | CodeGenerator | allocateRecompilationInfo() | J9::X86 | CodeGenerator |
| OMR::X86 | CodeGenerator | allowGuardMerging() | J9::X86 | CodeGenerator |
| OMR | CodeGenerator | buildInterpreterEntryPoint() | J9 | CodeGenerator |
| OMR | CodeGenerator | createHWPRecords() | J9 | CodeGenerator |
| OMR | CodeGenerator | createLinkageForCompilation() | J9 | CodeGenerator |
| OMR | CodeGenerator | createStackAtlas() | J9 | CodeGenerator |
| J9 | CodeGenerator | enableAESInHardwareTransformations() | J9::X86 | CodeGenerator |
| OMR | CodeGenerator | generateCatchBlockBBStartPrologue(TR::Node *,TR::Instruction *) | J9 | CodeGenerator |
| OMR::X86 | CodeGenerator | generateSwitchToInterpreterPrePrologue(TR::Instruction *,uint8_t,uint8_t) | J9::X86 | CodeGenerator |
| OMR | CodeGenerator | jitAdd32BitPicToPatchOnClassRedefinition(void *,void *,_Bool) | J9 | CodeGenerator |
| OMR | CodeGenerator | jitAdd32BitPicToPatchOnClassUnload(void *,void *) | J9 | CodeGenerator |
| OMR | CodeGenerator | jitAddPicToPatchOnClassRedefinition(void *,void *,_Bool) | J9 | CodeGenerator |
| OMR | CodeGenerator | jitAddPicToPatchOnClassUnload(void *,void *) | J9 | CodeGenerator |
| OMR | CodeGenerator | jitAddUnresolvedAddressMaterializationToPatchOnClassRedefinition(void *) | J9 | CodeGenerator |
| OMR | CodeGenerator | lowerTree(TR::Node *,TR::TreeTop *) | J9 | CodeGenerator |
| OMR | CodeGenerator | lowerTreesPreChildrenVisit(TR::Node *,TR::TreeTop *,vcount_t) | J9 | CodeGenerator |
| OMR | CodeGenerator | lowerTreesPreTreeTopVisit(TR::TreeTop *,vcount_t) | J9 | CodeGenerator |
| OMR | CodeGenerator | mustGenerateSwitchToInterpreterPrePrologue() | J9 | CodeGenerator |
| OMR | CodeGenerator | needClassAndMethodPointerRelocations() | J9 | CodeGenerator |
| OMR | CodeGenerator | needRelocationsForStatics() | J9 | CodeGenerator |
| OMR::X86 | CodeGenerator | nopsAlsoProcessedByRelocations() | J9::X86 | CodeGenerator |
| OMR | CodeGenerator | processRelocations() | J9 | CodeGenerator |
| OMR | CodeGenerator | registerAssumptions() | J9 | CodeGenerator |
| OMR::X86 | CodeGenerator | reserveNTrampolines(int32_t) | J9::X86 | CodeGenerator |
| OMR | CodeGenerator | setUpForInstructionSelection() | J9 | CodeGenerator |
| OMR | CodeGenerator | supportsMethodEntryPadding() | J9 | CodeGenerator |
| OMR | CodeGenerator | supportsUnneededLabelRemoval() | J9 | CodeGenerator |
| OMR | CodeGenerator | suppressInliningOfRecognizedMethod(TR::RecognizedMethod) | J9::X86 | CodeGenerator |
| OMR | CodeGenerator | wantToPatchClassPointer(const class TR_OpaqueClassBlock *,const uint8_t *) | J9 | CodeGenerator |
| OMR | CodeGenerator | wantToPatchClassPointer(const class TR_OpaqueClassBlock *,const TR::Node *) | J9 | CodeGenerator |
| OMR | CodeGenerator | lowerTreesPostChildrenVisit(TR::Node *,TR::TreeTop *,vcount_t) | J9::X86::i386 | CodeGenerator |
| OMR | CodeGenerator | lowerTreesPostTreeTopVisit(TR::TreeTop *,vcount_t) | J9::X86::i386 | CodeGenerator |
| OMR::Power | CodeGenerator | generateBinaryEncodingPrologue(struct TR_PPCBinaryEncodingData *) | J9::Power | CodeGenerator |
| OMR | CodeGenerator | inlineDirectCall(TR::Node *,TR::Register *&) | J9::Power | CodeGenerator |
| OMR | CodeGenerator | allowSplitWarmAndColdBlocks() | J9::Z | CodeGenerator |
| J9 | CodeGenerator | alwaysGeneratedSign(TR::Node *) | J9::Z | CodeGenerator |
| J9 | CodeGenerator | alwaysGeneratesAKnownCleanSign(TR::Node *) | J9::Z | CodeGenerator |
| J9 | CodeGenerator | alwaysGeneratesAKnownPositiveCleanSign(TR::Node *) | J9::Z | CodeGenerator |
| J9 | CodeGenerator | getMinimumNumberOfNodesBetweenMonitorsForTLE() | J9::Z | CodeGenerator |
| OMR | CodeGenerator | incRefCountForOpaquePseudoRegister(TR::Node *,TR::CodeGenerator *,TR::Compilation *) | J9::Z | CodeGenerator |
| OMR | CodeGenerator | propagateSignThroughBCDLeftShift(TR::DataType) | J9::Z | CodeGenerator |
