import pyxel
import random
import copy
from collections import deque

from blockconst import BlockConst
from masu import Masu
from block import Block
from stage import Stage
from timer import Timer
from particle import Particle
from musicMainGame import MusicMainGame
from keyRepeat import KeyRepeat
from ctrlParam import CtrlParam
import math
from score import Score
from crossKey import CrossKey

class StateMainGame:
    X_OFFSET=10
    Y_OFFSET=10
    X_POS_INIT=5
    Y_POS_INIT=0
    #======================================
    # 初期化
    #======================================
    def __init__(self):
        self.music =MusicMainGame()
        self.initialize_game(True)
        self.initialize_once()   
        self.param=CtrlParam()
        self.cross=CrossKey()

    def initialize_game(self,isFisrt):
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
        self.score=0
        self.block_queue.append(Block())
        self.block_queue.append(Block())
        self.block_queue.append(Block())
        self.activeBlock = self.block_queue.popleft()
        self.holdBlock = None
        self.canHold=True
        self.timer=Timer(33)
        self.enableFall=True
        self.waitUserInput=False
        self.selectContinue=True
        self.particles = []

    def initialize_once(self):
        self.visible=False
        self.score_manager = Score()
        self.leftKey=KeyRepeat(
            key1=pyxel.KEY_LEFT,
            key2=pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,
            firstDelay=10,
            repeat=3,
            ufunc=self.det_key_left
        )
        self.leftRight=KeyRepeat(
            key1=pyxel.KEY_RIGHT,
            key2=pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,
            firstDelay=10,
            repeat=3,
            ufunc=self.det_key_right
        )
    #======================================
    # ステージ選択
    #======================================
    def set_is_visible(self,visible):
        self.visible=visible
        if self.visible:
            self.initialize_game(False)
        else:
            self.initialize_game(False)
    def is_visible(self):
        return self.visible

    #======================================
    # 30fpsでpyxelにコールされる状態更新処理
    #======================================
    def update(self):
        if not self.visible:
            return
        #  *** 中断 ***
        if pyxel.btnp(pyxel.KEY_SPACE) or ( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.det_stop_tochu()):
            if not self.waitUserInput:
                self.waitUserInput=True
                self.music.music_stop()

        if pyxel.btnp(pyxel.KEY_RETURN) or ( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and  self.cross.mouseCenter()):
            if self.waitUserInput:
                if self.selectContinue:
                    self.waitUserInput=False
                    self.music.music_start()
                    if self.isGameOver:
                        self.initialize_game(False)
                else:
                    self.music.music_start()
                    self.set_is_visible(False)
            else:
                if ( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and  self.cross.mouseCenter()):
                    self.activeBlock.rotate()

        if  self.waitUserInput:
            if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or ( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and  self.cross.mouseRight()):
                self.selectContinue=False
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or ( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.cross.mouseLeft()):
                self.selectContinue=True       

        if not self.waitUserInput:
            self.cycle_start()
            self.update_key()
            self.action()
        




    #======================================
    # キー動作定義
    #======================================
    def det_key_left(self):
        if self.stage.can_plot_block(self.x -1,self.y,self.activeBlock.get_block()):
            self.x = self.x -1

    def det_key_right(self):
        if self.stage.can_plot_block(self.x +1,self.y,self.activeBlock.get_block()):
            self.x = self.x + 1

    def det_key_up(self):
        tempy = self.y
        while True:
            if self.stage.can_plot_block(self.x, tempy, self.activeBlock.get_block()):
                tempy = tempy + 1
            else:
                break
        if (tempy -1) != self.y:
            self.y=tempy-1
            self.enableFall=False

    def det_key_down(self):
        if self.stage.can_plot_block(self.x,self.y+1,self.activeBlock.get_block()):
            self.count = 0
            self.block_fall()
            self.enableFall=False

    def det_key_hold(self):
        if self.canHold:
            self.canHold=False
            if self.holdBlock is None:
                self.activeBlock.rotate_to_0()
                self.holdBlock = copy.deepcopy(self.activeBlock)
                del(self.activeBlock)
                self.block_queue.append(Block())
                self.activeBlock = self.block_queue.popleft()
                self.x=self.X_POS_INIT
                self.y=self.Y_POS_INIT
            else:
                #del(self.activeBlock)
                self.activeBlock.rotate_to_0()
                temp = copy.deepcopy(self.activeBlock)
                self.activeBlock=copy.deepcopy(self.holdBlock)
                self.holdBlock= copy.deepcopy(temp)
                self.x=self.X_POS_INIT
                self.y=self.Y_POS_INIT


    def det_key_rotate(self):
        if self.stage.can_plot_block(self.x,self.y, self.activeBlock.get_rotate_block()):
            self.activeBlock.rotate()

    #def det_key_debug(self):
    #    #self.music.music_stop()
    #    #self.music.sound_gameover()
    #    #self.music.sound_effect(2)
    #    #self.initialize_game(False)
    #    self.score = self.score + 1000

    def update_key(self):
        if pyxel.btnp(pyxel.KEY_E):
            self.det_key_hold()

        #if pyxel.btnp(pyxel.KEY_S):
        #    self.det_key_debug()

        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.isGameOver:
                self.music.music_start()
                self.initialize_game(False)

        if pyxel.btnp(pyxel.KEY_R):
            self.det_key_rotate()

        self.leftKey.update()
        self.leftRight.update()
        
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.det_key_up()

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.det_key_down()


        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.cross.mouseLeft():
                    self.det_key_left()
            elif self.cross.mouseRight():
                    self.det_key_right()
            elif self.cross.mouseUp():
                    self.det_key_up()
            elif self.cross.mouseDown():
                    self.det_key_down()
            elif self.det_hold_tochu():
                    self.det_key_hold()
            #elif 155 < pyxel.mouse_x < 185 and  175 < pyxel.mouse_y < 205:
            #        print("rotate")
            #        #self.det_key_rotate()
            elif self.det_stop_tochu():
                    if not self.waitUserInput:
                        self.waitUserInput=True
                        self.music.music_stop()


    def det_hold_tochu(self):
        return (152 < pyxel.mouse_x < 194 and  80 < pyxel.mouse_y < 122)
    def det_stop_tochu(self):
        return (10 < pyxel.mouse_x < 130 and  10 < pyxel.mouse_y < 230)
    #======================================
    # 更新前準備
    #======================================
    def cycle_start(self):
        self.enableFall=True
        self.timer.cyclic()
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)

    #======================================
    # 更新処理
    #======================================
    def action(self):
        # GameOver スキップ
        if self.isGameOver:
            return

        # 自然落下
        if self.enableFall:
            self.count=self.count+1
            if self.count >= self.block_fall_speed:
                self.count = 0
                self.block_fall()

        # 設置判定
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
            if line != 0:
                
                if line == 4:
                    self.create_explosion(130, self.y*10)
                    self.music.sound_effect(1)
                else:
                    self.music.sound_effect(0)
            else:
                self.music.sound_effect(2)
            
            self.score = self.param.score_countup(line,self.score)
            self.block_fall_speed = self.param.block_fall_speed_ctrl(self.score)

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
                self.score_manager.set_score(self.score)
                self.music.music_stop()
                self.music.sound_gameover()
                self.stage.gameover()
                self.isGameOver=True

    #---------------------
    # 落下処理
    #---------------------
    def block_fall(self):
        isFall=False
        baseY = self.y
    
        if self.stage.can_plot_block(self.x,baseY +1,self.activeBlock.get_block()):
            #１マスは移動可能
            self.timer.cancel_timer()
            self.y = self.y + 1
            isFall=True
            #y+1によって着地したか？(+2で判定)
            if self.stage.can_plot_block(self.x,baseY +2,self.activeBlock.get_block()) == False:
                if not self.timer.isTimerRunning() and not self.timer.isTimerComplate() :
                    # 着地後、何等か操作があれば600msは操作可能
                    self.timer.restart(700)  
        
        if isFall==False and not self.timer.isTimerRunning():
            self.y = self.y + 1


    #======================================
    # 描画処理 Pyxelにコールされる
    #======================================
    def draw(self):
        if not self.visible:
            return
        self.draw_main_game()
        if self.waitUserInput:
            if self.isGameOver:
                pyxel.text(55, 41, "Continue?", 7)
            else:
                pyxel.text(55, 41, "Continue?", pyxel.frame_count % 16)
            if self.selectContinue:
                #pyxel.rectb(52, 49, 20, 10, 1)
                yesCol=7
                noCol=1
            else:
                #pyxel.rectb(77, 49,  20, 10, 1)
                yesCol=1
                noCol=7
            pyxel.text(55,51, "YES!", yesCol)
            pyxel.text(80,51, "NO..", noCol)
        #pyxel.rectb(150, 200, 30, 30, 1)
        #pyxel.rectb(155, 145, 30, 90, 1)
        #pyxel.rectb(125, 175, 90, 30, 1)

        #回転
        #pyxel.rectb(160, 180, 30, 30, 1)
        #右キー
        #pyxel.rectb(190, 180, 30, 30, 1)
        #左キー
        #pyxel.rectb(130, 180, 30, 30, 1)
        #上キー
        #pyxel.rectb(160, 150, 30, 30, 1)
        #下キー
        #pyxel.rectb(160, 210, 30, 30, 1)
        
        self.cross.draw()

    #---------------------
    # ステージ描画
    #---------------------
    def draw_main_game(self):
        for i in range(Stage.ROWS):
            for j in range(Stage.COLS):
                #Grid
                #pyxel.rectb(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 10, 10, 7)
                self.draw_block(self.stage.get_stage_block(i,j),i,j)

        if self.isGameOver:
            pyxel.text(55, 100, "Game Over!!", pyxel.frame_count % 16)
        
        if not self.isGameOver:
            self.draw_next_two_blocks()
        self.draw_score()
        #self.show_debug_param()
        for particle in self.particles:
            pyxel.pset(particle.x, particle.y, 8 + particle.life % 8)

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

    #---------------------
    # NextとHoldの描画
    #---------------------
    def draw_next_two_blocks(self):
        next_block1 = self.block_queue[0].get_block()  # キューの先頭要素

        x_offset = 162
        y_offset=20
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

    #---------------------
    # スコア描画
    #---------------------
    def draw_score(self):
        x_offset = 162
        y_offset=128
        pyxel.text(x_offset+3, y_offset, "SCORE", 7)
        score_text = f"{self.score}"
        text_width = pyxel.FONT_WIDTH * len(score_text)

        pyxel.text(x_offset - text_width+30, y_offset+10,score_text, pyxel.COLOR_WHITE)

    #---------------------
    # パーティクル１
    #---------------------
    def create_explosion(self,x, y):
        for _ in range(50):
            self.particles.append(Particle(x, y))

    #---------------------
    # デバッグ
    #---------------------
    def show_debug_param(self):
        offset_y=200
        offset_val=10
        pyxel.text(136, offset_y+offset_val*0, f"speed:{self.block_fall_speed}", 7)
        pyxel.text(136, offset_y+offset_val*1, f"timer:{self.timer.get_count()*33}", 7)
        pyxel.text(136, offset_y+offset_val*2, f"x:{self.x}", 7)
        pyxel.text(136, offset_y+offset_val*3, f"y:{self.y}", 7)


