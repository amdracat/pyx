#ifndef TEST_FRAMEWORK_H
#define TEST_FRAMEWORK_H

#include <stdbool.h>

#define ASSERT_INT_EQ(expected, actual) \
    assert_int_eq(expected, actual, __FILE__, __LINE__, __func__)

#define ASSERT_FLOAT_EQ(expected, actual, tolerance) \
    assert_float_eq(expected, actual, tolerance, __FILE__, __LINE__, __func__)

#define ASSERT_TRUE(condition) \
    assert_true(condition, __FILE__, __LINE__, __func__)

typedef struct {
    void (*test_func)();
    const char* test_name;
} TestCase;

typedef void (*SetupFunc)();
typedef void (*TeardownFunc)();

void assert_int_eq(int expected, int actual, const char* file, int line, const char* func);
void assert_float_eq(float expected, float actual, float tolerance, const char* file, int line, const char* func);
void assert_true(bool condition, const char* file, int line, const char* func);

bool run_tests(TestCase* test_cases, int num_tests, SetupFunc module_setup, TeardownFunc module_teardown);
bool print_results();

#endif // TEST_FRAMEWORK_H
