import pyxel
import numpy
import random
from collections import deque

class Masu:
    BLANK= 0 
    def __init__(self, val):
        self.val = val  # マスの種類
        self.role=0
        self.kind=0
        self.special=0
    def set(self,val):
        self.val = val  # マスの種類
    def get(self):
        return self.val
    def setRole(self,val):
        self.role = (self.role + val)%360
    def getRole(self):
        return self.role
    def setObj(self, obj):
        self.val = obj.get()
        self.role = obj.getRole()
        self.kind = obj.getKind()
        self.special = obj.getSpecial()
    def setKind(self,val):
        self.kind = val  # マスの種類
    def getKind(self):
        return self.kind
    def setSpecial(self,val):
        self.special = val  # マスの種類
    def getSpecial(self):
        return self.special




class Block:
    CENTER_CENTER=0
    CENTER_ZURE=1
    def __init__(self):
        
        self.sharp=random_number = random.randint(0, 6)
        #self.sharp=0
        self.block  = [[Masu(Stage.BLANK) for _ in range(4)] for _ in range(4)]
        self.center=self.CENTER_CENTER
        self.kind=0
        if self.sharp == 0:
            # I
            self.block[0][1].set(1) 
            self.block[1][1].set(1) 
            self.block[2][1].set(1) 
            self.block[3][1].set(1) 
            self.center=self.CENTER_CENTER
            self.kind=Stage.BLOCK1
        elif  self.sharp == 1:
            # Z
            self.block[2][0].set(1) 
            self.block[2][1].set(1) 
            self.block[3][1].set(1) 
            self.block[3][2].set(1)
            self.center=self.CENTER_ZURE
            self.kind=Stage.BLOCK2
        elif  self.sharp == 2:
            #S
            self.block[3][0].set(1) 
            self.block[3][1].set(1) 
            self.block[2][1].set(1) 
            self.block[2][2].set(1)
            self.center=self.CENTER_ZURE
            self.kind=Stage.BLOCK3
        elif  self.sharp == 3:
            #」
            self.block[1][1].set(1) 
            self.block[2][1].set(1) 
            self.block[3][1].set(1) 
            self.block[3][0].set(1)
            self.center=self.CENTER_ZURE
            self.kind=Stage.BLOCK4
        elif  self.sharp == 4:
            #L
            self.block[1][1].set(1) 
            self.block[2][1].set(1) 
            self.block[3][1].set(1) 
            self.block[3][2].set(1)
            self.center=self.CENTER_ZURE
            self.kind=Stage.BLOCK5
        elif  self.sharp == 5:
            # 山
            self.block[2][0].set(1) 
            self.block[2][1].set(1) 
            self.block[2][2].set(1) 
            self.block[1][1].set(1)
            self.center=self.CENTER_ZURE
            self.kind=Stage.BLOCK6
        elif  self.sharp == 6:
            #□
            self.block[1][1].set(1)
            self.block[1][2].set(1)
            self.block[2][1].set(1)
            self.block[2][2].set(1)

            self.block[1][1].setSpecial(1)
            self.block[1][2].setSpecial(2)
            self.block[2][1].setSpecial(3)
            self.block[2][2].setSpecial(4)
            self.center=self.CENTER_CENTER
            self.kind=Stage.BLOCK7
        size = len(self.block)
        for i in range(size):
            for j in range(size):
                if self.block[i][j].get()==1:
                    self.block[i][j].setKind(self.kind)
        print(f"make block self.sharp :{self.sharp}")

    def get_block(self):
        return self.block

    # ブロックを90度回転させる関数4×4中心
    def rotate_90_degrees(self,matrix):
        size = len(matrix)
        new_matrix = [[Masu(Masu.BLANK) for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                new_matrix[j][size - 1 - i].setObj(matrix[i][j])
        return new_matrix

    # ブロックを90度回転させる関数3×3中心
    def rotate_90_degrees2(self,matrix):
        size = len(matrix)
        new_matrix = [[Masu(Masu.BLANK) for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                new_matrix[i][j].setObj(matrix[i][j])
        # 3x3の部分を抽出
        sub_matrix = [
            [matrix[i][j] for j in range(3)]
            for i in range(1, 4)
        ]
        # 3x3の部分を回転
        rotated_sub_matrix = self.rotate_90_degrees(sub_matrix)
        # 回転した部分を元の位置に戻す
        for i in range(3):
            for j in range(3):
                new_matrix[i + 1][j].setObj( rotated_sub_matrix[i][j] )
        return new_matrix


    def get_rotate_block(self):
        #self.block = numpy.rot90(self.block, -1)
        if self.center==self.CENTER_CENTER:        
            new_block=self.rotate_90_degrees(self.block)
        else:
            new_block=self.rotate_90_degrees2(self.block)
        return new_block

    def rotate(self):
        if self.kind!=Stage.BLOCK7:
            self.block=self.get_rotate_block()
        size = len(self.block)
        for i in range(size):
            for j in range(size):
                self.block[i][j].setRole(90)

    
class Stage:
    # クラス属性として定数を定義
    ROWS = 22
    COLS = 12
    WALL = -1
    BLANK= 0
    ACTICE = 1
    BLOCK1 = 2
    BLOCK2 = 3
    BLOCK3 = 4
    BLOCK4 = 5
    BLOCK5 = 6
    BLOCK6 = 7
    BLOCK7 = 8   
    BLOCKEND = 9  

    def __init__(self):
        # 配列を定義し、ステージの端を-1、それ以外の領域を0で初期化
        self.grid = [[Masu(self.BLANK) for _ in range(self.COLS)] for _ in range(self.ROWS)]
        
        # ステージの端を-1で初期化
        for i in range(self.ROWS):
            self.grid[i][0].set(self.WALL)         # 左端
            self.grid[i][self.COLS-1].set(self.WALL)  # 右端
        for j in range(self.COLS):
            #self.grid[0][j] = self.WALL         # 上端
            self.grid[self.ROWS-1][j].set(self.WALL)  # 下端
            
    
    def get_stage_block(self,row,col):
        return self.grid[row][col]
    def plot_block(self, x, y, block):
        for i in range(4):
            for j in range(4):
                if (0 <= (y - j) < self.ROWS and 0 <=(x + i) < self.COLS):
                    if block[3 - j][i].get() == 1:
                        self.grid[y - j][x + i].setObj( block[3 - j][i])
                        

    def clear_active_block(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.grid[i][j].get() == self.ACTICE:
                    self.grid[i][j].set(self.BLANK)
    
    def can_plot_block(self, x, y, block):
        ret = True
        count=0
        for i in range(4):
            for j in range(4):
                if (0 <= (y - j) < self.ROWS and 0 <=(x + i) < self.COLS):
                    if self.grid[y - j][x + i].get() !=self.BLANK and self.grid[y - j][x + i].get() !=self.ACTICE and  block[3 - j][i].get() == 1:
                        ret = False
                    if self.grid[y - j][x + i].get()==self.BLANK or self.grid[y - j][x + i].get()==self.ACTICE and  block[3 - j][i].get() == 1:
                        count =count+1
        ret = ret and (count !=0)
        
        return ret

    def fix_activeBlock(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.grid[i][j].get() == self.ACTICE:
                    self.grid[i][j].set(self.grid[i][j].getKind())

    def gameover(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.grid[i][j].get() != self.BLANK:
                    self.grid[i][j].set(self.BLOCKEND)

    def clear_full_lines(self):
        tmp_grid = [[Masu(self.BLANK) for _ in range(self.COLS)] for _ in range(self.ROWS)]
        new_row = self.ROWS - 1  # 新しいグリッドの行インデックスを設定

        for i in range(self.ROWS - 1, -1, -1):
            count = 0
            for j in range(self.COLS):
                if self.grid[i][j].get() != self.BLANK and self.grid[i][j].get() != self.WALL:
                    count += 1
            if count == (self.COLS - 2):
                # 1行そろったのでコピーしない
                print(f"delete {count} {i}")
            else:
                # tmp_gridにself.gridをコピー
                for j in range(self.COLS):
                    tmp_grid[new_row][j].setObj(self.grid[i][j])
                new_row -= 1


        # ステージの端を-1で初期化
        for i in range(self.ROWS):
            tmp_grid[i][0].set(self.WALL)         # 左端
            tmp_grid[i][self.COLS-1].set(self.WALL)  # 右端

        self.grid = tmp_grid




class Game:
    X_OFFSET=10
    Y_OFFSET=10
    X_POS_INIT=5
    Y_POS_INIT=0
    FPS=30
    LAST_MOVABLE_COUNT_MAX=2
    def __init__(self):
        self.stage =Stage()
        self.block_queue = deque()
        self.x=self.X_POS_INIT
        self.y=self.Y_POS_INIT
        self.count=0
        self.movble_count=0
        self.isGameOver=False
        self.left_key_counter = 0
        self.right_key_counter = 0
        self.key_delay = 10  # 最初の遅延
        self.key_repeat = 3  # 連続入力の間隔
        pyxel.init(220, 240, title="Hello Pyxel")
        self.block_queue.append(Block())
        self.block_queue.append(Block())
        self.block_queue.append(Block())
        self.activeBlock = self.block_queue.popleft()
        #self.activeBlock = Block()
        pyxel.load("tetris_resource.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            if self.isGameOver:
                self.x=self.X_POS_INIT
                self.y=self.Y_POS_INIT
                self.count=0
                self.movble_count=0
                self.isGameOver=False
                self.left_key_counter = 0
                self.right_key_counter = 0
                del(self.stage)
                self.stage =Stage()

                return
            if self.stage.can_plot_block(self.x,self.y, self.activeBlock.get_rotate_block()):
                self.activeBlock.rotate()
        if self.isGameOver:
            return
        self.count=self.count+1
        if self.count == self.FPS:
            self.count = 0
            self.y = self.y + 1

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.left_key_counter += 1
            if self.left_key_counter == 1 or (self.left_key_counter > self.key_delay )and ((self.left_key_counter - self.key_delay) % self.key_repeat == 0):
                if self.stage.can_plot_block(self.x -1,self.y,self.activeBlock.get_block()):
                    self.x = self.x -1
                    if self.stage.can_plot_block(self.x,self.y+1,self.activeBlock.get_block()) == False and self.movble_count < self.LAST_MOVABLE_COUNT_MAX and self.count > 20:
                        self.count = 0
                        self.movble_count = self.movble_count + 1
        else:
            self.left_key_counter = 0  # キーが離されたらリセット

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.right_key_counter += 1
            if self.right_key_counter == 1 or self.right_key_counter > self.key_delay and (self.right_key_counter - self.key_delay) % self.key_repeat == 0:
                if self.stage.can_plot_block(self.x +1,self.y,self.activeBlock.get_block()):
                    self.x = self.x + 1
                    if self.stage.can_plot_block(self.x,self.y+1,self.activeBlock.get_block()) == False and self.movble_count < self.LAST_MOVABLE_COUNT_MAX and self.count > 20:
                        self.count = 0
                        self.movble_count = self.movble_count + 1
        else:
            self.right_key_counter = 0  # キーが離されたらリセット 
        #if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
        #    self.y -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            if self.stage.can_plot_block(self.x,self.y+1,self.activeBlock.get_block()):
                self.y = self.y + 1
                self.count = 0
                self.movble_count=0


        
        if self.stage.can_plot_block(self.x,self.y,self.activeBlock.get_block()):
            #if self.stage.can_plot_block(self.x,self.y+1,self.activeBlock.get_block()) or self.count < self.LAST_MOVABLE :
            self.stage.clear_active_block()
            self.stage.plot_block(self.x,self.y,self.activeBlock.get_block())
        else:
            self.stage.fix_activeBlock()
            self.stage.clear_full_lines()
            self.x=self.X_POS_INIT
            self.y=self.Y_POS_INIT
            self.movble_count=0
            self.block_queue.append(Block())
            self.activeBlock = self.block_queue.popleft()
            if self.stage.can_plot_block(self.x,self.y,self.activeBlock.get_block())==False:
                print("GameOver")
                self.stage.gameover()
                self.isGameOver=True


    def draw_block(self,block,i,j):
        type_val=block.get()
        if type_val == Stage.ACTICE:
            type_val = block.getKind()
        
        if type_val == Stage.WALL:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,0,10, 10,100)
        elif type_val == Stage.BLOCK7:
            if block.getSpecial()==1:
                pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,(block.getRole()//90)*20 + 100,10, 10,100)
            elif block.getSpecial()==2:
                pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,10,(block.getRole()//90)*20 + 100,10, 10,100)
            elif block.getSpecial()==3:
                pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,(block.getRole()//90)*20 + 110,10, 10,100)
            elif block.getSpecial()==4:
                pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,10,(block.getRole()//90)*20 + 110,10, 10,100)
        elif type_val == Stage.BLOCKEND:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,10,0,10, 10,100)
        else:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,(block.getRole()//90)*10,(type_val-Stage.BLOCK1)*10+10,10, 10,100)


    def draw_next_two_blocks(self):
        next_block1 = self.block_queue[0].get_block()  # キューの先頭要素
        next_block2 = self.block_queue[1].get_block()  # キューの2番目の要素

        # 1つ目の次のブロックを描画
        for i in range(4):
            for j in range(4):
                if next_block1[j][i].get() == 1:
                    pyxel.rect(i * 10 + 170, j * 10 + 20, 8, 8, 9)

        # 2つ目の次のブロックを描画
        for i in range(4):
            for j in range(4):
                if next_block2[j][i].get() == 1:
                    pyxel.rect(i * 10 + 170, j * 10 + 60, 8, 8, 10)

    def draw(self):
        pyxel.cls(0)

        for i in range(Stage.ROWS):
            for j in range(Stage.COLS):
                #Grid
                pyxel.rectb(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 10, 10, 7)
                self.draw_block(self.stage.get_stage_block(i,j),i,j)

        if self.isGameOver:
            pyxel.text(55, 41, "Game Over!!", pyxel.frame_count % 16)
        
        self.draw_next_two_blocks()
Game()
