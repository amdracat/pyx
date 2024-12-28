#ifndef QUEUE_H
#define QUEUE_H

#include <stddef.h>

typedef struct Node {
    void* data;
    struct Node* next;
} Node;

typedef struct Queue {
    Node* front;
    Node* rear;
    size_t size;
} Queue;

// Queue functions
Queue* create_queue();
void destroy_queue(Queue* queue);
int enqueue(Queue* queue, void* data);
void* dequeue(Queue* queue);
int is_empty(Queue* queue);
size_t queue_size(Queue* queue);

#endif // QUEUE_H
