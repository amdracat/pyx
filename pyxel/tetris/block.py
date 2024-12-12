import numpy
import random
from blockconst import BlockConst
from masu import Masu




class Block:
    CENTER_CENTER=0
    CENTER_ZURE=1
    def __init__(self):
        
        self.sharp=random_number = random.randint(0, 6)
        #self.sharp=0
        self.block  = [[Masu(BlockConst.BLANK) for _ in range(4)] for _ in range(4)]
        self.center=self.CENTER_CENTER
        self.kind=0
        self.centrx=0
        self.centry=0
        
        if self.sharp == 0:
            # I
            self.block[0][1].set(1) 
            self.block[1][1].set(1) 
            self.block[2][1].set(1) 
            self.block[3][1].set(1) 
            self.center=self.CENTER_CENTER
            self.kind=BlockConst.BLOCK1
            self.centrx=15
            self.centry=20
        elif  self.sharp == 1:
            # Z
            self.block[2][0].set(1) 
            self.block[2][1].set(1) 
            self.block[3][1].set(1) 
            self.block[3][2].set(1)
            self.center=self.CENTER_ZURE
            self.kind=BlockConst.BLOCK2
            self.centrx=15
            self.centry=30
        elif  self.sharp == 2:
            #S
            self.block[3][0].set(1) 
            self.block[3][1].set(1) 
            self.block[2][1].set(1) 
            self.block[2][2].set(1)
            self.center=self.CENTER_ZURE
            self.kind=BlockConst.BLOCK3
            self.centrx=15
            self.centry=30
        elif  self.sharp == 3:
            #」
            self.block[1][1].set(1) 
            self.block[2][1].set(1) 
            self.block[3][1].set(1) 
            self.block[3][0].set(1)
            self.center=self.CENTER_ZURE
            self.kind=BlockConst.BLOCK4
            self.centrx=10
            self.centry=25 
        elif  self.sharp == 4:
            #L
            self.block[1][1].set(1) 
            self.block[2][1].set(1) 
            self.block[3][1].set(1) 
            self.block[3][2].set(1)
            self.center=self.CENTER_ZURE
            self.kind=BlockConst.BLOCK5
            self.centrx=15
            self.centry=25 
        elif  self.sharp == 5:
            # 山
            self.block[2][0].set(1) 
            self.block[2][1].set(1) 
            self.block[2][2].set(1) 
            self.block[1][1].set(1)
            self.center=self.CENTER_ZURE
            self.kind=BlockConst.BLOCK6
            self.centrx=15
            self.centry=20
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
            self.centrx=20
            self.centry=20 
            self.kind=BlockConst.BLOCK7
        size = len(self.block)
        for i in range(size):
            for j in range(size):
                if self.block[i][j].get()==1:
                    self.block[i][j].setKind(self.kind)

    def print_state(self):
        print(f"Shape: {self.sharp}")
        print(f"Center: {self.center}")
        print(f"Kind: {self.kind}")
        print(f"Center X: {self.centrx}")
        print(f"Center Y: {self.centry}")
        print("Block State:")
        for i in range(4):
            row = []
            for j in range(4):
                row.append(self.block[i][j].get())
            print(" ".join(map(str, row)))


    def get_block(self):
        return self.block

    # ブロックを90度回転させる関数4×4中心
    def rotate_90_degrees(self,matrix):
        size = len(matrix)
        new_matrix = [[Masu(BlockConst.BLANK) for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                new_matrix[j][size - 1 - i].setObj(matrix[i][j])
        return new_matrix

    # ブロックを90度回転させる関数3×3中心
    def rotate_90_degrees2(self,matrix):
        size = len(matrix)
        new_matrix = [[Masu(BlockConst.BLANK) for _ in range(size)] for _ in range(size)]
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
        if self.kind!=BlockConst.BLOCK7:
            self.block=self.get_rotate_block()
        size = len(self.block)
        for i in range(size):
            for j in range(size):
                self.block[i][j].setRole(90)

    def get_center_x(self):
        return self.centrx

    def get_center_y(self):
        return self.centry
