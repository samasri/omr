# Functions to virtualize
1. setDataType(TR::DataType)
2. getName()
3. getOffset()
4. isReferenced()
5. isStatic()
6. getRecognizedField()

# Ignored functions for being static
1. jitPersistentFree(void *)
2. jitPersistentAlloc(size_t)
3. convertTypeToSize(TR::DataType)

# Problematic functions
1. getKind(): `OMR::Symbol::getKind()` returns an `int32_t`. `OMR::AutomaticSymbol::getKind()` returns an `TR::ILOpCodes` object. Since `OMR::AutomaticSymbol` indirectly inherits from `OMR::Symbol::getKind`, it is not possible to virtualize this function.
