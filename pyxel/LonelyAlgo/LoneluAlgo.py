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

    def __init__(self,num,color):
        self.isPlace=False

        self.num = num
        self.color=color
        self.hold=False
        self.isVisible=False
        self.isOpen=False
        self.x_map=0
        self.y_map=0

        self.width = 16
        self.height = 24
        self.flip_frame = 0
        self.is_flipping = False
        self.isMoveOnlyX=False
        self.isMoveAll=True
        self.allCards = []

    def getCardInfo(self):
        return self.num ,self.color
    #以下の疑似コードをコードにして。疑似コード部は「疑似コード」と記載する
    def set_position_common(self, x, y,init):

        if not self.isOpen and not init:
            x, y = self.adjust_view_position_and_make_map_position(x, y)
            if y <= self.Y_SIZE*(8) :
                self.center = self.Position(x, y)
            else:
                self.center = self.Position(x, self.Y_SIZE*(8) )
            #print(f"{x} {y}")
            self.vertices = self.calculate_vertices(self.center)

        else:
            x, y = self.adjust_view_position_and_make_map_position(x, y)
            if self.isMoveOnlyX:

                arrSameY = []
                for card in self.allCards:
                    if card.center.y == self.center.y and not self.isSame(card):
                        arrSameY.append(card)


                
                arrSameY.sort(key=lambda card: card.center.x)
                if len(arrSameY) == 0:
                    self.center = self.Position(x, self.center.y)

                elif len(arrSameY) == 1:
                    if x < arrSameY[0].center.x:
                        self.center = self.Position(x, self.center.y)
                    else:
                        self.center = self.Position(arrSameY[0].center.x, self.center.y)
                else:
                    
                    for i in range(len(arrSameY) - 1):
                        #print(f"{arrSameY[i].center.x} {arrSameY[i].num} {self.center.x } {x} {arrSameY[i+1].center.x} {arrSameY[i+1].num} ")
                        if arrSameY[i].center.x < self.center.x < arrSameY[i + 1].center.x:
                            if arrSameY[i].center.x < x < arrSameY[i + 1].center.x:
                                self.center = self.Position(x, self.center.y)
                            else:
                                self.center = self.Position(self.center.x, self.center.y)
                            break
                        elif self.center.x  < arrSameY[i].center.x and i==0:
                            if x  < arrSameY[i].center.x:
                                self.center = self.Position(x, self.center.y)
                            else:
                                self.center = self.Position(self.center.x, self.center.y)
                            break
                        elif arrSameY[i + 1].center.x < self.center.x and i == (len(arrSameY) - 2):
                            if arrSameY[i + 1].center.x < x :
                                self.center = self.Position(x, self.center.y)
                            else:
                                self.center = self.Position(self.center.x, self.center.y)
                            break  
            else:
                self.center = self.Position(x, y)
            #print(f"{x} {y}")

            self.vertices = self.calculate_vertices(self.center)

    def setPositionInitIdx(self, x, y):  # 0始まり
        self.set_position_common((x + 1) * self.X_SIZE, (y + 1) * self.Y_SIZE,True)


    def setPosition(self, x, y):  # 0始まり
        self.set_position_common(x, y,False)

    def setPositionIdx(self, x, y):  # 0始まり
        self.set_position_common((x + 1) * self.X_SIZE, (y + 1) * self.Y_SIZE ,False)

    def setVisible(self ,isVisble):
        self.isVisible=isVisble
    def isOpend(self):
        return self.isOpen
    def setisOpen(self ,isOpen):
        if not self.isOpen:
            self.isOpen=isOpen
            self.is_flipping = True
            self.flip_frame = 0
            self.isMoveOnlyX=True

    def getPosition(self):
        x = self.x_map # 0～8
        y = self.y_map # 0～9
        return x,y

    def calculate_vertices(self, center):
        return [
            self.Position(center.x - self.X_SIZE / 2, center.y - self.Y_SIZE / 2),  # Top-left
            self.Position(center.x + self.X_SIZE / 2, center.y - self.Y_SIZE / 2),  # Top-right
            self.Position(center.x - self.X_SIZE / 2, center.y + self.Y_SIZE / 2),  # Bottom-left
            self.Position(center.x + self.X_SIZE / 2, center.y + self.Y_SIZE / 2)   # Bottom-right
        ]
    def adjust_view_position_and_make_map_position(self, x, y):

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

        self.x_map=x//self.X_SIZE -1
        self.y_map=y//self.Y_SIZE -1
        

        #print(f"{self.x_map} { self.y_map}")
        return x, y

    def isSame(self,card):
        return card.num==self.num and card.color==self.color
    def update(self,allCard):
        if not self.isVisible:
            return 
        self.allCards =allCard
        if self.isTouch() and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.hold=True
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
            self.hold=False
        if self.hold:
            xOld,yOld=self.getPosition()
            self.setPosition( pyxel.mouse_x,pyxel.mouse_y )
            xAfter,yAfter=self.getPosition()
            for card in self.allCards:
                if not self.isSame(card):
                    x,y=card.getPosition()
                    if x==xAfter and y == yAfter:
                        self.setPositionIdx( xOld,yOld)
                        break

        
        if self.isOpen:
            if self.is_flipping:
                self.flip_frame += 1
                if self.flip_frame <= 5:
                    self.width = self.X_SIZE - (self.X_SIZE / 5) * self.flip_frame  # Width reduces to 0 over 5 frames
                elif self.flip_frame <= 10:
                    self.width = (self.X_SIZE / 5) * (self.flip_frame - 5)  # Width increases back to 16 over 5 frames
                else:
                    self.is_flipping = False



    def draw(self):
        if not self.isVisible:
            return
        if self.color == pyxel.COLOR_WHITE:
            sigCol= pyxel.COLOR_BLACK
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

        pyxel.rectb(self.vertices[0].x +1,self.vertices[0].y+1, self.X_SIZE-2, self.Y_SIZE-2, pyxel.COLOR_RED)
        pyxel.rectb(self.vertices[0].x - self.width // 2+self.X_SIZE//2+1, self.vertices[0].y+1, self.width-2, self.height-2, pyxel.COLOR_BLACK)
        if self.flip_frame > 5:
            # 表面を描く
            pyxel.rect(self.vertices[0].x- self.width // 2 + self.X_SIZE//2+2, self.vertices[0].y +2, self.width - 4, self.height - 4, fillViewColor)
            if self.width == self.X_SIZE:
                pyxel.text(self.vertices[0].x +6-l, self.vertices[0].y+10, str(self.num),sigCol)
        else:
            # 裏面を描く
            pyxel.rect(self.vertices[0].x - self.width // 2 +  self.X_SIZE//2 +2, self.vertices[0].y+2, self.width - 4, self.height - 4,fillViewColor)
    

    def isTouch(self):
        
        ret= ( self.vertices[0].x < pyxel.mouse_x < self.vertices[1].x and  self.vertices[0].y < pyxel.mouse_y < self.vertices[2].y)
        #print(f" {ret} {pyxel.mouse_x } {pyxel.mouse_y} { self.vertices[0].x  }  { self.vertices[1].x  }  { self.vertices[0].y  }  { self.vertices[2].y }")
        return ret


class Game:
    def __init__(self):

        pyxel.init(160, 256, title="algo Pyxel")
        self.allCard = []
        self.cards = [[None for _ in range(10)] for _ in range(9)]  # 9列10行の2次元配列を作成
        self.card_queue = deque()
        self.create_cards()
        pyxel.mouse(True) #
        self.grid=False
        self.drawCardBtn=Button(10,210,40,15,pyxel.COLOR_BLACK,"DARW",pyxel.COLOR_WHITE)
        self.openBtn=Button(10,230,40,15,pyxel.COLOR_BLACK,"OPEN",pyxel.COLOR_WHITE)
        #pyxel.load("tetris_resource.pyxres")
        self.draw_init_cards(8)
        pyxel.run(self.update, self.draw)

    def draw_init_cards(self,num):
        for i in range(num):  # キューから8枚取り出してリストに追加
            if self.card_queue:
                card=self.card_queue.popleft()
                card.setPositionIdx(4,i)
                card.setVisible(True)
                num,col=card.getCardInfo()
                print(f"No{i} {num} {col}")
                self.allCard.append(card)

    def create_cards(self):
        # カードを生成し、キューに追加
        for num in range(12):
            self.card_queue.append(Card(num, pyxel.COLOR_WHITE))
            self.card_queue.append(Card(num, pyxel.COLOR_BLACK))
        
        # カードをシャッフル
        random.shuffle(self.card_queue)


    def update(self):
        self.cards = [[None for _ in range(10)] for _ in range(9)] 
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_S):
            self.grid = not self.grid


        #配列
        for card in self.allCard:
            card.update(self.allCard)
            x,y=card.getPosition()
            self.cards[x][y]=card

        if self.drawCardBtn.update():
            if self.drawCardBtn.isOn:
                isDraw=True
                for card in self.allCard:
                    if not card.isOpend():
                        isDraw=False

                print(f"len:{len(self.card_queue)}")
                if self.cards[7][8]==None and isDraw:
                    if self.card_queue:
                        card=self.card_queue.popleft()
                        card.setPositionInitIdx(7,8)
                        card.setVisible(True)
                        self.allCard.append(card)
                else:
                    print("card exits")


        if self.openBtn.update():
            if self.openBtn.isOn:
                for card in self.allCard:
                    card.setisOpen(True)












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

        for card in self.allCard:
            card.draw()


        self.drawCardBtn.draw()
        self.openBtn.draw()


Game()
