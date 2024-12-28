#include "data_structures/stack.h"
#include "test_framework/test_framework.h"

void test_create_stack() {
    Stack* stack = create_stack();
    ASSERT_TRUE(stack != NULL);
    destroy_stack(stack);
}

void test_push_pop_stack() {
    Stack* stack = create_stack();
    ASSERT_TRUE(stack != NULL);

    int data1 = 10, data2 = 20;
    ASSERT_INT_EQ(0, push_stack(stack, &data1));
    ASSERT_INT_EQ(0, push_stack(stack, &data2));

    int* result1 = (int*)pop_stack(stack);
    int* result2 = (int*)pop_stack(stack);

    ASSERT_TRUE(result1 != NULL && *result1 == data2);
    ASSERT_TRUE(result2 != NULL && *result2 == data1);

    destroy_stack(stack);
}

void test_is_stack_empty() {
    Stack* stack = create_stack();
    ASSERT_TRUE(stack != NULL);
    ASSERT_TRUE(is_stack_empty(stack));

    int data = 30;
    push_stack(stack, &data);
    ASSERT_TRUE(!is_stack_empty(stack));

    pop_stack(stack);
    ASSERT_TRUE(is_stack_empty(stack));

    destroy_stack(stack);
}

void test_stack_size() {
    Stack* stack = create_stack();
    ASSERT_TRUE(stack != NULL);
    ASSERT_INT_EQ(0, stack_size(stack));

    int data = 40;
    push_stack(stack, &data);
    ASSERT_INT_EQ(1, stack_size(stack));

    pop_stack(stack);
    ASSERT_INT_EQ(0, stack_size(stack));

    destroy_stack(stack);
}

// Function to run all stack tests
void run_all_tests_stack() {
    TestCase stack_tests[] = {
        {test_create_stack, "test_create_stack"},
        {test_push_pop_stack, "test_push_pop_stack"},
        {test_is_stack_empty, "test_is_stack_empty"},
        {test_stack_size, "test_stack_size"}
    };

    int num_stack_tests = sizeof(stack_tests) / sizeof(stack_tests[0]);

    run_tests(stack_tests, num_stack_tests, NULL, NULL);
}
