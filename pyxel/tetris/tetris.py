import pyxel
import numpy
import random
class Block:
    def __init__(self):
        
        self.sharp=random_number = random.randint(0, 6)
        #self.sharp=3
        self.block= numpy.zeros((4,4), dtype=int)
        if self.sharp == 0:
            # I
            self.block[0][1]=1 
            self.block[1][1]=1 
            self.block[2][1]=1 
            self.block[3][1]=1
        elif  self.sharp == 1:
            # Z
            self.block[2][0]=1 
            self.block[2][1]=1 
            self.block[3][1]=1 
            self.block[3][2]=1
        elif  self.sharp == 2:
            #S
            self.block[3][0]=1 
            self.block[3][1]=1 
            self.block[2][1]=1 
            self.block[2][2]=1
        elif  self.sharp == 3:
            #」
            self.block[1][2]=1 
            self.block[2][2]=1 
            self.block[3][2]=1 
            self.block[3][1]=1
        elif  self.sharp == 4:
            #L
            self.block[1][1]=1 
            self.block[2][1]=1 
            self.block[3][1]=1 
            self.block[3][2]=1
        elif  self.sharp == 5:
            # 山
            self.block[3][0]=1 
            self.block[3][1]=1 
            self.block[3][2]=1 
            self.block[2][1]=1
        elif  self.sharp == 6:
            #□
            self.block[2][1]=1 
            self.block[2][2]=1 
            self.block[3][1]=1 
            self.block[3][2]=1

        print(f"make block self.sharp :{self.sharp}")
    def __del__(self):
        print("delete block\n")    
    def get_block(self):
        return self.block
    def get_sharp(self):
        return self.sharp

    def get_rotate_block(self):
        return numpy.rot90(self.block, -1)
    def rotate(self):
        self.block = numpy.rot90(self.block, -1)

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

    def __init__(self):
        # 配列を定義し、ステージの端を-1、それ以外の領域を0で初期化
        self.grid = numpy.zeros((self.ROWS, self.COLS), dtype=int)
        
        # ステージの端を-1で初期化
        for i in range(self.ROWS):
            self.grid[i][0] = self.WALL         # 左端
            self.grid[i][self.COLS-1] = self.WALL  # 右端
        for j in range(self.COLS):
            #self.grid[0][j] = self.WALL         # 上端
            self.grid[self.ROWS-1][j] = self.WALL  # 下端
            
        # ステージ上部に左右3つずつ壁(-1)を配置し、その間を0に設定
        for j in range(3):
            self.grid[0][j] = self.WALL         # 左側の壁
            self.grid[0][self.COLS-1-j] = self.WALL # 右側の壁
    
    def display_stage(self):
        # ステージを表示するメソッド
        for row in self.grid:
            print(' '.join(map(str, row)))

    def get_stage_block(self,row,col):
            return self.grid[row][col]
    def plot_block(self, x, y, block):
        for i in range(4):
            for j in range(4):
                if (0 <= (y - j) < self.ROWS and 0 <=(x + i) < self.COLS):
                    if block[3 - j][i] == 1:
                        self.grid[y - j][x + i]= block[3 - j][i]
                        

    def clear_active_block(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.grid[i][j] == self.ACTICE:
                    self.grid[i][j] = self.BLANK
    
    def can_plot_block(self, x, y, block):
        ret = True
        count=0
        for i in range(4):
            for j in range(4):
                if (0 <= (y - j) < self.ROWS and 0 <=(x + i) < self.COLS):
                    if self.grid[y - j][x + i]!=self.BLANK and self.grid[y - j][x + i]!=self.ACTICE and  block[3 - j][i] == 1:
                        ret = False
                    if self.grid[y - j][x + i]==self.BLANK or self.grid[y - j][x + i]==self.ACTICE and  block[3 - j][i] == 1:
                        count =count+1
        ret = ret and (count !=0)
        
        return ret

    def fix_activeBlock(self,type):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.grid[i][j] == self.ACTICE:
                    self.grid[i][j] = type




class Game:
    X_OFFSET=10
    Y_OFFSET=10
    X_POS_INIT=5
    Y_POS_INIT=0
    FPS=30
    LAST_MOVABLE_COUNT_MAX=2
    def __init__(self):
        self.stage =Stage()
        self.x=self.X_POS_INIT
        self.y=self.Y_POS_INIT
        self.count=0
        self.movble_count=0
        pyxel.init(220, 240, title="Hello Pyxel")
        self.activeBlock = Block()
        pyxel.load("tetris_resource.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            if self.stage.can_plot_block(self.x,self.y, self.activeBlock.get_rotate_block()):
                self.activeBlock.rotate()
        
        self.count=self.count+1
        if self.count == self.FPS :
            self.count = 0
            self.y = self.y + 1

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            if self.stage.can_plot_block(self.x -1,self.y,self.activeBlock.get_block()):
                self.x = self.x -1
                if self.stage.can_plot_block(self.x,self.y+1,self.activeBlock.get_block()) == False and self.movble_count < self.LAST_MOVABLE_COUNT_MAX and self.count > 20:
                    self.count = 0
                    self.movble_count = self.movble_count + 1

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            if self.stage.can_plot_block(self.x +1,self.y,self.activeBlock.get_block()):
                self.x = self.x + 1
                if self.stage.can_plot_block(self.x,self.y+1,self.activeBlock.get_block()) == False and self.movble_count < self.LAST_MOVABLE_COUNT_MAX and self.count > 20:
                    self.count = 0
                    self.movble_count = self.movble_count + 1
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
            self.stage.fix_activeBlock(self.conv_sharp2block( self.activeBlock.get_sharp()))
            self.x=self.X_POS_INIT
            self.y=self.Y_POS_INIT
            self.movble_count=0
            del(self.activeBlock)
            self.activeBlock = Block()

    def conv_sharp2block(self,sharp_val):
        return sharp_val + 2

    def draw_block(self,type_val,i,j):
        if type_val == Stage.WALL:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,0,10, 10,100)
        elif  type_val== Stage.BLOCK1:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,10,10, 10,100)
        elif  type_val == Stage.BLOCK2:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,20,10, 10,100)
        elif  type_val == Stage.BLOCK3:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,30,10, 10,100)
        elif  type_val == Stage.BLOCK4:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,40,10, 10,100)
        elif  type_val == Stage.BLOCK5:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,50,10, 10,100)
        elif  type_val== Stage.BLOCK6:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,60,10, 10,100)
        elif  type_val == Stage.BLOCK7:
            pyxel.blt(j*10+self.X_OFFSET, i*10+self.Y_OFFSET, 0,0,70,10, 10,100)

    def draw(self):
        pyxel.cls(0)
        #pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        for i in range(Stage.ROWS):
            for j in range(Stage.COLS):
                if  self.stage.get_stage_block(i,j) == Stage.ACTICE:
                    self.draw_block(self.conv_sharp2block( self.activeBlock.get_sharp()),i,j)
                else:
                    self.draw_block(self.stage.get_stage_block(i,j),i,j)


Game()
