import pyxel
import random

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
STAGE_WIDTH = 1000
STAGE_HEIGHT = 1000
PLAYER_SPEED = 2
JUMP_HEIGHT = 50

class Game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="2D Map")
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2
        self.player_jump_y = 0
        self.jumping = False
        self.obstacles = self.generate_obstacles(50)  # 障害物をランダムに生成
        pyxel.run(self.update, self.draw)

    def generate_obstacles(self, count):
        obstacles = []
        for _ in range(count):
            x = random.randint(0, STAGE_WIDTH - 16)
            y = random.randint(0, STAGE_HEIGHT - 16)
            obstacles.append((x, y, 16, 16))
        return obstacles

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y += PLAYER_SPEED
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.jumping:
            self.jumping = True
            self.player_jump_y = self.player_y
        
        # ジャンプ処理
        if self.jumping:
            self.player_y = self.player_jump_y - JUMP_HEIGHT
            self.jumping = False

        # ステージの境界を超えないように制限
        self.player_x = max(0, min(self.player_x, STAGE_WIDTH - 16))
        self.player_y = max(0, min(self.player_y, STAGE_HEIGHT - 16))

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        # ステージ全体を描画
        for x, y, w, h in self.obstacles:
            pyxel.rect(x, y, w, h, pyxel.COLOR_RED)

        # プレイヤーを描画
        pyxel.rect(self.player_x, self.player_y, 16, 16, pyxel.COLOR_NAVY)

Game()
