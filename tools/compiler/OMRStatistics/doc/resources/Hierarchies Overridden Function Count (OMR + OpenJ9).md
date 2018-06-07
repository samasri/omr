# Possible cases for overrides and assumptions

| Case # | BaseNamespace | BaseClassName | Signature | OverridingNamespace | OverridingClassName |
| --- | --- | --- | --- | --- | --- |
| 1 | OMR | CodeGenerator | hasTMEvaluator() | OMR::X86 | CodeGenerator
| 2 | OMR | CodeCache | dumpCodeCache() | J9 | CodeCache
| 3 | J9 | CodeGenerator | enableAESInHardwareTransformations() | J9::X86 | CodeGenerator
| 4 | OMR | Instruction | Instruction(TR::CodeGenerator *,TR::Instruction *,TR::class InstOpCode::Mnemonic,TR::Node *) | J9 | Instruction
| 4 | J9 | Instruction | Instruction(TR::CodeGenerator *,TR::Instruction *,TR::class InstOpCode::Mnemonic,TR::Node *) | J9::Z | StaticSymbol
| 5 | OMR | Symbol | isStatic()() | OMR::X86 | MethodSymbol
| 5 | J9 | Symbol | getRecognizedField() | J9 | StaticSymbol

Notes about cases:
1. Same classname; the base and overriding classes are from a `OMR` namespace
2. Same classname; the base class is from an `OMR` namespace and the overriding class is from a `J9` namespace
3. Same classname; the base and overriding classes are from a `J9` namespace
4. These two are assumed one override in `OMR` (since that is where the override started)
5. In cases like this, I merge the `MethodSymbol` hierarchy and `Symbol` to the base className (`Symbol`) hierarchy after producing the table, and add their counts together. Below are the cases where I had to merge hierarchies:


| Base Qualified Signature | Overriding  Qualified Signature |
| --- | --- |
| OMR::Register::setAssignedRegister(TR::Register \*) | OMR::RealRegister |
| OMR::Symbol::getKind() | OMR::AutomaticSymbol |
| OMR::Symbol::getName() | OMR::StaticSymbol |
| OMR::Symbol::getOffset() | OMR::RegisterMappedSymbol |
| OMR::Symbol::isReferenced() | OMR::AutomaticSymbol |
| OMR::Symbol::isStatic() | OMR::MethodSymbol |
| J9::Symbol::getRecognizedField() | J9::StaticSymbol |

I also filtered out virtual and implicit functions

# Results
| ID | Hierarchy | Number of Overridden Functions in OMR | Number of Overridden functions in J9 |
| --- | --- | --- | --- |
| 1 | CodeGenerator | 194 | 5 |
| 2 | MemoryReference | 62 | 0 |
| 3 | Symbol | 58 | 1 |
| 4 | Compilation | 45 | 1 |
| 5 | ClassEnv | 35 | 0 |
| 6 | VMEnv | 34 | 0 |
| 7 | GCStackAtlas | 26 | 0 |
| 8 | Instruction | 20 | 0 |
| 9 | TreeEvaluator | 18 | 0 |
| 10 | ArithEnv | 17 | 0 |
| 11 | Register | 15 | 0 |
| 12 | Options | 14 | 0 |
| 13 | IL | 13 | 0 |
| 14 | Node | 12 | 0 |
| 15 | DataType | 10 | 0 |
| 16 | CodeCacheManager | 8 | 1 |
| 17 | SymbolReference | 8 | 1 |
| 18 | IO | 7 | 0 |
| 19 | TransformUtil | 6 | 0 |
| 20 | CodeCache | 6 | 0 |
| 21 | CodeGenPhase | 5 | 0 |
| 22 | Linkage | 5 | 0 |
| 23 | CodeCacheMemorySegment | 5 | 1 |
| 24 | RegisterPair | 5 | 0 |
| 25 | Snippet | 4 | 0 |
| 26 | IlGeneratorMethodDetails | 4 | 4 |
| 27 | LabelSymbol | 3 | 0 |
| 28 | VMMethodEnv | 3 | 0 |
| 29 | DebugEnv | 3 | 0 |
| 30 | MonitorTable | 3 | 0 |
| 31 | Block | 3 | 0 |
| 32 | AheadOfTimeCompile | 2 | 1 |
| 33 | ParameterSymbol | 2 | 0 |
| 34 | CompilerEnv | 2 | 0 |
| 35 | TreeTop | 2 | 0 |
| 36 | ResolvedMethodSymbol | 1 | 0 |
| 37 | ELFRelocationResolver | 1 | 0 |
| 38 | IlGenRequest | 1 | 0 |
| 39 | Optimization | 1 | 0 |
| 40 | OptimizationManager | 1 | 0 |
| 41 | Machine | 1 | 0 |
| 42 | RegisterIterator | 1 | 0 |
| 43 | KnownObjectTable | 1 | 0 |
| 44 | CodeCacheConfig | 1 | 0 |
| 45 | VMAccessCriticalSection | 0 | 3 |
