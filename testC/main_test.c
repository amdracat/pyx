#include "test_framework.h"
#include <stdio.h>
bool run_module1_tests();
bool run_module2_tests();

int main() {
    printf("\n==================== TEST STARTED ====================\n");

    bool success = true;

    // モジュール1のテストを実行
    success &= run_module1_tests();

    // モジュール2のテストを実行
    success &= run_module2_tests();

    // 結果を表示
    success &= print_results();

    // テスト結果に基づいて戻り値を設定
    return success ? 0 : 1;
}
