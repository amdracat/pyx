import pyxel
import copy
import random
from collections import deque
import math
class ButtonTri:
    def __init__(self,x,y,size,color,direction):
        self.color=color
        self.isOn=False
        self.vertex1, self.vertex2, self.vertex3 = self.calculate_vertices(x, y, size, direction)
        self.in_vertex1, self.in_vertex2, self.in_vertex3 = self.calculate_vertices(x, y, size-5, direction)


    def calculate_vertices(self,x, y, size, direction):
        if direction == "right":
            angle_offset = 0
        elif direction == "left":
            angle_offset = math.pi
        elif direction == "up":
            angle_offset = -math.pi / 2
        elif direction == "down":
            angle_offset = math.pi / 2
        
        vertex1 = (x + size * math.cos(angle_offset), y + size * math.sin(angle_offset))
        vertex2 = (x + size * math.cos(angle_offset + 2 * math.pi / 3), y + size * math.sin(angle_offset + 2 * math.pi / 3))
        vertex3 = (x + size * math.cos(angle_offset + 4 * math.pi / 3), y + size * math.sin(angle_offset + 4 * math.pi / 3))
        
        return vertex1, vertex2, vertex3

    def point_in_triangle(self,px, py, v1, v2, v3):
        # ベクトルの外積を使って点が三角形の内側にあるかを判定
        d1 = (px - v2[0]) * (v1[1] - v2[1]) - (py - v2[1]) * (v1[0] - v2[0])
        d2 = (px - v3[0]) * (v2[1] - v3[1]) - (py - v3[1]) * (v2[0] - v3[0])
        d3 = (px - v1[0]) * (v3[1] - v1[1]) - (py - v1[1]) * (v3[0] - v1[0])
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)

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
        if self.isOn:
            pyxel.tri(self.in_vertex1[0], self.in_vertex1[1], self.in_vertex2[0], self.in_vertex2[1], self.in_vertex3[0], self.in_vertex3[1], self.color)
        
        pyxel.line(self.vertex1[0],self.vertex1[1], self.vertex2[0], self.vertex2[1], self.color)  # 点Aから点Bへの線
        pyxel.line(self.vertex2[0],self.vertex2[1], self.vertex3[0], self.vertex3[1], self.color)  # 点Aから点Bへの線
        pyxel.line(self.vertex3[0],self.vertex3[1], self.vertex1[0], self.vertex1[1], self.color)  # 点Aから点Bへの線

    def isTouch(self):
        return self.point_in_triangle(pyxel.mouse_x, pyxel.mouse_y, self.vertex1, self.vertex2, self.vertex3)



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
        self.isFirst=True
        self.isFirsttouch=False
    
    def update(self):
        if self.isFirst and self.isTouch():
            self.isOn=True
            self.isFirsttouch=True
        self.isFirst =False
        if self.isOn:
            now=True
        else:
            now=False
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            if self.isTouch():
                self.isOn=True
            else:
                self.isOn=False
                self.isFirsttouch=False
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

        if self.isOn and not self.isFirsttouch:
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
    def isTouch(self):
        ret= ( self.vertices[0].x < pyxel.mouse_x < self.vertices[1].x and  self.vertices[0].y < pyxel.mouse_y < self.vertices[2].y)
        #print(f" {ret} {pyxel.mouse_x } {pyxel.mouse_y} { self.vertices[0].x  }  { self.vertices[1].x  }  { self.vertices[0].y  }  { self.vertices[2].y }")
        return ret

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
    


