import pyxel
import copy
import random
from collections import deque


class Button:
    def __init__(self,x,y,w,h,color,string,string_color):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.color=color
        self.string=string
        self.string_color=string_color
        self.isOn=False
    
    def update(self):
        if self.isOn:
            now=True
        else:
            now=False
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            if self.isTouch():
                self.isOn=True
            else:
                self.isOn=False
        else:
            self.isOn=False
        if now != self.isOn:
            return True
        else:
            return False

    def draw(self):
        col=pyxel.COLOR_WHITE
        if self.isOn:
                col=col=pyxel.COLOR_BLACK

        pyxel.rectb(self.x,self.y, self.w, self.h, col)
        pyxel.rect(self.x+1,self.y+1, self.w-2, self.h-2, self.color)
        text = f"{self.string}"
        text_width = pyxel.FONT_WIDTH * len(text)
        pyxel.text(self.x + (self.w/2 - text_width/2),self.y+self.h/2-3, self.string, self.string_color)

    def isTouch(self):
        return ( self.x < pyxel.mouse_x < self.x+self.w and  self.y < pyxel.mouse_y < self.y+self.h)



class Card:
    X_SIZE=16
    Y_SIZE=24

    class Position:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    def __init__(self,x,y,num,color):
        self.isPlace=False
        x, y = self.adjust_position(x, y)
        self.center = self.Position(x, y)
        self.num = num
        self.color=color
        self.hold=False
        self.vertices = [
            self.Position(self.center.x - self.X_SIZE / 2, self.center.y - self.Y_SIZE / 2),  # Top-left
            self.Position(self.center.x + self.X_SIZE / 2, self.center.y - self.Y_SIZE / 2),  # Top-right
            self.Position(self.center.x - self.X_SIZE / 2, self.center.y + self.Y_SIZE / 2),  # Bottom-left
            self.Position(self.center.x + self.X_SIZE / 2, self.center.y + self.Y_SIZE / 2)   # Bottom-right
        ]
        self.viewCenter=copy.deepcopy(self.center )
        self.viewVertices=copy.deepcopy(self.vertices)
    def getCardInfo(self):
        return self.num ,self.color
    def setPosition(self, x, y):
        x, y = self.adjust_position(x, y)
        self.center = self.Position(x, y)
        self.vertices = self.calculate_vertices(self.center)
        self.viewCenter=copy.deepcopy(self.center )
        self.viewVertices=copy.deepcopy(self.vertices)
    def place_card(self):
        self.isPlace=True
    def setPositionView(self, x, y):
        x, y = self.adjust_position(x, y)
        if self.isPlace:
            self.viewCenter = self.Position(x, self.viewCenter.y)
        else:
            self.viewCenter = self.Position(x, y)

        self.viewVertices = self.calculate_vertices(self.viewCenter)

    def calculate_vertices(self, center):
        return [
            self.Position(center.x - self.X_SIZE / 2, center.y - self.Y_SIZE / 2),  # Top-left
            self.Position(center.x + self.X_SIZE / 2, center.y - self.Y_SIZE / 2),  # Top-right
            self.Position(center.x - self.X_SIZE / 2, center.y + self.Y_SIZE / 2),  # Bottom-left
            self.Position(center.x + self.X_SIZE / 2, center.y + self.Y_SIZE / 2)   # Bottom-right
        ]
    def fixPosition(self):
        if 16<=self.viewCenter.x<=16*9 and 24<=self.viewCenter.y<=24*8:
            self.center=copy.deepcopy(self.viewCenter)
            self.vertices = copy.deepcopy(self.viewVertices)
    def isOut(self):
        if 16<=self.center.x<=16*9 and 24<=self.center.y<=24*8:
            return False
        return True
    def getCenterPosition(self):
        return self.center.x , self.center.y
    def getCenterViewPosition(self):
        return self.viewCenter.x , self.viewCenter.y

    def isMove(self):
        for i in range(4):
            if self.vertices[i].x != self.viewVertices[i].x or self.vertices[i].y != self.viewVertices[i].y:
                return True
        return False


    def adjust_position(self, x, y):

        # 補正後の値が範囲内に収まるように調整
        half_width = self.X_SIZE / 2
        half_height = self.Y_SIZE / 2

        if x - half_width < 1:
            x = 1 + half_width
        elif x + half_width > 159:
            x = 159 - half_width

        if y - half_height < 1:
            y = 1 + half_height
        elif y + half_height > 255:
            y = 255 - half_height

        x = round(x / self.X_SIZE) * self.X_SIZE
        y = round(y / self.Y_SIZE) * self.Y_SIZE

        #print(f"{x} {y}")
        return x, y

    def isTouch(self):
        #print(f"   { self.vertices[0].x  }  { self.vertices[1].x  }  { self.vertices[0].y  }  { self.vertices[2].y }")
        return ( self.vertices[0].x < pyxel.mouse_x < self.vertices[1].x and  self.vertices[0].y < pyxel.mouse_y < self.vertices[2].y)


    def isTouchView(self):
        #print(f"   { self.vertices[0].x  }  { self.vertices[1].x  }  { self.vertices[0].y  }  { self.vertices[2].y }")
        return ( self.viewVertices[0].x < pyxel.mouse_x < self.viewVertices[1].x and  self.viewVertices[0].y < pyxel.mouse_y < self.viewVertices[2].y)
    
    def update(self, any_card_move,any_card_held):
        if self.isTouch() and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.setPositionView( pyxel.mouse_x,pyxel.mouse_y )
        if self.isTouchView() and (( not any_card_held and not any_card_move )or self.isMove()):
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                self.hold=True
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
            self.hold=False
        if self.hold:
            self.setPositionView( pyxel.mouse_x,pyxel.mouse_y )


    def draw(self):
        if self.color == pyxel.COLOR_WHITE:
            sigCol= pyxel.COLOR_NAVY
            fillColor=pyxel.COLOR_WHITE
            fillViewColor=pyxel.COLOR_WHITE
        else:
            sigCol= pyxel.COLOR_WHITE
            fillColor=pyxel.COLOR_BLACK
            fillViewColor=pyxel.COLOR_BLACK

        if self.isPlace:
            wakuCol=pyxel.COLOR_LIGHT_BLUE
        else:
            wakuCol=pyxel.COLOR_RED
        
        l=len( f"{self.num}")
        if l==1:
            l=0
        pyxel.rect(self.vertices[0].x,self.vertices[0].y, self.X_SIZE, self.Y_SIZE, fillColor)
        pyxel.rectb(self.vertices[0].x,self.vertices[0].y, self.X_SIZE, self.Y_SIZE, pyxel.COLOR_BLACK)
        pyxel.rect(self.viewVertices[0].x+1,self.viewVertices[0].y+1, self.X_SIZE-2, self.Y_SIZE-2, fillViewColor)
        pyxel.rectb(self.viewVertices[0].x+1,self.viewVertices[0].y+1, self.X_SIZE-2, self.Y_SIZE-2, wakuCol)
        pyxel.text(self.center.x -  pyxel.FONT_WIDTH/2 - l, self.center.y-2, f"{self.num}",sigCol)
        pyxel.text(self.viewCenter.x-pyxel.FONT_WIDTH/2- l, self.viewCenter.y-2, f"{self.num}",sigCol)

