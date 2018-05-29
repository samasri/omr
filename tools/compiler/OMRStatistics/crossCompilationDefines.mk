export DEFINES_AMD64 = '-D__sync()=' \
'-D__lwsync()=' \
'-D__isync()=' \
-DBITVECTOR_BIT_NUMBERING_MSB \
-DUT_DIRECT_TRACE_REGISTRATION \
-DJITTEST \
-DTEST_PROJECT_SPECIFIC \
-DTR_HOST_X86 \
-DTR_HOST_64BIT \
-DBITVECTOR_64BIT \
-DLINUX -DTR_TARGET_X86 \
-DTR_TARGET_64BIT \
-DSUPPORTS_THREAD_LOCAL \
-D_LONG_LONG \
-DJ9HAMMER \
-DDEBUG

export PLUGIN_INCLUDES_AMD64 = -I $(OMR)/include_core \
-I $(OMR)/fvtest/compilertest/x/amd64 \
-I $(OMR)/fvtest/compilertest/x \
-I $(OMR)/fvtest/compilertest \
-I $(OMR)/fvtest \
-I $(OMR)/compiler/x/amd64 \
-I $(OMR)/compiler/x \
-I $(OMR)/compiler \
-I $(OMR)/ \
-I $(OMR)/third_party/gtest-1.8.0 \
-I $(OMR)/third_party/gtest-1.8.0/include \
-I $(OMR)/compiler/

export DEFINES_I386 = '-D__sync()=' '-D__lwsync()=' '-D__isync()=' \
-DBITVECTOR_BIT_NUMBERING_MSB \
-DUT_DIRECT_TRACE_REGISTRATION \
-DJITTEST \
-DTEST_PROJECT_SPECIFIC \
-DTR_HOST_X86 \
-DTR_HOST_64BIT \
-DBITVECTOR_64BIT \
-DLINUX \
-DTR_TARGET_X86 \
-DTR_TARGET_32BIT \
-DSUPPORTS_THREAD_LOCAL \
-D_LONG_LONG \
-DJ9HAMMER \
-DDEBUG

export PLUGIN_INCLUDES_I386 = -I $(OMR)/include_core \
-I $(OMR)/fvtest/compilertest/x/i386 \
-I $(OMR)/fvtest/compilertest/x \
-I $(OMR)/fvtest/compilertest \
-I $(OMR)/fvtest \
-I $(OMR)/compiler/x/i386 \
-I $(OMR)/compiler/x \
-I $(OMR)/compiler \
-I $(OMR) \
-I $(OMR) \
-I $(OMR)/third_party/gtest-1.8.0 \
-I $(OMR)/third_party/gtest-1.8.0/include

export DEFINES_P = -DBITVECTOR_BIT_NUMBERING_MSB \
-DUT_DIRECT_TRACE_REGISTRATION \
-DJITTEST \
-DTEST_PROJECT_SPECIFIC \
-DTR_HOST_X86 \
-DTR_HOST_64BIT \
-DBITVECTOR_64BIT \
-DLINUX \
-DTR_TARGET_POWER \
-DTR_TARGET_64BIT \
-DSUPPORTS_THREAD_LOCAL \
-D_LONG_LONG \
-DJ9HAMMER \
-DDEBUG

export PLUGIN_INCLUDES_P = -I $(OMR)/include_core \
-I $(OMR)/fvtest/compilertest/p/ \
-I $(OMR)/fvtest/compilertest/p \
-I $(OMR)/fvtest/compilertest \
-I $(OMR)/fvtest \
-I $(OMR)/compiler/p/ \
-I $(OMR)/compiler/p \
-I $(OMR)/compiler \
-I $(OMR) \
-I $(OMR) \
-I $(OMR)/third_party/gtest-1.8.0 \
-I $(OMR)/third_party/gtest-1.8.0/include

export DEFINES_Z = -DBITVECTOR_BIT_NUMBERING_MSB \
-DUT_DIRECT_TRACE_REGISTRATION \
-DJITTEST \
-DTEST_PROJECT_SPECIFIC \
-DTR_HOST_X86 \
-DTR_HOST_64BIT \
-DBITVECTOR_64BIT \
-DLINUX \
-DTR_TARGET_S390 \
-DTR_TARGET_64BIT \
-DSUPPORTS_THREAD_LOCAL \
-D_LONG_LONG \
-DJ9HAMMER \
-DDEBUG

export PLUGIN_INCLUDES_Z = -I $(OMR)/include_core \
-I $(OMR)/fvtest/compilertest/z/ \
-I $(OMR)/fvtest/compilertest/z \
-I $(OMR)/fvtest/compilertest \
-I $(OMR)/fvtest \
-I $(OMR)/compiler/z/ \
-I $(OMR)/compiler/z \
-I $(OMR)/compiler \
-I $(OMR) \
-I $(OMR) \
-I $(OMR)/third_party/gtest-1.8.0 \
-I $(OMR)/third_party/gtest-1.8.0/include

# Variables used to generate configuration (includes and defines) for openJ9
export TOOLCHAIN=gnu
export ASSUMES=1
export PUBLIC_BUILD=0
export OS=linux
export BUILD_CONFIG=prod
export HOST_BITS=64
export TARGET_BITS=64