class StateMain:
    def __init__(self,tateNum,zanki,hint):
        self.nHaichi=tateNum
        self.count=0
        self.sec=0
        self.start=False
        self.viewStart=False
        self.allCard = []
        self.cards = [[None for _ in range(10)] for _ in range(9)]  # 9列10行の2次元配列を作成
        self.card_queue = deque()
        self.create_cards()
        self.grid=False
        self.done=False
        self.miss=False
        self.missCount=0
        self.zanki=zanki
        self.isHint = hint
        self.waitFirstOpen=True
        #self.drawCardBtn=Button(5,205,40,15,pyxel.COLOR_BLACK,"DARW",pyxel.COLOR_WHITE)
        self.openBtn=Button(5,205,40,20,pyxel.COLOR_BLACK,"OPEN",pyxel.COLOR_WHITE)
        self.newBtn=Button(5,205+20,40,15,pyxel.COLOR_GRAY,"NEW GAME",pyxel.COLOR_BLACK)
        self.settingBtn=Button(5,205+20+15,40,15,pyxel.COLOR_GRAY,"SETTING",pyxel.COLOR_BLACK)


        self.newGameDialog=Dialog("Go Next Game?",self.dialog_newgame_yes,self.dialog_newgame_no)
        self.settingDialog=Dialog("Go Setting?",self.dialog_newgame_yes,self.dialog_newgame_no)
        self.draw_init_cards(self.nHaichi)
        self.is_visible=False
        self.ng_card=None
        self.del_count=0
        self.isClear=False
        self.next_setting=False
        self.next_newgame=False
        self.score_manager = Score()

    def isVisible(self):
        return self.is_visible

    def setisVisible(self,isVisible):
        self.is_visible=isVisible
    def get_next_isSetting(self):
        return self.next_setting
    def get_next_isNewGame(self):
        return self.next_newgame

    def dialog_newgame_yes(self):
        self.is_visible=False
    def dialog_newgame_no(self):
        self.next_setting=False
        self.next_newgame=False


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
        #for num in range(7):
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

    def isNotOpenCardExist(self):
        for card in self.allCard:
            if not card.isOpend():
                return True
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

    def openCard(self):
        retCard=None
        for card in self.allCard:
            if self.cards[7][8]==None:
                if not self.start:
                    self.game_start()
                for x in range(9):
                    for y in range(10):
                        if self.cards[x][y] is not None:
                            card = self.cards[x][y]
                            #num, color = card.getCardInfo()
                            # ここでカードをオープンする条件をチェック
                            if not card.isOpend():
                                if self.can_open_card(x, y):
                                    card.setisOpen(True)
                                    retCard=card
                                else:
                                    card.setisCantOpen()
                                    return None
        return retCard

    def game_start(self):
        self.start=True
        self.count=0
        self.sec=0
        self.viewStart=True

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
    
    def drawCard(self):
        if  not self.miss:
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



    #def update_drawBtn(self):
    #    if self.drawCardBtn.update():
    #        if self.drawCardBtn.isOn and not self.miss:
    #            self.drawCard()

    def update_openBtn(self):
        if self.openBtn.update():
            if self.openBtn.isOn and not self.miss:
                self.waitFirstOpen=False
                opencard = self.openCard()
                if opencard != None:
                    ret = self.checkGame()
                    leng = len(self.card_queue)
                    #print(f"check {ret}  {leng}")
                    if ret == False:
                        self.zanki= self.zanki-1
                        self.missCount +=1
                        if self.zanki == 0:
                            self.miss=True
                        else:
                            self.ng_card=opencard
                            self.del_count=0
                            opencard.setisCantOpen()
                    else:  
                        if leng == 0:
                            self.isClear=True
                            score = (10 - self.nHaichi) * 1000 - self.sec -self.missCount*100
                            if score < 10:
                                score = 10
                            self.score_manager.set_score(score,self.nHaichi,self.sec,self.missCount)
                        else:
                            self.drawCard()

    def update_newBtn(self):
        if self.newBtn.update():
            if self.newBtn.isOn:
                if not self.isClear and not self.miss:
                    self.newGameDialog.setisEnableDialog(True)
                else:
                    self.dialog_newgame_yes()
                self.next_newgame=True

    def update_settingBtn(self):
        if self.settingBtn.update():
            if self.settingBtn.isOn:
                self.settingDialog.setisEnableDialog(True)
                self.next_setting=True

    def delete_card(self):
        if self.ng_card != None:
            self.del_count=self.del_count+1
            if self.del_count > 30:
                self.del_count = 0
                self.card_queue.append(Card(self.ng_card.num, self.ng_card.color,self.nHaichi))
                random.shuffle(self.card_queue)
                self.allCard.remove(self.ng_card)
                del(self.ng_card)
                self.ng_card=None
                self.drawCard()

    def update(self):
        if not self.is_visible:
            return

        self.newGameDialog.update()
        if self.newGameDialog.isEnableDialog():
            return
        self.settingDialog.update()
        if self.settingDialog.isEnableDialog():
            return

        self.cards = [[None for _ in range(10)] for _ in range(9)] 


        self.count=self.count+1
        if self.count == 30:
            self.count=0
            if not self.miss and not self.isClear:
                self.sec=self.sec+1

        #デバッグイベント
        
        if pyxel.btnp(pyxel.KEY_S):
            self.grid = not self.grid
        if pyxel.btnp(pyxel.KEY_A):
            score = (10 - self.nHaichi) * 1000 - self.sec - self.missCount*100
            if score < 10:
                score = 10
            print(f"score {score} {self.nHaichi} {self.sec}")
            self.score_manager.set_score(score,self.nHaichi,self.sec,self.missCount)
        if pyxel.btnp(pyxel.KEY_W):
            self.miss=True
        if pyxel.btnp(pyxel.KEY_E):
            self.isClear=True
        


        #配列
        for card in self.allCard:
            card.update(self.allCard)
            x,y=card.getPosition()
            self.cards[x][y]=card

        #self.update_drawBtn()
        self.update_openBtn()
        self.update_newBtn()
        self.update_settingBtn()



        self.delete_card()




    def draw_hint(self,x,y):
        x_offset=x
        y_offset=y
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

    def draw_time(self,x,y,sec):
        strSec=f"{sec}"
        secLen=len( strSec)*pyxel.FONT_WIDTH
        pyxel.text(x-secLen,y,strSec, pyxel.COLOR_BLACK)
        pyxel.text(x,y," sec", pyxel.COLOR_BLACK)

    def draw_start(self,x,y):
        # フレーム数に基づいて位置をランダムに変える
        x_tmp = x + random.randint(-1, 1)
        y_tmp = y + random.randint(-1, 1)

        pyxel.text(x_tmp, y_tmp, "start!!", pyxel.COLOR_BLACK)

    def draw_zanki(self,x,y):
        #pyxel.text(x, y, f"LIFE {self.zanki}", pyxel.COLOR_BLACK)
        pyxel.text(x, y, f"LIFE", pyxel.COLOR_BLACK)
        for i in range(self.zanki):
            self.draw_filled_heart(x+4*pyxel.FONT_WIDTH+3 + i*6, y+2, 5, pyxel.COLOR_RED)

    def draw_gameover(self,x,y):
        strClear = Str("Game Over", pyxel.COLOR_WHITE)
        pyxel.rect(x-40, y, 80, 20, pyxel.COLOR_NAVY)
        strClear.draw(x, y+7)

    def draw_gameclear(self,x,y):
        strClear = Str("Game Clear!!", pyxel.COLOR_BLACK)
        pyxel.rect(x-40, y, 80, 20, pyxel.COLOR_LIGHT_BLUE)
        strClear.draw(x, y+7)
        #pyxel.text(x, y, f"Game Clear!!", pyxel.COLOR_BLACK)


    def draw_filled_heart(self,x, y, size, color):
        # ハートの上部を描く（2つの円）
        pyxel.circ(x - size//4, y - size//4, size//4, color)
        pyxel.circ(x + size//4, y - size//4, size//4, color)
        
        # ハートの下部を描く（四角形と三角形）
        pyxel.tri(x - size//2, y - size//8, x + size//2, y - size//8, x, y + size//2, color)
        pyxel.rect(x - size//2, y - size//4, size, size//4, color)


    def draw(self):
        
        if not self.is_visible:
            return
    
        if self.grid:
            if self.cards[7][8]!=None:
                pyxel.text(130,10,f"{self.cards[7][8].num}", pyxel.COLOR_BLACK)



        for card in self.allCard:
            card.draw()

        #self.drawCardBtn.draw()
        self.openBtn.draw()
        self.newBtn.draw()
        self.settingBtn.draw()
        

        if self.start:
            self.draw_time(140,1,self.sec)
            self.draw_zanki(5,1)

            if self.viewStart and not self.newGameDialog.isEnableDialog() and not self.settingDialog.isEnableDialog():
                self.draw_start(10,20)
                if self.sec > 2:
                    self.viewStart=False

        if self.miss:
            self.draw_gameover(80,100)
        if self.isClear:
            self.draw_gameclear(80,100)

        if self.isHint :
            self.draw_hint(50,235)

        self.newGameDialog.draw()
        self.settingDialog.draw()
        if self.waitFirstOpen:
            pyxel.rectb(5,205,40,20, pyxel.frame_count % 16)

class Dialog:
    HEIGHT=100
    def __init__(self,inputStr,yesCbr,noCbr):
        self.s=inputStr
        self.yC=yesCbr
        self.nC=noCbr
        self.isVisble=False
        self.yesBtn=Button(60,self.HEIGHT+20,17,12,pyxel.COLOR_WHITE,"Yes",pyxel.COLOR_BLACK)
        self.noBtn=Button(80,self.HEIGHT+20,17,12,pyxel.COLOR_WHITE,"No",pyxel.COLOR_BLACK)


    def setisEnableDialog(self,val):
        self.isVisble=val
    def isEnableDialog(self):
        return self.isVisble

    def update(self):
        if not self.isVisble:
            return

        if self.isVisble:
            if self.yesBtn.update():
                if self.yesBtn.isOn:
                    self.yC()
                    self.isVisble=False
            if self.noBtn.update():
                if self.noBtn.isOn:
                    self.nC()
                    self.isVisble=False



    def draw(self):
        if not self.isVisble:
            return
        strStr=self.s
        length=len(strStr)
        #pyxel.rect(30, 200, 80, 52,pyxel.COLOR_RED)
        pyxel.rect(40, self.HEIGHT, 80, 42,pyxel.COLOR_RED)
        pyxel.text(80-pyxel.FONT_WIDTH * length//2, self.HEIGHT+10, strStr, pyxel.COLOR_BLACK)
        self.yesBtn.draw()
        self.noBtn.draw()

class Str:
    def __init__(self,inputStr,color):
        self.s=inputStr
        self.c=color
        self.lengthOffset =pyxel.FONT_WIDTH * len(inputStr)//2
    def draw(self,x,y):
        pyxel.text(x-self.lengthOffset, y, self.s, self.c)


class Score:
    def __init__(self):
        self.scores = {'score': 0, 'nLine': 0, 'time': 0, 'miss': 0}
        self.highscores = self.load_highscores()
        
    def load_highscores(self):
        try:
            with open("highscores.bin", "rb") as file:
                return [{'score': int.from_bytes(file.read(4), 'big'), 
                         'nLine': int.from_bytes(file.read(4), 'big'), 
                         'time': int.from_bytes(file.read(4), 'big'),
                         'miss': int.from_bytes(file.read(4), 'big')} for _ in range(10)]
        except FileNotFoundError:
            return [{'score': 0, 'nLine': 0, 'time': 0, 'miss': 0} for _ in range(10)]

    def save_highscores(self):
        with open("highscores.bin", "wb") as file:
            for hs in self.highscores:
                file.write(hs['score'].to_bytes(4, 'big'))
                file.write(hs['nLine'].to_bytes(4, 'big'))
                file.write(hs['time'].to_bytes(4, 'big'))
                file.write(hs['miss'].to_bytes(4, 'big'))

    def set_score(self, new_score, new_nLine, new_time, new_miss):
        new_entry = {'score': new_score, 'nLine': new_nLine, 'time': new_time, 'miss': new_miss}
        if new_entry['score'] > min(self.highscores, key=lambda x: x['score'])['score']:
            self.highscores.append(new_entry)
            self.highscores = sorted(self.highscores, key=lambda x: x['score'], reverse=True)[:10]
            self.save_highscores()

    def clear_highscores(self):
        self.highscores = [{'score': 0, 'nLine': 0, 'time': 0, 'miss': 0} for _ in range(10)]
        self.save_highscores()
    
    def display_highscores(self):
        header = f"{'Rank':<5}{'Score':<10}{'Lines':<10}{'Time':<10}{'Miss':<10}"
        print(header)
        print("-" * len(header))
        for i, hs in enumerate(self.highscores):
            print(f"{i + 1:<5}{hs['score']:<10}{hs['nLine']:<10}{hs['time']:<10}{hs['miss']:<10}")


class Game:
    def __init__(self):

        pyxel.init(160, 256, title="algo Pyxel")
        pyxel.mouse(True) #
        self.viewNo=1
        self.nLine=8
        self.zanki=3
        self.isHint=True
        self.isMouse=True
        self.algo=StateMain(self.nLine,self.zanki,self.isHint)
        self.algo.setisVisible(True)
        self.tri1r = ButtonTri(130,24+17*0+4,8,pyxel.COLOR_BLACK,"right")
        self.tri1l = ButtonTri(100,24+17*0+4,8,pyxel.COLOR_BLACK,"left")

        self.tri2r = ButtonTri(130,24+17*1+4,8,pyxel.COLOR_BLACK,"right")
        self.tri2l = ButtonTri(100,24+17*1+4,8,pyxel.COLOR_BLACK,"left")

        self.tri3r = ButtonTri(130,24+17*2+4,8,pyxel.COLOR_BLACK,"right")
        self.tri3l = ButtonTri(100,24+17*2+4,8,pyxel.COLOR_BLACK,"left")

        self.tri4r = ButtonTri(130,24+17*3+4,8,pyxel.COLOR_BLACK,"right")
        self.tri4l = ButtonTri(100,24+17*3+4,8,pyxel.COLOR_BLACK,"left")

        self.title=Str("Setting", pyxel.COLOR_BLACK)
        self.score=Str("Highscores", pyxel.COLOR_BLACK)
        self.setting1=Str("Initial Card Count", pyxel.COLOR_BLACK)
        self.setting2=Str("Life", pyxel.COLOR_BLACK)
        self.setting3=Str("Hint", pyxel.COLOR_BLACK)
        self.setting4=Str("Mouse", pyxel.COLOR_BLACK)

        self.newBtn=Button(60,90,40,20,pyxel.COLOR_BLACK,"NEW GAME",pyxel.COLOR_WHITE)
        self.deleteBtn=Button(60,230,40,20,pyxel.COLOR_BLACK,"DELETE",pyxel.COLOR_WHITE)
        self.scoreDialog=Dialog("Detete?",self.dialog_newgame_yes,self.dialog_newgame_no)
        self.score_manager=None
        pyxel.run(self.update, self.draw)
        
    def dialog_newgame_yes(self):
        self.score_manager.clear_highscores()
    def dialog_newgame_no(self):
        pass
    def update(self):

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.viewNo==1:
            self.algo.update()
            if not self.algo.isVisible():
                if self.algo.get_next_isNewGame():
                    del(self.algo)
                    if self.score_manager != None:
                        del(self.score_manager)
                        self.score_manager=None
                    self.algo=StateMain(self.nLine,self.zanki,self.isHint)
                    self.algo.setisVisible(True)

                elif self.algo.get_next_isSetting(): 
                    del(self.algo)
                    self.viewNo=2
                    self.score_manager = Score()
        elif self.viewNo==2:
            self.scoreDialog.update()
            #if self.scoreDialog.isEnableDialog():
            #    return
            if self.newBtn.update():
                if self.newBtn.isOn:
                    self.viewNo=1
                    if self.score_manager != None:
                        del(self.score_manager)
                        self.score_manager=None
                    self.algo=StateMain(self.nLine,self.zanki,self.isHint)
                    self.algo.setisVisible(True)
            if self.deleteBtn.update():
                if self.deleteBtn.isOn:
                    self.scoreDialog.setisEnableDialog(True)
            if self.tri1r.update():
                if self.tri1r.isOn:
                    if self.nLine < 8:
                        self.nLine += 1
            if self.tri1l.update():
                 if self.tri1l.isOn:
                    if self.nLine >3:
                        self.nLine -= 1
            if self.tri2r.update():
                if self.tri2r.isOn:
                    if self.zanki < 9:
                        self.zanki += 1
            if self.tri2l.update():
                 if self.tri2l.isOn:
                    if self.zanki >1:
                        self.zanki -= 1
            if self.tri3r.update():
                if self.tri3r.isOn:
                    self.isHint = True
            if self.tri3l.update():
                 if self.tri3l.isOn:
                    self.isHint = False
            if self.tri4r.update():
                if self.tri4r.isOn:
                    self.isMouse = True
                    pyxel.mouse(self.isMouse )
            if self.tri4l.update():
                 if self.tri4l.isOn:
                    self.isMouse = False
                    pyxel.mouse(self.isMouse )


    def draw(self):
        pyxel.cls(pyxel.COLOR_WHITE)
        if self.viewNo==1:
            self.algo.draw()
        elif self.viewNo==2:
            self.title.draw(80,7)
            self.setting1.draw(40,24)
            self.setting2.draw(40,24+17)
            self.setting3.draw(40,24+17*2)
            self.setting4.draw(40,24+17*3)
            self.tri1r.draw()
            self.tri1l.draw()
            self.tri2r.draw()
            self.tri2l.draw()
            self.tri3r.draw()
            self.tri3l.draw()
            self.tri4r.draw()
            self.tri4l.draw()
            self.deleteBtn.draw()
            pyxel.text(115-1, 24+2, f"{self.nLine}", pyxel.COLOR_BLACK)
            pyxel.text(115-1, 24+17+2, f"{self.zanki}", pyxel.COLOR_BLACK)
            if self.isHint:
                pyxel.text(115-1*pyxel.FONT_WIDTH, 24+17*2+2, f"Yes", pyxel.COLOR_BLACK)
            else:
                pyxel.text(115-1*pyxel.FONT_WIDTH, 24+17*2+2, f"No", pyxel.COLOR_BLACK)

            if self.isMouse:
                pyxel.text(115-1*pyxel.FONT_WIDTH, 24+17*3+2, f"Yes", pyxel.COLOR_BLACK)
            else:
                pyxel.text(115-1*pyxel.FONT_WIDTH, 24+17*3+2, f"No", pyxel.COLOR_BLACK)

            self.newBtn.draw()

            self.score.draw(80,117)
            for i, hs in enumerate(self.score_manager.highscores):
                pyxel.text(10, 130 + i * 10, f"{i + 1:>3}: {hs['score']:>5}pt {hs['nLine']:>1}cnt {hs['time']:>7}sec {hs['miss']:>1}miss",pyxel.COLOR_BLACK)
            self.scoreDialog.draw()



Game()
