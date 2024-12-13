import pyxel
from fire import Fire
from musicMainGame import MusicMainGame

class StateStart:
    def __init__(self):
        self.fires = [Fire() for _ in range(8)]  # Fireオブジェクトをリストで管理
        
        self.selectStart=True
        self.visible=False

    def set_is_visible(self,visible):
        self.visible=visible
        if self.visible:
            self.selectStart=True

    def is_visible(self):
        return self.visible

    def is_goto_start(self):
        return self.selectStart

    def is_goto_score(self):
        if not self.selectStart:
            return True
        return False

    def update(self):
        if not self.visible:
            return
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.selectStart=False
        if pyxel.btnp(pyxel.KEY_UP):
            self.selectStart=True

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.set_is_visible(False)

        for i, fire in enumerate(self.fires):
            fire.update()
            if fire.isEnd():
                self.fires[i] = Fire()  # 再生成

    def draw(self):
        if not self.visible:
            return
        pyxel.blt(75,100, 1,13,0,75, 15,100)
        if self.selectStart:
            playCol=pyxel.frame_count % 16
            scoreCol=13
        else:
            playCol=13
            scoreCol=pyxel.frame_count % 16
        pyxel.text(90, 130, "PLAY",  playCol)
        pyxel.text(90, 140, "SCORE", scoreCol)
        
        for fire in self.fires:
            fire.draw()
