#!/bin/sh

# lcovとgenhtmlが存在するディレクトリをパスに追加
export PATH=$PATH:/c/ProgramData/chocolatey/lib/lcov/tools/bin

# クリーンアップ関数
clean_all() {
    make clean
    echo "全てのビルドファイルとカバレッジファイルが削除されました。"
}

# 引数のチェック
if [ "$1" = "-clean" ]; then
    clean_all
elif [ "$1" = "-all" ]; then
    # クリーン
    make clean

    # ビルド
    make

    # テストプログラムの実行
    ./test_program

    # カバレッジ情報の収集とレポート生成
    echo "カバレッジ情報を取得中..."
    lcov --capture --directory . --output-file coverage.info
    genhtml coverage.info --output-directory coverage_report

    # カバレッジレポートの生成が成功した場合のメッセージ
    if [ $? -eq 0 ]; then
        echo "カバレッジレポートが生成されました。'coverage_report' ディレクトリ内の 'index.html' を開いて確認してください。"
    else
        echo "カバレッジレポートの生成に失敗しました。"
    fi
else
    # デフォルトの動作（カバレッジなしのテスト実行）
    make clean
    make
    ./test_program
    echo "カバレッジ情報は取得されませんでした。"
fi
