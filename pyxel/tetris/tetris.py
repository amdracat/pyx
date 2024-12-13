import pyxel

from stateMainGame import StateMainGame
from stateStart import StateStart
from score import Score
from musicMainGame import MusicMainGame



class StateScore:
    def __init__(self):
        self.visible=False
        self.selectStart=True
        self.score_manager = Score()
        self.del_check=False
        self.del_done=False

    def set_is_visible(self,visible):
        self.visible=visible
        if self.visible:
            self.selectStart=True
            self.del_check=False

    def is_visible(self):
        return self.visible
    def update(self):
        if not self.visible:
            return
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.selectStart:
                self.set_is_visible(False)
            else:
                if self.del_check:
                    if self.del_done:
                        self.score_manager.clear_highscores()
                    self.del_check=False
                    self.del_done=False
                else:
                    self.del_check = True

        if pyxel.btnp(pyxel.KEY_LEFT):
            if not self.del_check:
                self.selectStart=True
            else:
                self.del_done = True
        if pyxel.btnp(pyxel.KEY_RIGHT):
            if not self.del_check:
                self.selectStart=False
            else:
                self.del_done=False


    def draw(self):
        if not self.visible:
            return
        
        if self.del_check:
            scoreCol=13
        else:
            scoreCol=pyxel.COLOR_WHITE
        pyxel.text(10, 10, "Highscores:", scoreCol)
        for i, score in enumerate(self.score_manager.highscores):
            pyxel.text(10, 20 + i * 10, f"{i + 1}. {score}",scoreCol)


        if self.del_check:
            startCol=13
            deletaCol=13
        elif self.selectStart:
            startCol=pyxel.frame_count % 16
            deletaCol=13
        else:
            startCol=13
            deletaCol=pyxel.frame_count % 16

        pyxel.text(10, 150, "TITLE", startCol)
        pyxel.text(40, 150, "ERASE", deletaCol)

        if self.del_check:
            pyxel.text(90, 100, "Delete?", 7)
            if self.del_done:
                noCol=13
                yesCol=7
            else:
                noCol=7
                yesCol=13
            pyxel.text(85, 110, "YES", yesCol)
            pyxel.text(110, 110, "NO", noCol)


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
                    self.scoreGame=StateScore()
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
