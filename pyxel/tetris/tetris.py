import pyxel

from stateMainGame import StateMainGame


class Game:
    def __init__(self):
        self.viewState=1
        
        pyxel.init(220, 240, title="Tetris Pyxel")
        self.mainGame=StateMainGame()
        self.mainGame.set_is_visible(True)
        pyxel.load("tetris_resource.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.mainGame.update()

    def draw(self):
        pyxel.cls(0)
        self.mainGame.draw()

Game()
