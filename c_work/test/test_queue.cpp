#include "data_structures/queue.h"
#include "test_framework/test_framework.h"

// Individual test functions
void test_create_queue() {
    Queue* queue = create_queue();
    ASSERT_TRUE(queue != NULL);
    destroy_queue(queue);
}

void test_enqueue_dequeue() {
    Queue* queue = create_queue();
    ASSERT_TRUE(queue != NULL);

    int data1 = 10, data2 = 20;
    ASSERT_INT_EQ(0, enqueue(queue, &data1));
    ASSERT_INT_EQ(0, enqueue(queue, &data2));

    int* result1 = (int*)dequeue(queue);
    int* result2 = (int*)dequeue(queue);

    ASSERT_TRUE(result1 != NULL && *result1 == data1);
    ASSERT_TRUE(result2 != NULL && *result2 == data2);

    destroy_queue(queue);
}

void test_is_empty() {
    Queue* queue = create_queue();
    ASSERT_TRUE(queue != NULL);
    ASSERT_TRUE(is_empty(queue));

    int data = 30;
    enqueue(queue, &data);
    ASSERT_TRUE(!is_empty(queue));

    dequeue(queue);
    ASSERT_TRUE(is_empty(queue));

    destroy_queue(queue);
}

void test_queue_size() {
    Queue* queue = create_queue();
    ASSERT_TRUE(queue != NULL);
    ASSERT_INT_EQ(0, queue_size(queue));

    int data = 40;
    enqueue(queue, &data);
    ASSERT_INT_EQ(1, queue_size(queue));

    dequeue(queue);
    ASSERT_INT_EQ(0, queue_size(queue));

    destroy_queue(queue);
}

// Function to run all queue tests
void run_all_tests_queue() {
    TestCase queue_tests[] = {
        {test_create_queue, "test_create_queue"},
        {test_enqueue_dequeue, "test_enqueue_dequeue"},
        {test_is_empty, "test_is_empty"},
        {test_queue_size, "test_queue_size"}
    };

    int num_queue_tests = sizeof(queue_tests) / sizeof(queue_tests[0]);

    run_tests(queue_tests, num_queue_tests, NULL, NULL);
}
