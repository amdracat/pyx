#include "data_structures/list.h"
#include "test_framework/test_framework.h"

void test_create_list() {
    List* list = create_list();
    ASSERT_TRUE(list != NULL);
    destroy_list(list);
}

void test_add_remove_list() {
    List* list = create_list();
    ASSERT_TRUE(list != NULL);

    int data1 = 10, data2 = 20;
    ASSERT_INT_EQ(0, add_to_list(list, &data1));
    ASSERT_INT_EQ(0, add_to_list(list, &data2));

    int* result1 = (int*)remove_from_list(list, &data1);
    int* result2 = (int*)remove_from_list(list, &data2);

    ASSERT_TRUE(result1 != NULL && *result1 == data1);
    ASSERT_TRUE(result2 != NULL && *result2 == data2);

    destroy_list(list);
}

void test_is_list_empty() {
    List* list = create_list();
    ASSERT_TRUE(list != NULL);
    ASSERT_TRUE(is_list_empty(list));

    int data = 30;
    add_to_list(list, &data);
    ASSERT_TRUE(!is_list_empty(list));

    remove_from_list(list, &data);
    ASSERT_TRUE(is_list_empty(list));

    destroy_list(list);
}

void test_list_size() {
    List* list = create_list();
    ASSERT_TRUE(list != NULL);
    ASSERT_INT_EQ(0, list_size(list));

    int data = 40;
    add_to_list(list, &data);
    ASSERT_INT_EQ(1, list_size(list));

    remove_from_list(list, &data);
    ASSERT_INT_EQ(0, list_size(list));

    destroy_list(list);
}

// Function to run all list tests
void run_all_tests_list() {
    TestCase list_tests[] = {
        {test_create_list, "test_create_list"},
        {test_add_remove_list, "test_add_remove_list"},
        {test_is_list_empty, "test_is_list_empty"},
        {test_list_size, "test_list_size"}
    };

    int num_list_tests = sizeof(list_tests) / sizeof(list_tests[0]);

    run_tests(list_tests, num_list_tests, NULL, NULL);
}