class Game:
    def __init__(self):

        pyxel.init(160, 256, title="algo Pyxel")
        self.cards = []
        self.card_queue = deque()
        self.create_cards()
        pyxel.mouse(True) #
        self.grid=False
        self.drawCardBtn=Button(10,210,40,15,pyxel.COLOR_BLACK,"DARW",pyxel.COLOR_WHITE)
        self.placeBtn=Button(10,230,40,15,pyxel.COLOR_BLACK,"PLACE",pyxel.COLOR_WHITE)
        #pyxel.load("tetris_resource.pyxres")
        self.draw_init_cards(8)
        pyxel.run(self.update, self.draw)

    def draw_init_cards(self,num):
        for i in range(num):  # キューから8枚取り出してリストに追加
            if self.card_queue:
                card=self.card_queue.popleft()
                card.setPosition(80,24+24*i)
                card.place_card()
                num,col=card.getCardInfo()
                #print(f"No{i} {num} {col}")
                self.cards.append(card)

    def create_cards(self):
        # カードを生成し、キューに追加
        for num in range(12):
            self.card_queue.append(Card(0, 0, num, pyxel.COLOR_WHITE))
            self.card_queue.append(Card(0, 0, num, pyxel.COLOR_BLACK))
        
        # カードをシャッフル
        random.shuffle(self.card_queue)

    def check_overlap(self, vertices):
        for card in self.cards:
            if vertices.getCenterViewPosition()==card.getCenterPosition():
                return True
        return False

    def update(self):
        any_card_move = any(card.isMove() for card in self.cards)
        any_card_held = any(card.hold for card in self.cards)
        any_card_out = any(card.isOut() for card in self.cards)
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_S):
            self.grid = not self.grid
        if pyxel.btnp(pyxel.KEY_A):
            self.cards.append(Card(100, 100, 1, pyxel.COLOR_WHITE))
        if pyxel.btnp(pyxel.KEY_R):
            self.cards.append(Card(100, 100, 1, pyxel.COLOR_BLACK))
        if pyxel.btnp(pyxel.KEY_E):
            for mCard in self.cards:
                if mCard.isMove():
                    if not self.check_overlap(mCard):
                        mCard.fixPosition()

        for card in self.cards:
            card.update(any_card_move,any_card_held)

        if self.drawCardBtn.update():
            if self.drawCardBtn.isOn:
                if not any_card_out:
                    card=self.card_queue.popleft()
                    card.setPosition(120,220)
                    #num,col=card.getCardInfo()
                    #print(f"No{i} {num} {col}")
                    self.cards.append(card)
                else:
                    print("cant")

        if self.placeBtn.update():
            if self.placeBtn.isOn:
                for mCard in self.cards:
                    if mCard.isMove():
                        if not self.check_overlap(mCard):
                            mCard.fixPosition()





    def draw(self):
        pyxel.cls(pyxel.COLOR_WHITE)
        if self.grid:
            # 垂直方向の直線を描画
            for x in range(0, 180, 16):
                if 20 <x <160:
                    pyxel.line(x-8, 12, x-8, 12+24*8, pyxel.COLOR_NAVY)
            # 水平方向の直線を描画
            for y in range(0, 270, 24):
                if 20 < y <240:
                    pyxel.line(24, y-12, 160-24, y-12, pyxel.COLOR_NAVY)


        for card in self.cards:
            card.draw()

        self.drawCardBtn.draw()
        self.placeBtn.draw()


Game()
