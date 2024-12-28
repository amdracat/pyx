import pyxel

class Game:
    def __init__(self):
        # Pyxelウィンドウの初期化
        pyxel.init(160, 120)

        # タイルマップとタイルセットの読み込み
        pyxel.load("test_resource.pyxres")

        # プレイヤーの初期位置
        self.player_x = 80
        self.player_y = 60

        # カメラの初期位置
        self.camera_x = 0
        self.camera_y = 0

        pyxel.run(self.update, self.draw)
    
    def update(self):
        # プレイヤーの移動処理
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y -= 1
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y += 1
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += 1
        
        # カメラの位置をプレイヤーの位置に合わせる
        self.camera_x = self.player_x - pyxel.width // 2
        self.camera_y = self.player_y - pyxel.height // 2

        # ゲーム終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    
    def draw(self):
        # 画面のクリア
        pyxel.cls(0)

        # タイルマップの描画（カメラの位置を考慮）
        pyxel.bltm(0, 0, 0, self.camera_x, self.camera_y, pyxel.width, pyxel.height)

        # プレイヤーの描画
        pyxel.rect(self.player_x - self.camera_x, self.player_y - self.camera_y, 8, 8, 9)
        
        # その他の描画処理
        pyxel.text(5, 5, "Use WASD to move. Press Q to quit.", 7)

# ゲームの実行
Game()
