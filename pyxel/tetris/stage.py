
#import numpy

from blockconst import BlockConst
from masu import Masu
from block import Block

class Stage:
    # クラス属性として定数を定義
    ROWS = 22
    COLS = 12

    def __init__(self):
        # 配列を定義し、ステージの端を-1、それ以外の領域を0で初期化
        self.grid = [[Masu(BlockConst.BLANK) for _ in range(self.COLS)] for _ in range(self.ROWS)]
        
        # ステージの端を-1で初期化
        for i in range(self.ROWS):
            self.grid[i][0].set(BlockConst.WALL)         # 左端
            self.grid[i][self.COLS-1].set(BlockConst.WALL)  # 右端
        for j in range(self.COLS):
            #self.grid[0][j] = BlockConst.WALL         # 上端
            self.grid[self.ROWS-1][j].set(BlockConst.WALL)  # 下端
    def print_grid(self):
        for i in range(self.ROWS):
            row = []
            for j in range(self.COLS):
                row.append(self.grid[i][j].get())
            print(" ".join(map(str, row)))

    
    def get_stage_block(self,row,col):
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            return self.grid[row][col]
        else:
            raise IndexError(f"Index out of bounds: row {row}, col {col}")
    def plot_block(self, x, y, block):
        for i in range(4):
            for j in range(4):
                if (0 <= (y - j) < self.ROWS and 0 <=(x + i) < self.COLS):
                    if block[3 - j][i].get() == 1:
                        if 0 <= (y - j) < self.ROWS and 0 <= (x + i) < self.COLS:
                            self.grid[y - j][x + i].setObj( block[3 - j][i])
                        else:
                            raise IndexError(f"Index out of bounds: y {y}, x {x}")

    def plot_fallblock(self, x, y, block):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.grid[i][j].get() == BlockConst.FALLPOS:
                    self.grid[i][j].set(BlockConst.BLANK)

        for i in range(4):
            for j in range(4):
                if (0 <= (y - j) < self.ROWS and 0 <=(x + i) < self.COLS):
                    if block[3 - j][i].get() == 1:
                        if 0 <= (y - j) < self.ROWS and 0 <= (x + i) < self.COLS:
                            self.grid[y - j][x + i].set(BlockConst.FALLPOS)
                        else:
                            raise IndexError(f"Index out of bounds: y {y}, x {x}")

    def clear_active_block(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.grid[i][j].get() == BlockConst.ACTICE:
                    self.grid[i][j].set(BlockConst.BLANK)
    
    def can_plot_block(self, x, y, block):
        ret = True
        #count=0
        for i in range(4):
            for j in range(4):
                if (0 <= (y - j) < self.ROWS and 0 <=(x + i) < self.COLS):
                    if self.grid[y - j][x + i].get() !=BlockConst.BLANK and self.grid[y - j][x + i].get() !=BlockConst.ACTICE and self.grid[y - j][x + i].get() !=BlockConst.FALLPOS and  block[3 - j][i].get() == 1:
                        ret = False
                    #if (self.grid[y - j][x + i].get()==BlockConst.BLANK or self.grid[y - j][x + i].get()==BlockConst.ACTICE or self.grid[y - j][x + i].get()==BlockConst.FALLPOS) and  block[3 - j][i].get() == 1:
                    #    count =count+1
                else:
                    if ( (x + i) == 0 or (x + i) >= (self.COLS-1) ) and  block[3 - j][i].get() == 1:
                        ret = False
                    if  self.ROWS <= (y - j) and  block[3 - j][i].get() == 1:
                        ret = False
        #ret = ret and (count !=0)
        return ret

    def fix_activeBlock(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.grid[i][j].get() == BlockConst.ACTICE:
                    self.grid[i][j].set(self.grid[i][j].getKind())

    def gameover(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.grid[i][j].get() != BlockConst.BLANK and self.grid[i][j].get() != BlockConst.FALLPOS:
                    self.grid[i][j].set(BlockConst.BLOCKEND)

    def clear_full_lines(self):
        tmp_grid = [[Masu(BlockConst.BLANK) for _ in range(self.COLS)] for _ in range(self.ROWS)]
        new_row = self.ROWS - 1  # 新しいグリッドの行インデックスを設定
        clearLine=0
        for i in range(self.ROWS - 1, -1, -1):
            count = 0
            for j in range(self.COLS):
                if self.grid[i][j].get() != BlockConst.BLANK and self.grid[i][j].get() != BlockConst.WALL and self.grid[i][j].get() != BlockConst.FALLPOS:
                    count += 1
            if count == (self.COLS - 2):
                # 1行そろったのでコピーしない
                #print(f"delete {count} {i}")
                clearLine = clearLine + 1
            else:
                # tmp_gridにself.gridをコピー
                for j in range(self.COLS):
                    tmp_grid[new_row][j].setObj(self.grid[i][j])
                new_row -= 1


        # ステージの端を-1で初期化
        for i in range(self.ROWS):
            tmp_grid[i][0].set(BlockConst.WALL)         # 左端
            tmp_grid[i][self.COLS-1].set(BlockConst.WALL)  # 右端

        self.grid = tmp_grid
        return clearLine

