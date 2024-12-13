import unittest
from unittest.mock import patch, MagicMock
from tetris import Game  # あなたのゲームのクラスが保存されているモジュール名に変更してください

class TestGame(unittest.TestCase):

    def setUp(self):
        with patch('pyxel.init'), patch('pyxel.load'), patch('pyxel.run'):
            self.game = Game()

    def test_initialize(self):
        self.game.initialize(True)
        self.assertEqual(self.game.x, self.game.X_POS_INIT)
        self.assertEqual(self.game.y, self.game.Y_POS_INIT)
        self.assertFalse(self.game.isGameOver)
        self.assertEqual(len(self.game.block_queue), 3)

    def test_score_countup(self):
        self.game.score = 0
        self.game.score_countup(1)
        self.assertEqual(self.game.score, 100)
        self.game.score_countup(2)
        self.assertEqual(self.game.score, 350)
        self.game.score_countup(4)
        self.assertEqual(self.game.score, 1350)

    def test_block_fall_speed_ctrl(self):
        self.game.score = 6000
        self.game.block_fall_speed_ctrl()
        self.assertEqual(self.game.block_fall_speed, 1)
        self.game.score = 3500
        self.game.block_fall_speed_ctrl()
        self.assertEqual(self.game.block_fall_speed, 5)
        self.game.score = 1000
        self.game.block_fall_speed_ctrl()
        self.assertEqual(self.game.block_fall_speed, 30)

if __name__ == '__main__':
    unittest.main()
