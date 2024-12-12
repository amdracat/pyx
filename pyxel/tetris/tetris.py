import pyxel
import numpy
import random
import copy
from collections import deque

from blockconst import BlockConst
from masu import Masu
from block import Block
from stage import Stage
from timer import Timer




class Game:
    X_OFFSET=10
    Y_OFFSET=10
    X_POS_INIT=5
    Y_POS_INIT=0

    def initialize(self,isFisrt):
        if isFisrt != True:
            del(self.stage)
            del(self.timer)
            self.block_queue.clear()

        self.stage =Stage()
        self.block_queue = deque()
        self.x=self.X_POS_INIT
        self.y=self.Y_POS_INIT
        self.count=0
        self.block_fall_speed=30
        self.isGameOver=False
        self.left_key_counter = 0
        self.right_key_counter = 0
        self.key_delay = 10  # 最初の遅延
        self.key_repeat = 3  # 連続入力の間隔
        self.score=0
        self.block_queue.append(Block())
        self.block_queue.append(Block())
        self.block_queue.append(Block())
        self.activeBlock = self.block_queue.popleft()
        self.holdBlock = None
        self.canHold=True
        self.timer=Timer(33)
        self.isTouchFloor=False

    def __init__(self):
        self.initialize(True)

        pyxel.init(220, 240, title="Hello Pyxel")
        pyxel.load("tetris_resource.pyxres")
        pyxel.run(self.update, self.draw)

    def score_countup(self,line):
        if line == 0:
            self.score = self.score
        elif line == 1:
            self.score = self.score+100
        elif line == 2:
            self.score = self.score+250
        elif line == 3:
            self.score = self.score+500
        elif line == 4:
            self.score = self.score+1000
        else:
            self.score = self.score+line*300

    def block_fall_speed_ctrl(self):
        if 5000 < self.score:
            self.block_fall_speed = 1
        elif 4000 < self.score:
            self.block_fall_speed = 2
        elif 3000 < self.score:
            self.block_fall_speed = 5
        elif 2000 < self.score:
            self.block_fall_speed = 10
        elif 1000 < self.score:
            self.block_fall_speed = 20
        else:
            self.block_fall_speed = 30

    def block_fall(self):
        isFall=False
        baseY = self.y
    
        if self.stage.can_plot_block(self.x,baseY +1,self.activeBlock.get_block()):
            #１マスは移動可能
            self.timer.cancel_timer()
            self.y = self.y + 1
            isFall=True
            self.isTouchFloor=False
            #y+1によって着地したか？(+2で判定)
            if self.stage.can_plot_block(self.x,baseY +2,self.activeBlock.get_block()) == False:
                self.isTouchFloor = True
                if not self.timer.isTimerRunning() and not self.timer.isTimerComplate() :
                    # 着地後、何等か操作があれば600msは操作可能
                    self.timer.restart(700)
                    
        else:
            self.isTouchFloor = True
        
        if isFall==False and not self.timer.isTimerRunning():
            self.y = self.y + 1



    #======================================
    # 30fpsでpyxelにコールされる状態更新処理
    #======================================
    def update(self):
        enableFall=True
        #----------------------
        # タイマー
        #----------------------
        self.timer.cyclic()

        #----------------------
        # key更新
        #----------------------
        #  *** 中断 ***
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        #  *** ホールド ***
        if pyxel.btnp(pyxel.KEY_E):
            if self.canHold:
                self.canHold=False
                if self.holdBlock is None:
                    self.holdBlock = copy.deepcopy(self.activeBlock)
                    del(self.activeBlock)
                    self.block_queue.append(Block())
                    self.activeBlock = self.block_queue.popleft()
                else:
                    #del(self.activeBlock)
                    temp = copy.deepcopy(self.activeBlock)
                    self.activeBlock=copy.deepcopy(self.holdBlock)
                    self.holdBlock= copy.deepcopy(temp)

        #  *** デバッグ ***
        if pyxel.btnp(pyxel.KEY_S):
            self.initialize(False)

        #  *** デバッグ ***
        if pyxel.btnp(pyxel.KEY_A):
            self.block_fall_speed =1

        #  *** 回転 ***
        if pyxel.btnp(pyxel.KEY_R):
            if self.isGameOver:
                self.initialize(False)
                return
            if self.stage.can_plot_block(self.x,self.y, self.activeBlock.get_rotate_block()):
                self.activeBlock.rotate()

        #  *** 左キー ***
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.left_key_counter += 1
            if self.left_key_counter == 1 or (self.left_key_counter > self.key_delay )and ((self.left_key_counter - self.key_delay) % self.key_repeat == 0):
                #if self.stage.can_plot_block(self.x,self.y,self.activeBlock.get_block()) == False:
                if self.stage.can_plot_block(self.x -1,self.y,self.activeBlock.get_block()):
                    self.x = self.x -1
        else:
            self.left_key_counter = 0  # キーが離されたらリセット

        #  *** 右キー ***
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.right_key_counter += 1
            if self.right_key_counter == 1 or self.right_key_counter > self.key_delay and (self.right_key_counter - self.key_delay) % self.key_repeat == 0:
                if self.stage.can_plot_block(self.x +1,self.y,self.activeBlock.get_block()):
                    self.x = self.x + 1
        else:
            self.right_key_counter = 0  # キーが離されたらリセット 
        
        #  *** 上キー ***
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            tempy = self.y
            while True:
                if self.stage.can_plot_block(self.x, tempy, self.activeBlock.get_block()):
                    tempy = tempy + 1
                else:
                    break
            if (tempy -1) != self.y:
                self.y=tempy-1
                enableFall=False

        #  *** 下キー ***
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            if self.stage.can_plot_block(self.x,self.y+1,self.activeBlock.get_block()):
                self.count = 0
                self.block_fall()
                enableFall=False

        #----------------------
        # GameOver スキップ
        #----------------------
        if self.isGameOver:
            return

        #----------------------
        # 自然落下
        #----------------------
        if enableFall:
            self.count=self.count+1
            if self.count >= self.block_fall_speed:
                self.count = 0
                self.block_fall()

        #----------------------
        # 設置判定
        #----------------------
        if self.stage.can_plot_block(self.x,self.y,self.activeBlock.get_block()):
            #落下位置表示
            tempy = self.y
            while True:
                if self.stage.can_plot_block(self.x, tempy, self.activeBlock.get_block()):
                    tempy = tempy + 1
                else:
                    break
            if (tempy -1) != self.y:
                self.stage.plot_fallblock(self.x,tempy -1,self.activeBlock.get_block())
            self.stage.clear_active_block()
            self.stage.plot_block(self.x,self.y,self.activeBlock.get_block())
        else:
            if self.timer.isTimerRunning()==True:
                return
            #配置が確定
            self.stage.fix_activeBlock()

            #行のクリア判定＆スコア更新
            line = self.stage.clear_full_lines()
            self.score_countup(line)
                
            #次のブロックを配置
            self.x=self.X_POS_INIT
            self.y=self.Y_POS_INIT
            self.canHold=True
            self.block_queue.append(Block())
            self.activeBlock = self.block_queue.popleft()

            #初期ブロックを置けなければゲームオーバー
            if self.stage.can_plot_block(self.x,self.y,self.activeBlock.get_block())==False:
                #print("GameOver")
                #self.activeBlock.print_state()
                #self.stage.print_grid()
                self.stage.gameover()
                self.isGameOver=True

    def show_debug_param(self):
        offset_y=160
        offset_val=10
        #pyxel.text(136, offset_y+offset_val*0, f"ti_key:{self.timerKey.isTimerRunning()}", 7)
        pyxel.text(136, offset_y+offset_val*1, f"timer:{self.timer.get_count()*33}", 7)
        pyxel.text(136, offset_y+offset_val*2, f"ti_ru:{self.timer.isTimerRunning()}", 7)
        pyxel.text(136, offset_y+offset_val*3, f"ti_co:{self.timer.isTimerComplate() }", 7)
        pyxel.text(136, offset_y+offset_val*4, f"key_L:{self.left_key_counter}", 7)
        pyxel.text(136, offset_y+offset_val*5, f"kye_R:{self.right_key_counter}", 7)
        pyxel.text(136, offset_y+offset_val*6, f"x:{self.x}", 7)
        pyxel.text(136, offset_y+offset_val*7, f"y:{self.y}", 7)


    def draw_block(self,block,i,j):
        type_val=block.get()
        if type_val == BlockConst.ACTICE:
            type_val = block.getKind()
        
        if type_val == BlockConst.WALL:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,0,10, 10,100)
        elif type_val == BlockConst.BLOCK7:
            if block.getSpecial()==1:
                pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,(block.getRole()//90)*20 + 100,10, 10,100)
            elif block.getSpecial()==2:
                pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,10,(block.getRole()//90)*20 + 100,10, 10,100)
            elif block.getSpecial()==3:
                pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,(block.getRole()//90)*20 + 110,10, 10,100)
            elif block.getSpecial()==4:
                pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,10,(block.getRole()//90)*20 + 110,10, 10,100)
        elif type_val == BlockConst.BLOCKEND:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,10,0,10, 10,100)
        elif type_val == BlockConst.FALLPOS:
            pyxel.rectb(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 10, 10,1)
        else:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,(block.getRole()//90)*10,(type_val-BlockConst.BLOCK1)*10+10,10, 10,100)


    def draw_score(self):
        x_offset = 162
        y_offset=135
        #pyxel.line(x_offset+20, y_offset, x_offset+20, y_offset+200, 10)
        #self.score=self.score+10
        pyxel.text(x_offset+3, y_offset, "SCORE", 7)
        score_text = f"{self.score}"
        text_width = pyxel.FONT_WIDTH * len(score_text)

        pyxel.text(x_offset - text_width+30, y_offset+20,score_text, pyxel.COLOR_WHITE)
    def draw_next_two_blocks(self):
        next_block1 = self.block_queue[0].get_block()  # キューの先頭要素

        x_offset = 162
        y_offset=20
        #pyxel.line(x_offset+20, y_offset, x_offset+20, y_offset+200, 10)

        pyxel.text(x_offset+3, y_offset-7, "NEXT", 7)
        pyxel.text(x_offset+3, y_offset-7+60, "HOLD", 7)
        # 1つ目の次のブロックを描画
        pyxel.rectb(x_offset-10, y_offset, 42, 42, 1)
        pyxel.rectb(x_offset-10, y_offset+60, 42, 42, 1)
        for i in range(4):
            for j in range(4):
                if next_block1[j][i].get() == 1:
                    pyxel.rect(i * 10 + x_offset - self.block_queue[0].get_center_x()+ 11, j * 10 + y_offset + 22 - self.block_queue[0].get_center_y(), 8, 8,1)


        # 2つ目の次のブロックを描画
        if self.holdBlock is not None:
            for i in range(4):
                for j in range(4):
                    if self.holdBlock.get_block()[j][i].get() == 1:
                        pyxel.rect(i * 10 + x_offset - self.holdBlock.get_center_x()+ 11, j * 10 + y_offset  + 22 - self.holdBlock.get_center_y()+60, 8, 8,1)


    def draw(self):
        pyxel.cls(0)

        for i in range(Stage.ROWS):
            for j in range(Stage.COLS):
                #Grid
                #pyxel.rectb(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 10, 10, 7)
                self.draw_block(self.stage.get_stage_block(i,j),i,j)

        if self.isGameOver:
            pyxel.text(55, 41, "Game Over!!", pyxel.frame_count % 16)
        
        if not self.isGameOver:
            self.draw_next_two_blocks()
        self.draw_score()
        self.show_debug_param()
Game()
