import unittest
from block import Block
from blockconst import BlockConst
from masu import Masu

class TestBlock(unittest.TestCase):
    def test_random_initialization(self):
        block = Block()
        self.assertIn(block.sharp, range(7))
        self.assertEqual(len(block.block), 4)
        self.assertTrue(all(len(row) == 4 for row in block.block))

    def test_specific_initialization(self):
        for i in range(7):
            block = Block(sharp=i)
            self.assertEqual(block.sharp, i)
            self.assertEqual(len(block.block), 4)
            self.assertTrue(all(len(row) == 4 for row in block.block))

            if i == 0:
                self.assertEqual(block.center, Block.CENTER_CENTER)
                self.assertEqual(block.kind, BlockConst.BLOCK1)
                self.assertEqual(block.centrx, 15)
                self.assertEqual(block.centry, 20)
            elif i == 1:
                self.assertEqual(block.center, Block.CENTER_ZURE)
                self.assertEqual(block.kind, BlockConst.BLOCK2)
                self.assertEqual(block.centrx, 15)
                self.assertEqual(block.centry, 30)
            elif i == 2:
                self.assertEqual(block.center, Block.CENTER_ZURE)
                self.assertEqual(block.kind, BlockConst.BLOCK3)
                self.assertEqual(block.centrx, 15)
                self.assertEqual(block.centry, 30)
            elif i == 3:
                self.assertEqual(block.center, Block.CENTER_ZURE)
                self.assertEqual(block.kind, BlockConst.BLOCK4)
                self.assertEqual(block.centrx, 10)
                self.assertEqual(block.centry, 25)
            elif i == 4:
                self.assertEqual(block.center, Block.CENTER_ZURE)
                self.assertEqual(block.kind, BlockConst.BLOCK5)
                self.assertEqual(block.centrx, 15)
                self.assertEqual(block.centry, 25)
            elif i == 5:
                self.assertEqual(block.center, Block.CENTER_ZURE)
                self.assertEqual(block.kind, BlockConst.BLOCK6)
                self.assertEqual(block.centrx, 15)
                self.assertEqual(block.centry, 20)
            elif i == 6:
                self.assertEqual(block.center, Block.CENTER_CENTER)
                self.assertEqual(block.kind, BlockConst.BLOCK7)
                self.assertEqual(block.centrx, 20)
                self.assertEqual(block.centry, 20)

    def test_rotate_90_degrees(self):
        block = Block(sharp=0)  # 任意のsharp値で初期化
        original_block = block.get_block()
        original_matrix = [
            [Masu(BlockConst.BLANK), Masu(BlockConst.ACTICE), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)],
            [Masu(BlockConst.BLANK), Masu(BlockConst.ACTICE), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)],
            [Masu(BlockConst.BLANK), Masu(BlockConst.ACTICE), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)],
            [Masu(BlockConst.BLANK), Masu(BlockConst.ACTICE), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)]
        ]
        
        # 手動で作成した回転後の期待される行列
        expected_matrix = [
            [Masu(BlockConst.BLANK), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)],
            [Masu(BlockConst.ACTICE), Masu(BlockConst.ACTICE), Masu(BlockConst.ACTICE), Masu(BlockConst.ACTICE)],
            [Masu(BlockConst.BLANK), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)],
            [Masu(BlockConst.BLANK), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)]
        ]

        for i in range(4):
            for j in range(4):
                self.assertEqual(original_block[i][j].get(), original_matrix[i][j].get())

        rotated_matrix = block.rotate_90_degrees(original_matrix)
        
        for i in range(4):
            for j in range(4):
                self.assertEqual(rotated_matrix[i][j].get(), expected_matrix[i][j].get())
    

    def test_rotate_90_degrees2(self):
        block = Block(sharp=1)
        original_block = block.get_block()
        
        # 手動で作成した回転前の行列
        expected_block_before = [
            [Masu(BlockConst.BLANK), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)],
            [Masu(BlockConst.BLANK), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)],
            [Masu(BlockConst.ACTICE), Masu(BlockConst.ACTICE), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)],
            [Masu(BlockConst.BLANK), Masu(BlockConst.ACTICE), Masu(BlockConst.ACTICE), Masu(BlockConst.BLANK)],
        ]

        for i in range(4):
            for j in range(4):
                self.assertEqual(original_block[i][j].get(), expected_block_before[i][j].get())
        
        rotated_block = block.rotate_90_degrees2(original_block)
        
        # 手動で作成した回転後の行列
        expected_block_after = [
            [Masu(BlockConst.BLANK), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)],
            [Masu(BlockConst.BLANK), Masu(BlockConst.ACTICE), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)],
            [Masu(BlockConst.ACTICE), Masu(BlockConst.ACTICE), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)],
            [Masu(BlockConst.ACTICE), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK), Masu(BlockConst.BLANK)],
        ]

        for i in range(4):
            for j in range(4):
                self.assertEqual(rotated_block[i][j].get(), expected_block_after[i][j].get())

    def test_get_rotate_block(self):
        block = Block(sharp=0)
        new_block = block.get_rotate_block()
        self.assertEqual(len(new_block), 4)
        self.assertTrue(all(len(row) == 4 for row in new_block))

    def test_rotate(self):
        block = Block(sharp=0)
        block.rotate()
        rotated_block = block.get_block()
        self.assertEqual(len(rotated_block), 4)
        self.assertTrue(all(len(row) == 4 for row in rotated_block))

    def test_get_center_x(self):
        block = Block(sharp=0)
        self.assertEqual(block.get_center_x(), 15)

    def test_get_center_y(self):
        block = Block(sharp=0)
        self.assertEqual(block.get_center_y(), 20)

if __name__ == '__main__':
    unittest.main()
