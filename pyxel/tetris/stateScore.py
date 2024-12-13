import pyxel
from score import Score

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
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 5 < pyxel.mouse_x < 35 and  147 < pyxel.mouse_y < 160:
                if not self.del_check:
                    self.set_is_visible(False)
            elif 35 < pyxel.mouse_x < 65 and  147 < pyxel.mouse_y < 160:
                self.selectStart=False
                self.del_check = True
            elif 80 < pyxel.mouse_x < 100 and  107 < pyxel.mouse_y < 120:
                if self.del_check:
                    self.del_check=False
                    self.del_done=False
                    self.score_manager.clear_highscores()
            elif 105 < pyxel.mouse_x < 125 and  107 < pyxel.mouse_y < 120:
                if self.del_check:
                    self.del_check=False

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
        pyxel.rectb(5, 147,  30, 13, 1)
        pyxel.rectb(35, 147,  30, 13, 1)
        pyxel.rectb(80, 107,  20, 13, 1)
        pyxel.rectb(105, 107,  20, 13, 1)
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

