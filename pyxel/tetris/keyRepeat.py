import pyxel


class KeyRepeat:
    def __init__(self,key1,key2,firstDelay,repeat,ufunc):
        self.keyType1=key1
        self.keyType2=key2
        self.key_delay = firstDelay
        self.key_repeat = repeat
        self.func = ufunc
        self.count=0
    
    def update(self):
        if pyxel.btn(self.keyType1) or pyxel.btn(self.keyType2):
            self.count += 1
            if self.count == 1 or (self.count > self.key_delay )and ((self.count - self.key_delay) % self.key_repeat == 0):
                self.func()
        else:
            self.count = 0  # キーが離されたらリセット
