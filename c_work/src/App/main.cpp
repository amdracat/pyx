
/*
#include <stdio.h>
int main(){
    printf("sssss\n");

#if defined UNIT_TEST_BUILD
    printf("test\n");
#endif

    return 0;
}
*/

#include "dx/DxLib.h"
#include "log.h"
#include "assert.h"
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {

    // DXライブラリの初期化
    ChangeWindowMode(TRUE);    // ウィンドウモードに変更
    SetGraphMode(200, 200, 32); // ウィンドウサイズを200x200に設定
    if (DxLib_Init() == -1) {  // DXライブラリの初期化処理
        return -1;             // 初期化に失敗した場合
    }


    // ログスレッドの開始
    start_log_thread();

    // 四角形の初期位置
    int x = 90;
    int y = 90;
    const int size = 20; // 四角形のサイズ

    // 描画先を裏画面に設定
    SetDrawScreen(DX_SCREEN_BACK);

    // メインループ
    while (ProcessMessage() == 0 && ClearDrawScreen() == 0) {
        // キー入力処理
        if (CheckHitKey(KEY_INPUT_UP)) y -= 2;
        if (CheckHitKey(KEY_INPUT_DOWN)) y += 2;
        if (CheckHitKey(KEY_INPUT_LEFT)) x -= 2;
        if (CheckHitKey(KEY_INPUT_RIGHT)) x += 2;

        // 四角形を描画
        DrawBox(x, y, x + size, y + size, GetColor(255, 255, 255), TRUE);


        // 例として、四角形がウィンドウの外に出た場合にアサートを発生させる
        ASSERT(x >= 0 && x + size <= 200);
        ASSERT(y >= 0 && y + size <= 200);

        // 裏画面の内容を表画面に反映
        ScreenFlip();
    }

    // DXライブラリの終了処理
    DxLib_End();

    // ログスレッドの停止
    stop_log_thread();
    
    return 0;
}
