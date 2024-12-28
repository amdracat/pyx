#include "assert.h"
#include <iostream>
#include <fstream>
#include <ctime>

// アサート失敗時の処理
void assert_failed(const char* file, int line, const char* cond) {
    // 時刻を取得
    std::time_t t = std::time(nullptr);
    char time_str[100];
    std::strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", std::localtime(&t));

    // エラーメッセージを作成
    std::string error_message = "ASSERT FAILED: " + std::string(cond) + " in file " + file + " at line " + std::to_string(line) + " [Time: " + time_str + "]\n";
    
    // 標準エラー出力に表示
    std::cerr << error_message;

    // ログファイルに書き出し
    std::ofstream log_file("assert_log.txt", std::ios::app);
    if (log_file.is_open()) {
        log_file << error_message;
        log_file.close();
    } else {
        std::cerr << "Failed to open log file for writing.\n";
    }

    // アサート失敗を出力してプログラムを終了
    std::terminate();
}
