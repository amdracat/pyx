# 変数定義
CC = gcc
CFLAGS = -Wall -Wextra -Werror
TARGET = run
SOURCES = $(wildcard *.c) $(wildcard */*.c)
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
