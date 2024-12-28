#ifndef ASSERT_H
#define ASSERT_H

#include <cstdio>

// ASSERTマクロ
#define ASSERT(cond) \
    do { \
        if (!(cond)) { \
            assert_failed(__FILE__, __LINE__, #cond); \
        } \
    } while (0)

// アサート失敗時の処理関数
void assert_failed(const char* file, int line, const char* cond);

#endif // ASSERT_H
