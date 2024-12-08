#!/bin/bash

# 現在のスクリプトのディレクトリを取得
SCRIPT_DIR=$(dirname "$0")

# functionディレクトリに移動
cd "$SCRIPT_DIR/function"

# make cleanとmakeの実行
make clean
make

# 生成されたrun.exeを実行
./run
