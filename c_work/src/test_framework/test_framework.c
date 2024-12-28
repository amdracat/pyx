#include "test_framework.h"
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// 時間測定を有効にするためのマクロ定義
#define ENABLE_TIME_MEASUREMENT

#ifdef ENABLE_TIME_MEASUREMENT
#include <time.h>  // 時間計測用
static double total_time_taken = 0;
#endif

typedef struct {
    int total_tests;
    int failed_tests;
    int total_assertions;
    int failed_assertions;
    int total_suites;
    int failed_suites;
} TestResults;

static TestResults global_results = {0, 0, 0, 0, 0, 0};

static void test_printf(const char *format, ...) {
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
}

void assert_int_eq(int expected, int actual, const char* file, int line, const char* func) {
    global_results.total_assertions++;
    if (expected != actual) {
        global_results.failed_assertions++;
        test_printf("ASSERTION FAILED: %s:%d: %s: Expected %d, but got %d\n", file, line, func, expected, actual);
    }
}

void assert_float_eq(float expected, float actual, float tolerance, const char* file, int line, const char* func) {
    global_results.total_assertions++;
    if (fabs(expected - actual) > tolerance) {
        global_results.failed_assertions++;
        test_printf("ASSERTION FAILED: %s:%d: %s: Expected %f, but got %f\n", file, line, func, expected, actual);
    }
}

void assert_true(bool condition, const char* file, int line, const char* func) {
    global_results.total_assertions++;
    if (!condition) {
        global_results.failed_assertions++;
        test_printf("ASSERTION FAILED: %s:%d: %s: Condition is false\n", file, line, func);
    }
}

// テストケースをシャッフルする関数
void shuffle_tests(TestCase* test_cases, int num_tests) {
    srand((unsigned int)time(NULL));
    for (int i = num_tests - 1; i > 0; --i) {
        int j = rand() % (i + 1);
        TestCase temp = test_cases[i];
        test_cases[i] = test_cases[j];
        test_cases[j] = temp;
    }
}

bool run_tests(TestCase* test_cases, int num_tests, SetupFunc module_setup, TeardownFunc module_teardown) {
    if (module_setup) {
        module_setup();
    }

    TestResults local_results = {0, 0, 0, 0, 0, 0};

    global_results.total_suites++;

    // テストケースをシャッフル
    shuffle_tests(test_cases, num_tests);

    for (int i = 0; i < num_tests; ++i) {
        local_results.total_tests++;
        int failed_assertions_before = global_results.failed_assertions;

        #ifdef ENABLE_TIME_MEASUREMENT
        // 処理時間の計測開始
        clock_t start_time = clock();
        #endif
        
        test_cases[i].test_func();
        
        #ifdef ENABLE_TIME_MEASUREMENT
        // 処理時間の計測終了
        clock_t end_time = clock();
        double time_taken = ((double)(end_time - start_time)) / CLOCKS_PER_SEC;
        total_time_taken += time_taken;
        #endif
        
        if (global_results.failed_assertions > failed_assertions_before) {
            local_results.failed_tests++;
            test_printf("Test case %s: FAILED\n\n", test_cases[i].test_name);
        }
    }

    global_results.total_tests += local_results.total_tests;
    global_results.failed_tests += local_results.failed_tests;

    if (local_results.failed_tests > 0) {
        global_results.failed_suites++;
    }

    if (module_teardown) {
        module_teardown();
    }

    return local_results.failed_tests == 0;
}

bool print_results() {
    bool success = global_results.failed_tests == 0;
    test_printf("\n==================== TEST RESULTS ====================\n");
    test_printf("--Run Summary: Type      Total     Failed\n");
    test_printf("               Suites    %-8d %-8d\n", global_results.total_suites, global_results.failed_suites);
    test_printf("               Tests     %-8d %-8d\n", global_results.total_tests, global_results.failed_tests);
    test_printf("               Asserts   %-8d %-8d\n", global_results.total_assertions, global_results.failed_assertions);
    #ifdef ENABLE_TIME_MEASUREMENT
    test_printf("Total time taken: %.6f seconds\n", total_time_taken);
    #endif
    test_printf("======================================================\n");
    return success;
}