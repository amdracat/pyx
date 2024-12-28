#include "data_structures/stack.h"
#include "mem_allocator/mem_allocator.h"
#include <stdlib.h>

Stack* create_stack() {
    Stack* stack = (Stack*)my_malloc(sizeof(Stack));
    if (!stack) {
        return NULL;
    }
    stack->top = NULL;
    stack->size = 0;
    return stack;
}

void destroy_stack(Stack* stack) {
    while (!is_stack_empty(stack)) {
        pop_stack(stack);
    }
    my_free(stack);
}

int push_stack(Stack* stack, void* data) {
    StackNode* new_node = (StackNode*)my_malloc(sizeof(StackNode));
    if (!new_node) {
        return -1; // Failed to allocate memory
    }
    new_node->data = data;
    new_node->next = stack->top;
    stack->top = new_node;
    stack->size++;
    return 0; // Success
}

void* pop_stack(Stack* stack) {
    if (is_stack_empty(stack)) {
        return NULL;
    }
    StackNode* top_node = stack->top;
    void* data = top_node->data;
    stack->top = top_node->next;
    my_free(top_node);
    stack->size--;
    return data;
}

int is_stack_empty(Stack* stack) {
    return stack->size == 0;
}

size_t stack_size(Stack* stack) {
    return stack->size;
}
