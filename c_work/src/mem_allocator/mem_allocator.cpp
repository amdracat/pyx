#include "mem_allocator.h"
#include <stdlib.h> // For malloc and free

void* my_malloc(size_t size) {
    return malloc(size); // Wrapper around malloc
}

void my_free(void* ptr) {
    free(ptr); // Wrapper around free
}
