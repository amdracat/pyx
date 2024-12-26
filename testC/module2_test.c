#include <stdio.h>
#include "test_framework.h"

bool module2_function();
float module2_another_function();
bool module2_third_function();

// モジュール2のセットアップ関数
void module2_setup() {
    // モジュール2の初期化処理
    printf("Module 2 Setup called\n");
}

// モジュール2のティアダウン関数
void module2_teardown() {
    // モジュール2のクリーンアップ処理
    printf("Module 2 Teardown called\n");
}

void test_module2_case_1() {
    bool result = module2_function();
    ASSERT_TRUE(result); // 成功するはず
    ASSERT_TRUE(!result == false); // 成功するはず
}

void test_module2_case_2() {
    float result = module2_another_function();
    ASSERT_FLOAT_EQ(1.0f, result, 0.01f); // 成功するはず
    ASSERT_FLOAT_EQ(2.0f, result + 1.0f, 0.01f); // 成功するはず
}

void test_module2_case_3() {
    bool result = module2_third_function();
    ASSERT_TRUE(result); // 成功するはず
    ASSERT_TRUE(result == true); // 成功するはず
}

void test_module2_case_4() {
    float result = module2_another_function();
    ASSERT_FLOAT_EQ(2.0f, result, 0.01f); // 失敗するはず
    ASSERT_FLOAT_EQ(1.0f, result, 0.01f); // 成功するはず
}

void test_module2_case_5() {
    bool result = module2_function();
    ASSERT_TRUE(!result); // 失敗するはず
    ASSERT_TRUE(result == true); // 成功するはず
}

bool run_module2_tests() {
    TestCase tests[] = {
        {test_module2_case_1, "test_module2_case_1"},
        {test_module2_case_2, "test_module2_case_2"},
        {test_module2_case_3, "test_module2_case_3"},
        {test_module2_case_4, "test_module2_case_4"},
        {test_module2_case_5, "test_module2_case_5"}
    };
    int num_tests = sizeof(tests) / sizeof(tests[0]);
    return run_tests(tests, num_tests, module2_setup, module2_teardown);
}
