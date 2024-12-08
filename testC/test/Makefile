# 変数定義
CC = gcc
CFLAGS = -Wall -Wextra -Werror -I../function -I.
TARGET = run

# ソースファイルの指定
FUNCTION_SRC = $(filter-out ../function/main.c, $(wildcard ../function/*.c))
TEST_SRC = $(wildcard *.c)
SOURCES = $(FUNCTION_SRC) $(TEST_SRC)
OBJECTS = $(SOURCES:.c=.o)

# デフォルトのターゲット
all: $(TARGET)

# 実行ファイルの生成
$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^

# オブジェクトファイルの生成
%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

# クリーンアップ
clean:
	rm -f $(TARGET) $(OBJECTS)

.PHONY: all clean
