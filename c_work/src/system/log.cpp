#include "log.h"
#include "dx/DxLib.h"
#include <pthread.h>
#include <iostream>
#include <string>
#include <unordered_map>
#include <algorithm>

// コマンド処理関数の型
typedef void (*CommandFunction)();

// スレッドID
static pthread_t log_thread_id;
static bool running = true;

// コマンド関数
void cmd_exit() {
    DxLib_End();
    std::cout << "Exiting log thread." << std::endl;
    running = false;
}

void cmd_hello() {
    std::cout << "Hello, World!" << std::endl;
}

// コマンドテーブル
std::unordered_map<std::string, CommandFunction> commands = {
    {"exit", cmd_exit},
    {"hello", cmd_hello}
};

// コマンド受付スレッド
void* log_thread(void* arg) {
    while (running) {
        std::cout << ">> ";
        std::string command;
        std::getline(std::cin, command);

        // 空文字や改行の場合は無視
        if (command.empty()) {
            continue;
        }

        // 大文字小文字を区別しないように変換
        std::transform(command.begin(), command.end(), command.begin(), ::tolower);

        auto it = commands.find(command);
        if (it != commands.end()) {
            it->second(); // コマンドに対応する関数を実行
        } else {
            std::cout << "Unknown command: " << command << std::endl;
        }
    }
    return nullptr;
}

// ログスレッドの開始
void start_log_thread() {
    running = true;
    if (pthread_create(&log_thread_id, nullptr, log_thread, nullptr) != 0) {
        std::cerr << "Failed to create log thread." << std::endl;
    }
}

// ログスレッドの停止
void stop_log_thread() {
    running = false;
    pthread_join(log_thread_id, nullptr);
    std::cout << "Log thread stopped." << std::endl;
}
