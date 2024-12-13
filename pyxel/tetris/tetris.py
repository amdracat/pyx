import pyxel

from stateMainGame import StateMainGame
from stateStart import StateStart
from score import Score
from musicMainGame import MusicMainGame



class StateScore:
    def __init__(self):
        self.visible=False
        self.score_manager = Score()

    def set_is_visible(self,visible):
        self.visible=visible

    def is_visible(self):
        return self.visible
    def update(self):
        if not self.visible:
            return
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.set_is_visible(False)
    def draw(self):
        if not self.visible:
            return
        pyxel.text(10, 0, "SCORE", 7)
        pyxel.text(10, 10, "Highscores:", pyxel.COLOR_WHITE)
        for i, score in enumerate(self.score_manager.highscores):
            pyxel.text(10, 20 + i * 10, f"{i + 1}. {score}", pyxel.COLOR_WHITE)


class Game:
    def __init__(self):
        self.viewState=0
        # 使用例
        
        #self.score_manager.set_score(100)  # 新しいスコアをセット
        #print(self.score_manager.highscores)  # ハイスコアリストを表示
        pyxel.init(220, 240, title="Tetris Pyxel")
        self.music = MusicMainGame()
        self.music.music_start()
        self.mainGame=StateMainGame()
        self.startGame=StateStart()
        self.scoreGame=StateScore()
        self.startGame.set_is_visible(True)


        pyxel.load("tetris_resource.pyxres")
        pyxel.run(self.update, self.draw)

        




    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.viewState==0:
            self.startGame.update()
            if not self.startGame.is_visible():
                if self.startGame.is_goto_start():
                    self.viewState=1
                    self.mainGame.set_is_visible(True)
                elif self.startGame.is_goto_score():
                    self.viewState=2
                    #self.scoreGame=StateScore()
                    self.scoreGame.set_is_visible(True)

        elif self.viewState==1:
            self.mainGame.update()
            if not self.mainGame.is_visible():
                self.viewState=0
                self.startGame.set_is_visible(True)
        elif self.viewState==2:
            self.scoreGame.update()
            if not self.scoreGame.is_visible():
                self.viewState=0
                #del(self.scoreGame)
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
