import unittest
from blockconst import BlockConst
from masu import Masu
from block import Block
from stage import Stage

class TestStage(unittest.TestCase):
    def setUp(self):
        self.stage = Stage()

    def test_initial_state(self):
        # 左右の壁のチェック
        for i in range(self.stage.ROWS):
            self.assertEqual(self.stage.get_stage_block(i, 0).get(), BlockConst.WALL)
            self.assertEqual(self.stage.get_stage_block(i, self.stage.COLS - 1).get(), BlockConst.WALL)

        # 下の壁のチェック
        for j in range(self.stage.COLS):
            self.assertEqual(self.stage.get_stage_block(self.stage.ROWS - 1, j).get(), BlockConst.WALL)

        # その他のセルがBLANKかどうかをチェック
        for i in range(self.stage.ROWS - 1):
            for j in range(1, self.stage.COLS - 1):
                self.assertEqual(self.stage.get_stage_block(i, j).get(), BlockConst.BLANK)

    def test_get_stage_block(self):
        self.assertEqual(self.stage.get_stage_block(0, 0).get(), BlockConst.WALL)
        with self.assertRaises(IndexError):
            self.stage.get_stage_block(-1, 0)
        with self.assertRaises(IndexError):
            self.stage.get_stage_block(0, -1)
        with self.assertRaises(IndexError):
            self.stage.get_stage_block(self.stage.ROWS, 0)
        with self.assertRaises(IndexError):
            self.stage.get_stage_block(0, self.stage.COLS)

    def test_plot_block(self):
        block = Block(sharp=0)  # I型のブロックを生成
        self.stage.plot_block(5, 5, block.get_block())
        self.assertEqual(self.stage.get_stage_block(5, 6).get(), 1)
        self.assertEqual(self.stage.get_stage_block(4, 6).get(), 1)
        self.assertEqual(self.stage.get_stage_block(3, 6).get(), 1)
        self.assertEqual(self.stage.get_stage_block(2, 6).get(), 1)

    def test_plot_fallblock(self):
        block = Block(sharp=0)  # I型のブロックを生成
        self.stage.plot_fallblock(5, 5, block.get_block())
        self.assertEqual(self.stage.get_stage_block(5, 6).get(), BlockConst.FALLPOS)
        self.assertEqual(self.stage.get_stage_block(4, 6).get(), BlockConst.FALLPOS)
        self.assertEqual(self.stage.get_stage_block(3, 6).get(), BlockConst.FALLPOS)
        self.assertEqual(self.stage.get_stage_block(2, 6).get(), BlockConst.FALLPOS)

    def test_clear_active_block(self):
        block = Block(sharp=0)  # I型のブロックを生成
        self.stage.plot_block(5, 5, block.get_block())
        self.stage.clear_active_block()
        self.assertEqual(self.stage.get_stage_block(5, 6).get(), BlockConst.BLANK)
        self.assertEqual(self.stage.get_stage_block(4, 6).get(), BlockConst.BLANK)
        self.assertEqual(self.stage.get_stage_block(3, 6).get(), BlockConst.BLANK)
        self.assertEqual(self.stage.get_stage_block(2, 6).get(), BlockConst.BLANK)

    def test_can_plot_block(self):
        block = Block(sharp=0)  # I型のブロックを生成
        self.assertTrue(self.stage.can_plot_block(5, 5, block.get_block()))
        self.stage.plot_block(5, 5, block.get_block())
        self.stage.fix_activeBlock()
        self.assertFalse(self.stage.can_plot_block(5, 5, block.get_block()))

    def test_fix_activeBlock(self):
        block = Block(sharp=0)  # I型のブロックを生成
        self.stage.plot_block(5, 5, block.get_block())
        self.stage.fix_activeBlock()
        self.assertEqual(self.stage.get_stage_block(5, 6).get(), BlockConst.BLOCK1)
        self.assertEqual(self.stage.get_stage_block(4, 6).get(), BlockConst.BLOCK1)
        self.assertEqual(self.stage.get_stage_block(3, 6).get(), BlockConst.BLOCK1)
        self.assertEqual(self.stage.get_stage_block(2, 6).get(), BlockConst.BLOCK1)

    def test_gameover(self):
        self.stage.grid[0][0].set(BlockConst.BLOCK1)
        self.stage.gameover()
        for i in range(self.stage.ROWS):
            for j in range(self.stage.COLS):
                if self.stage.grid[i][j].get() != BlockConst.BLANK and self.stage.grid[i][j].get() != BlockConst.FALLPOS:
                    self.assertEqual(self.stage.grid[i][j].get(), BlockConst.BLOCKEND)

    def test_clear_full_lines(self):
        for j in range(1, self.stage.COLS - 1):
            self.stage.grid[self.stage.ROWS - 2][j].set(BlockConst.BLOCK1)
        cleared_lines = self.stage.clear_full_lines()
        self.assertEqual(cleared_lines, 1)
        for j in range(1, self.stage.COLS - 1):
            self.assertEqual(self.stage.get_stage_block(self.stage.ROWS - 2, j).get(), BlockConst.BLANK)

if __name__ == '__main__':
    unittest.main()
