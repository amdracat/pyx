import pyxel
from fire import Fire
from musicMainGame import MusicMainGame
from crossKey import CrossKey

class StateStart:
    def __init__(self):
        self.fires = [Fire() for _ in range(8)]  # Fireオブジェクトをリストで管理
        #pyxel.mouse(True) #
        self.visible=False
        self.cross=CrossKey()
        self.pos=0

    def set_is_visible(self,visible):
        self.visible=visible
        if self.visible:
            self.pos=0

    def is_visible(self):
        return self.visible

    def is_goto_start(self):
        if self.pos==0:
            return True
        return False

    def is_goto_score(self):
        if self.pos==1:
            return True
        return False

    def update(self):
        if not self.visible:
            return
        if pyxel.btnp(pyxel.KEY_DOWN)or ( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and  self.cross.mouseDown()):
            if self.pos < 2:
                self.pos=self.pos+1
        if pyxel.btnp(pyxel.KEY_UP)or ( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and  self.cross.mouseUp()):
            if 0 < self.pos :
                self.pos=self.pos-1

        if pyxel.btnp(pyxel.KEY_RETURN) or ( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and  self.cross.mouseCenter()):
            if self.pos==2:
                pyxel.quit()
            self.set_is_visible(False)

        for i, fire in enumerate(self.fires):
            fire.update()
            if fire.isEnd():
                self.fires[i] = Fire()  # 再生成

    def draw(self):
        if not self.visible:
            return
        pyxel.blt(75,100, 1,13,0,75, 15,100)
        if self.pos==0:
            playCol=pyxel.frame_count % 16
            scoreCol=13
            exitCol=13
        elif self.pos==1:
            playCol=13
            scoreCol=pyxel.frame_count % 16
            exitCol=13
        else:
            playCol=13
            exitCol=pyxel.frame_count % 16
            scoreCol=13
        pyxel.text(90, 130, "PLAY",  playCol)
        pyxel.text(90, 140, "SCORE", scoreCol)
        pyxel.text(90, 150, "EXIT", exitCol)
        
        #pyxel.rectb(80, 120, 40, 20, 1)
        #pyxel.rectb(80, 150, 40, 20, 1)
        for fire in self.fires:
            fire.draw()
        self.cross.draw()
