#ifndef LIST_H
#define LIST_H

#include <stddef.h>

typedef struct ListNode {
    void* data;
    struct ListNode* next;
} ListNode;

typedef struct List {
    ListNode* head;
    size_t size;
} List;

// List functions
List* create_list();
void destroy_list(List* list);
int add_to_list(List* list, void* data);
void* remove_from_list(List* list, void* data);
int is_list_empty(List* list);
size_t list_size(List* list);

#endif // LIST_H
