#!/bin/sh

# lcovとgenhtmlが存在するディレクトリをパスに追加
export PATH=$PATH:/c/ProgramData/chocolatey/lib/lcov/tools/bin

# クリーン
make clean

# ビルド
make

# テストプログラムの実行
./test_program

# 引数が渡された場合はカバレッジ情報を取得
if [ $# -gt 0 ]; then
    echo "カバレッジ情報を取得中..."
    # カバレッジ情報の収集
    lcov --capture --directory . --output-file coverage.info

    # カバレッジレポートの生成
    genhtml coverage.info --output-directory coverage_report

    # カバレッジレポートの生成が成功した場合のメッセージ
    if [ $? -eq 0 ]; then
        echo "カバレッジレポートが生成されました。'coverage_report' ディレクトリ内の 'index.html' を開いて確認してください。"
    else
        echo "カバレッジレポートの生成に失敗しました。"
    fi
else
    echo "カバレッジ情報は取得されませんでした。"
fi
