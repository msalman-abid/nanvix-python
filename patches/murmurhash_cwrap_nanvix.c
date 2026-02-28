/* murmurhash_cwrap.c - Fixed C wrapper for Nanvix cross-compilation.
 *
 * MurmurHash2 functions are compiled as C++ (mangled symbols).
 * MurmurHash3 functions use extern "C" linkage (unmangled symbols).
 *
 * This replacement wrapper avoids referencing incorrect mangled names
 * for MurmurHash3 that don't match the actual compilation output.
 */
#include <stdint.h>

/* MurmurHash2: C++ linkage - reference mangled names directly */
extern uint64_t _Z13MurmurHash64APKviy(const void *key, int len, uint64_t seed);
extern uint64_t _Z13MurmurHash64BPKviy(const void *key, int len, uint64_t seed);

uint64_t MurmurHash64A(const void *key, int len, uint64_t seed) {
    return _Z13MurmurHash64APKviy(key, len, seed);
}

uint64_t MurmurHash64B(const void *key, int len, uint64_t seed) {
    return _Z13MurmurHash64BPKviy(key, len, seed);
}

/* MurmurHash3: extern "C" linkage - symbols are unmangled in MurmurHash3.o,
 * so no wrapper needed. The linker resolves them directly. */
