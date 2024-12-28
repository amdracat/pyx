#include "data_structures/list.h"
#include "mem_allocator/mem_allocator.h"
#include <stdlib.h>

List* create_list() {
    List* list = (List*)my_malloc(sizeof(List));
    if (!list) {
        return NULL;
    }
    list->head = NULL;
    list->size = 0;
    return list;
}

void destroy_list(List* list) {
    while (!is_list_empty(list)) {
        remove_from_list(list, list->head->data);
    }
    my_free(list);
}

int add_to_list(List* list, void* data) {
    ListNode* new_node = (ListNode*)my_malloc(sizeof(ListNode));
    if (!new_node) {
        return -1; // Failed to allocate memory
    }
    new_node->data = data;
    new_node->next = list->head;
    list->head = new_node;
    list->size++;
    return 0; // Success
}

void* remove_from_list(List* list, void* data) {
    if (is_list_empty(list)) {
        return NULL;
    }

    ListNode* current = list->head;
    ListNode* prev = NULL;

    while (current != NULL && current->data != data) {
        prev = current;
        current = current->next;
    }

    if (current == NULL) {
        return NULL; // Data not found
    }

    if (prev == NULL) {
        list->head = current->next;
    } else {
        prev->next = current->next;
    }

    void* removed_data = current->data;
    my_free(current);
    list->size--;
    return removed_data;
}

int is_list_empty(List* list) {
    return list->size == 0;
}

size_t list_size(List* list) {
    return list->size;
}
