#include "data_structures/queue.h"
#include "mem_allocator/mem_allocator.h"
#include <stdlib.h>

Queue* create_queue() {
    Queue* queue = (Queue*)my_malloc(sizeof(Queue));
    if (!queue) {
        return NULL;
    }
    queue->front = NULL;
    queue->rear = NULL;
    queue->size = 0;
    return queue;
}

void destroy_queue(Queue* queue) {
    while (!is_empty(queue)) {
        dequeue(queue);
    }
    my_free(queue);
}

int enqueue(Queue* queue, void* data) {
    Node* new_node = (Node*)my_malloc(sizeof(Node));
    if (!new_node) {
        return -1; // Failed to allocate memory
    }
    new_node->data = data;
    new_node->next = NULL;
    if (is_empty(queue)) {
        queue->front = new_node;
        queue->rear = new_node;
    } else {
        queue->rear->next = new_node;
        queue->rear = new_node;
    }
    queue->size++;
    return 0; // Success
}

void* dequeue(Queue* queue) {
    if (is_empty(queue)) {
        return NULL;
    }
    Node* front_node = queue->front;
    void* data = front_node->data;
    queue->front = front_node->next;
    my_free(front_node);
    queue->size--;
    if (is_empty(queue)) {
        queue->rear = NULL;
    }
    return data;
}

int is_empty(Queue* queue) {
    return queue->size == 0;
}

size_t queue_size(Queue* queue) {
    return queue->size;
}
