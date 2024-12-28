#include <stdio.h>
#include "test_framework.h"

int module1_function();
int module1_another_function();
int module1_third_function();

// モジュール1のセットアップ関数
void module1_setup() {
    // モジュール1の初期化処理
    printf("Module 1 Setup called\n");
}

// モジュール1のティアダウン関数
void module1_teardown() {
    // モジュール1のクリーンアップ処理
    printf("Module 1 Teardown called\n");
}

void test_module1_case_1() {
    int result = module1_function();
    ASSERT_INT_EQ(1, result); // 成功するはず
    ASSERT_INT_EQ(2, result + 1); // 成功するはず
    ASSERT_INT_EQ(0, result - 1); // 成功するはず
}

void test_module1_case_2() {
    int result = module1_another_function();
    ASSERT_INT_EQ(3, result); // 失敗するはず
    ASSERT_INT_EQ(2, result); // 成功するはず
}

void test_module1_case_3() {
    int result = module1_third_function();
    ASSERT_INT_EQ(5, result); // 成功するはず
    ASSERT_INT_EQ(10, result * 2); // 成功するはず
}

void test_module1_case_4() {
    int result = module1_function();
    ASSERT_INT_EQ(0, result); // 失敗するはず
    ASSERT_INT_EQ(1, result); // 成功するはず
}

void test_module1_case_5() {
    int result = module1_another_function();
    ASSERT_INT_EQ(2, result); // 成功するはず
    ASSERT_INT_EQ(4, result * 2); // 成功するはず
}

bool run_module1_tests() {
    TestCase tests[] = {
        {test_module1_case_1, "test_module1_case_1"},
        {test_module1_case_2, "test_module1_case_2"},
        {test_module1_case_3, "test_module1_case_3"},
        {test_module1_case_4, "test_module1_case_4"},
        {test_module1_case_5, "test_module1_case_5"}
    };
    int num_tests = sizeof(tests) / sizeof(tests[0]);
    return run_tests(tests, num_tests, module1_setup, module1_teardown);
}
