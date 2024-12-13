import pyxel

from stateMainGame import StateMainGame
from stateStart import StateStart
from stateScore import StateScore
from musicMainGame import MusicMainGame

class Game:
    def __init__(self):
        self.viewState=0

        pyxel.init(220, 240, title="Tetris Pyxel")

        self.music = MusicMainGame()
        self.music.music_start()
        self.mainGame=StateMainGame()
        self.startGame=StateStart()

        #初期画面
        self.startGame.set_is_visible(True)

        pyxel.load("tetris_resource.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # 開始画面
        if self.viewState==0:
            self.startGame.update()
            if not self.startGame.is_visible():
                if self.startGame.is_goto_start():
                    self.viewState=1
                    self.mainGame.set_is_visible(True)
                elif self.startGame.is_goto_score():
                    self.viewState=2
                    self.scoreGame=StateScore()
                    self.scoreGame.set_is_visible(True)

        #ゲーム画面
        elif self.viewState==1:
            self.mainGame.update()
            if not self.mainGame.is_visible():
                self.viewState=0
                self.startGame.set_is_visible(True)

        #スコア画面
        elif self.viewState==2:
            self.scoreGame.update()
            if not self.scoreGame.is_visible():
                self.viewState=0
                del(self.scoreGame)
                self.startGame.set_is_visible(True)

    def draw(self):
        pyxel.cls(0)
        if self.viewState==0:
            self.startGame.draw()
        elif self.viewState==1:
            self.mainGame.draw()
        elif self.viewState==2:
            self.scoreGame.draw()

Game()
