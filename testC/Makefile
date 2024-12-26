# コンパイラとフラグの定義
CC = gcc
CFLAGS = -Wall -Wextra -Werror -I./test_framework -fprofile-arcs -ftest-coverage
LDFLAGS = -fprofile-arcs -ftest-coverage

# ソースファイルとオブジェクトファイルの定義
SRC_DIR = .
TEST_FRAMEWORK_DIR = ./test_framework
SRC = $(SRC_DIR)/main_test.c $(SRC_DIR)/module1_test.c $(SRC_DIR)/module1.c $(SRC_DIR)/module2_test.c $(SRC_DIR)/module2.c $(TEST_FRAMEWORK_DIR)/test_framework.c
OBJ = $(SRC:.c=.o)

# 実行ファイルの名前
TARGET = test_program

# デフォルトターゲット
all: $(TARGET)

# 実行ファイルのビルドルール
$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

# オブジェクトファイルのビルドルール
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# カバレッジ情報の収集とレポート生成
coverage: $(TARGET)
	./$(TARGET)
	lcov --capture --directory . --output-file coverage.info
	genhtml coverage.info --output-directory coverage_report
	$(MAKE) clean_coverage

# クリーンアップルール
clean:
	rm -f $(OBJ) $(TARGET) *.gcda *.gcno *.gcov coverage.info
	rm -rf coverage_report

clean_coverage:
	rm -f *.gcda *.gcno *.gcov coverage.info

.PHONY: all clean coverage clean_coverage
