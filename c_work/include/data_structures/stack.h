#ifndef STACK_H
#define STACK_H

#include <stddef.h>

typedef struct StackNode {
    void* data;
    struct StackNode* next;
} StackNode;

typedef struct Stack {
    StackNode* top;
    size_t size;
} Stack;

// Stack functions
Stack* create_stack();
void destroy_stack(Stack* stack);
int push_stack(Stack* stack, void* data);
void* pop_stack(Stack* stack);
int is_stack_empty(Stack* stack);
size_t stack_size(Stack* stack);

#endif // STACK_H
