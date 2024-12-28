#ifndef MEM_ALLOCATOR_H
#define MEM_ALLOCATOR_H

#include <stddef.h>

// Simple memory allocator API
void* my_malloc(size_t size);
void my_free(void* ptr);

#endif // MEM_ALLOCATOR_H
