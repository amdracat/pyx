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

    def __init__(self,num,color,nHaichi):
        self.isPlace=False
        self.nHaichi=nHaichi
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
        self.count=0
        self.isCantOpen = False
        self.warn_count = 0


    def setisCantOpen(self):
        self.warn_count = 0
        self.isCantOpen=True
    def getCardInfo(self):
        return self.num ,self.color
    def set_position_common(self, x, y,init):

        if not self.isOpen and not init:
            x, y = self.adjust_view_position_and_make_map_position(x, y)
            #print(f"{x} {y}")
            
            if y <= self.Y_SIZE*(self.nHaichi) or ((x//self.X_SIZE -1)==7 and (y//self.Y_SIZE -1)==8) :
                self.center = self.Position(x, y)
                self.x_map=x//self.X_SIZE -1
                self.y_map=y//self.Y_SIZE -1
            else:
                self.center = self.Position(x, self.Y_SIZE*(self.nHaichi) )
                self.x_map=x//self.X_SIZE -1
                self.y_map=self.Y_SIZE*(self.nHaichi) //self.Y_SIZE -1
            #print(f"{self.center.x} {self.center.y} { self.x_map} { self.y_map}")
            self.vertices = self.calculate_vertices(self.center)

        else:
            #
            x, y = self.adjust_view_position_and_make_map_position(x, y)
            if self.isMoveOnlyX:
                arrSameY = []
                for card in self.allCards:
                    if card.center.y == self.center.y and not self.isSame(card):
                        arrSameY.append(card)


                
                arrSameY.sort(key=lambda card: card.center.x)
                if len(arrSameY) == 0:
                    self.x_map=x//self.X_SIZE -1
                    self.y_map=self.center.y//self.Y_SIZE -1
                    self.center = self.Position(x, self.center.y)

                elif len(arrSameY) == 1:
                    if self.center.x < arrSameY[0].center.x:
                        if x < arrSameY[0].center.x:
                            self.center = self.Position(x, self.center.y)
                            self.x_map=x//self.X_SIZE -1
                            self.y_map=self.center.y//self.Y_SIZE -1
                        else:
                            self.center = self.Position(self.center.x, self.center.y)
                            self.x_map=self.center.x//self.X_SIZE -1
                            self.y_map=self.center.y//self.Y_SIZE -1
                    else:
                        if arrSameY[0].center.x < x:
                            self.center = self.Position(x, self.center.y)
                            self.x_map=x//self.X_SIZE -1
                            self.y_map=self.center.y//self.Y_SIZE -1
                        else:
                            self.center = self.Position(self.center.x, self.center.y)
                            self.x_map=self.center.x//self.X_SIZE -1
                            self.y_map=self.center.y//self.Y_SIZE -1
                else:
                    for i in range(len(arrSameY) - 1):
                        #print(f"{arrSameY[i].center.x} {arrSameY[i].num} {self.center.x } {x} {arrSameY[i+1].center.x} {arrSameY[i+1].num} ")
                        if arrSameY[i].center.x < self.center.x < arrSameY[i + 1].center.x:
                            if arrSameY[i].center.x < x < arrSameY[i + 1].center.x:
                                self.center = self.Position(x, self.center.y)
                                self.x_map=x//self.X_SIZE -1
                                self.y_map=self.center.y//self.Y_SIZE -1
                            else:
                                self.center = self.Position(self.center.x, self.center.y)
                                self.x_map=self.center.x//self.X_SIZE -1
                                self.y_map=self.center.y//self.Y_SIZE -1
                            break
                        elif (self.center.x  < arrSameY[i].center.x) and i==0:
                            if x  < arrSameY[i].center.x:
                                self.center = self.Position(x, self.center.y)
                                self.x_map=x//self.X_SIZE -1
                                self.y_map=self.center.y//self.Y_SIZE -1
                            else:
                                self.center = self.Position(self.center.x, self.center.y)
                                self.x_map=self.center.x//self.X_SIZE -1
                                self.y_map=self.center.y//self.Y_SIZE -1
                            break
                        elif (arrSameY[i + 1].center.x < self.center.x) and i == (len(arrSameY) - 2):
                            if arrSameY[i + 1].center.x < x :
                                self.center = self.Position(x, self.center.y)
                                self.x_map=x//self.X_SIZE -1
                                self.y_map=self.center.y//self.Y_SIZE -1
                            else:
                                self.center = self.Position(self.center.x, self.center.y)
                                self.x_map=self.center.x//self.X_SIZE -1
                                self.y_map=self.center.y//self.Y_SIZE -1
                            break  
            else:
                #初回
                self.center = self.Position(x, y)
                self.x_map=x//self.X_SIZE -1
                self.y_map=y//self.Y_SIZE -1
            #print(f"{x} {y}")

            self.vertices = self.calculate_vertices(self.center)

    #初期配置のみ
    def setPositionInitIdx(self, x, y):  # 0始まり
        self.set_position_common((x + 1) * self.X_SIZE, (y + 1) * self.Y_SIZE,True)

    #マウス移動
    def setPosition(self, x, y):  # 0始まり
        self.set_position_common(x, y,False)

    #特殊用途
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
      

        #print(f"{self.x_map} { self.y_map}")
        return x, y

    def isSame(self,card):
        return card.num==self.num and card.color==self.color
    def update(self,allCard):
        if not self.isVisible:
            return 
        self
        #ddd=False
        self.allCards =allCard
        if self.isTouch() and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.hold=True
            self.isCantOpen=False
            #xOld,yOld=self.getPosition()
            #print(f"{xOld} {yOld}")
            #ddd=True
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
            self.hold=False
        if self.hold:
            xOld,yOld=self.getPosition()
            #if yOld > self.Y_SIZE*(8) :
            self.setPosition( pyxel.mouse_x,pyxel.mouse_y )
            xAfter,yAfter=self.getPosition()
            #self.count=self.count+1
            #if self.count >30:
            #    self.count=0
            #if ddd:
            #    print(f"{xOld} {yOld} -> {xAfter} {yAfter} {pyxel.mouse_x} {pyxel.mouse_y}")
            for card in self.allCards:
                if not self.isSame(card):
                    x,y=card.getPosition()
                    if x==xAfter and y == yAfter:
                        self.setPositionIdx( xOld,yOld)
                        #print("back")
                        break

        if self.isCantOpen:
            self.warn_count =self.warn_count +1
            if self.warn_count > 30:
                #self.isOpen=False
                self.isCantOpen=False

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


        #pyxel.rectb(self.vertices[0].x +1,self.vertices[0].y+1, self.X_SIZE-2, self.Y_SIZE-2, pyxel.COLOR_RED)
        red_ranges = [(0, 2), (4, 6), (8, 10), (12, 14), (16, 18), (20, 22), (24, 26), (28, 30)]
        if self.isCantOpen:
            # warn_countが赤色にする範囲に含まれているかチェック
            if any(start <= self.warn_count < end for start, end in red_ranges):
                wakuColor = pyxel.COLOR_RED
            else:
                wakuColor = pyxel.COLOR_WHITE
        else:
            wakuColor=pyxel.COLOR_BLACK
        
        pyxel.rectb(self.vertices[0].x - self.width // 2+self.X_SIZE//2+1, self.vertices[0].y+1, self.width-2, self.height-2, wakuColor)
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

class StateMain:
    def __init__(self,tateNum,zanki):
        self.nHaichi=tateNum
        self.count=0
        self.sec=0
        self.frame_count = 0
        self.start=False
        self.viewStart=False
        self.allCard = []
        self.cards = [[None for _ in range(10)] for _ in range(9)]  # 9列10行の2次元配列を作成
        self.card_queue = deque()
        self.create_cards()
        self.grid=False
        self.done=False
        self.miss=False
        self.zanki=zanki
        self.drawCardBtn=Button(5,205,40,15,pyxel.COLOR_BLACK,"DARW",pyxel.COLOR_WHITE)
        self.openBtn=Button(5,220,40,15,pyxel.COLOR_BLACK,"OPEN",pyxel.COLOR_WHITE)
        self.newBtn=Button(5,235,40,10,pyxel.COLOR_BLACK,"NEW GAME",pyxel.COLOR_WHITE)
        self.settingBtn=Button(5,245,40,10,pyxel.COLOR_BLACK,"SETTING",pyxel.COLOR_WHITE)
        #pyxel.load("tetris_resource.pyxres")
        self.draw_init_cards(self.nHaichi)
        self.is_visible=False
        self.ng_card=None
        self.del_count=0

    def isVisible(self):
        return self.is_visible

    def setisVisible(self,isVisible):
        self.is_visible=isVisible

    def draw_init_cards(self,num):
        for i in range(num):  # キューから8枚取り出してリストに追加
            if self.card_queue:
                card=self.card_queue.popleft()
                card.setPositionIdx(4,i)
                card.setVisible(True)
                num,col=card.getCardInfo()
                #print(f"No{i} {num} {col}")
                self.allCard.append(card)

    def create_cards(self):
        # カードを生成し、キューに追加
        for num in range(12):
        #for num in range(6):
            self.card_queue.append(Card(num, pyxel.COLOR_WHITE,self.nHaichi))
            self.card_queue.append(Card(num, pyxel.COLOR_BLACK,self.nHaichi))
        
        # カードをシャッフル
        random.shuffle(self.card_queue)

    def isCardOpen(self,num,color):
        for card in self.allCard:
            refNum,refColor=card.getCardInfo()
            if refNum==num and refColor==color:
                if card.isOpend():
                    return True
                else:
                    return False
        return False


    def checkGame(self):
        for x in range(9):
            for y in range(10):
                if self.cards[x][y] is not None:
                    card = self.cards[x][y]
                    num, color = card.getCardInfo()
                    if not self.is_valid_card_position(x, y, num, color):
                        return False
        return True

    def is_valid_card_position(self, x, y, num, color):
        # y方向に並んでいるカードの数をカウント
        count = self.count_cards_in_line(y)
        if count > self.nHaichi:
            return False

        # 数字が小さい順であることを確認
        previous_num = -1
        previous_color = None
        for i in range(9):
            if self.cards[i][y] is not None:
                current_card = self.cards[i][y]
                current_num, current_color = current_card.getCardInfo()
                if current_num < previous_num:
                    return False
                elif current_num == previous_num:
                    if previous_color == pyxel.COLOR_WHITE and current_color == pyxel.COLOR_BLACK:
                        return False
                previous_num = current_num
                previous_color = current_color

        return True




    def can_open_card(self, x, y):
        # カードをオープンするための条件を定義
        # 例: self.nHaichiの値に基づいてカードをオープンするかどうかを決定
        if self.nHaichi == 8 and self.count_cards_in_line(y) <= 3:
            return True
        elif self.nHaichi == 7 and self.count_cards_in_line(y) <= 4:
            return True
        elif self.nHaichi == 6 and self.count_cards_in_line(y) <= 4:
            return True
        elif self.nHaichi == 5 and self.count_cards_in_line(y) <= 5:
            return True
        elif self.nHaichi == 4 and self.count_cards_in_line(y) <= 6:
            return True
        elif self.nHaichi == 3 and self.count_cards_in_line(y) <= 8:
            return True
        return False

    def count_cards_in_line(self, y):
        # 指定された高さラインにあるカードの数をカウント
        count = 0
        for x in range(9):
            if self.cards[x][y] is not None:
                count += 1
        return count


    def openCard(self):
        retCard=None
        for card in self.allCard:
            if self.cards[7][8]==None:
                if not self.start:
                    self.start=True
                    self.count=0
                    self.sec=0
                    self.frame_count=0
                    self.viewStart=True

                for x in range(9):
                    for y in range(10):
                        if self.cards[x][y] is not None:
                            card = self.cards[x][y]
                            #num, color = card.getCardInfo()
                            # ここでカードをオープンする条件をチェック
                            if self.can_open_card(x, y):
                                card.setisOpen(True)
                                retCard=card
                            else:
                                if not card.isOpend():
                                    card.setisCantOpen()
        return retCard



                            



    def update(self):
        if not self.is_visible:
            return
        self.cards = [[None for _ in range(10)] for _ in range(9)] 

        if pyxel.btnp(pyxel.KEY_S):
            self.grid = not self.grid


        #配列
        for card in self.allCard:
            card.update(self.allCard)
            x,y=card.getPosition()
            self.cards[x][y]=card

        if self.drawCardBtn.update():
            if self.drawCardBtn.isOn and not self.miss:
                isDraw=True
                for card in self.allCard:
                    if not card.isOpend():
                        isDraw=False

                #print(f"len:{len(self.card_queue)}")
                if self.cards[7][8]==None and isDraw:
                    if self.card_queue:
                        card=self.card_queue.popleft()
                        card.setPositionInitIdx(7,8)
                        card.setVisible(True)
                        self.allCard.append(card)
                #else:
                #    print("card exits")

        self.frame_count += 1
        if self.openBtn.update():
            if self.openBtn.isOn and not self.miss:
                opencard = self.openCard()
                ret = self.checkGame()
                leng = len(self.card_queue)
                print(f"check {ret}  {leng}")
                if ret == False:
                    self.zanki= self.zanki-1
                    if self.zanki == 0:
                        self.miss=True
                    else:
                        self.ng_card=opencard
                        self.del_count=0
                        opencard.setisCantOpen()
                        
                if leng == 0:
                    print("end!")
                    

        if self.newBtn.update():
            if self.newBtn.isOn:
                print("p")
                self.is_visible=False

        if self.settingBtn.update() and not self.miss:
            if self.settingBtn.isOn:
                print("s")

        if self.ng_card != None:
            self.del_count=self.del_count+1
            if self.del_count > 30:
                self.del_count = 0
                self.card_queue.append(Card(self.ng_card.num, self.ng_card.color,self.nHaichi))
                random.shuffle(self.card_queue)
                self.allCard.remove(self.ng_card)
                del(self.ng_card)
                self.ng_card=None






    def draw(self):
        if not self.is_visible:
            return
        
        if self.grid:
            if self.cards[7][8]!=None:
                pyxel.text(130,1,f"{self.cards[7][8].num}", pyxel.COLOR_BLACK)

        for card in self.allCard:
            card.draw()


        self.drawCardBtn.draw()
        self.openBtn.draw()
        self.newBtn.draw()
        self.settingBtn.draw()


        self.count=self.count+1
        if self.count == 30:
            self.count=0
            if not self.miss:
                self.sec=self.sec+1


        if self.start:
            strSec=f"{self.sec}"
            secLen=len( strSec)*pyxel.FONT_WIDTH
            pyxel.text(110-secLen,1,strSec, pyxel.COLOR_BLACK)
            pyxel.text(110,1," sec", pyxel.COLOR_BLACK)
            pyxel.text(50, 1, f"zanki {self.zanki}", pyxel.COLOR_BLACK)

            if self.viewStart:
                # フレーム数に基づいて位置をランダムに変える
                x = 10 + random.randint(-1, 1)
                y = 2 + random.randint(-1, 1)

                #fade_color = 7 - (self.frame_count // 10)  # 色を徐々に薄くする
                #if fade_color < 0:
                #    fade_color = 0  # 色が範囲外にならないようにする

                pyxel.text(x, y, "start!!", pyxel.COLOR_BLACK)
                if self.sec > 2:
                    self.viewStart=False

                

        if self.miss:
            pyxel.text(100, 100, f"Game Over", pyxel.COLOR_BLACK)

        x_offset=50
        y_offset=235
        line_offset=10
        for num in range(12):
            l=len( f"{num}")
            if l==1:
                l=2
            else:
                l=0
            isExist=self.isCardOpen(num,pyxel.COLOR_BLACK)
            if not isExist:
                pyxel.rect(x_offset+num*9,y_offset, 8,8, pyxel.COLOR_BLACK)
                pyxel.text(x_offset+num*9+l,y_offset+1,f"{num}", pyxel.COLOR_WHITE)

            isExist=self.isCardOpen(num,pyxel.COLOR_WHITE)
            if not isExist:
                pyxel.rect(x_offset+num*9,y_offset + line_offset, 8,8, pyxel.COLOR_GRAY)
                pyxel.text(x_offset+num*9+l,y_offset+1+line_offset,f"{num}", pyxel.COLOR_BLACK)


        #text = f"{self.string}"
        #text_width = pyxel.FONT_WIDTH * len(text)
        #pyxel.text(self.x + (self.w/2 - text_width/2),self.y+self.h/2-3, self.string, self.string_color)






class Game:
    def __init__(self):

        pyxel.init(160, 256, title="algo Pyxel")
        pyxel.mouse(True) #
        self.viewNo=1
        self.algo=StateMain(8,3)
        self.algo.setisVisible(True)

        pyxel.run(self.update, self.draw)

    def update(self):

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.viewNo==1:
            self.algo.update()
            if not self.algo.isVisible():
                del(self.algo)
                #self.algo=StateMain()
                #self.algo.setisVisible(True)
                self.viewNo=2
        #elif self.viewNo==2:

    def draw(self):
        pyxel.cls(pyxel.COLOR_WHITE)
        if self.viewNo==1:
            self.algo.draw()
        elif self.viewNo==2:
            pyxel.text(80, 100, "Setting", pyxel.COLOR_BLACK)



Game()
