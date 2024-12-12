import unittest
from blockconst import BlockConst
from masu import Masu

class TestMasu(unittest.TestCase):
    def test_initial_state(self):
        masu = Masu(BlockConst.BLANK)
        self.assertEqual(masu.get(), BlockConst.BLANK)
        self.assertEqual(masu.getRole(), 0)
        self.assertEqual(masu.getKind(), 0)
        self.assertEqual(masu.getSpecial(), 0)

    def test_set_and_get(self):
        masu = Masu(BlockConst.BLANK)
        masu.set(BlockConst.BLOCK1)
        self.assertEqual(masu.get(), BlockConst.BLOCK1)

    def test_setRole(self):
        masu = Masu(BlockConst.BLANK)
        masu.setRole(45)
        self.assertEqual(masu.getRole(), 45)
        masu.setRole(360)
        self.assertEqual(masu.getRole(), 45)  # 360度回転しても45度のまま

    def test_setObj(self):
        masu1 = Masu(BlockConst.BLOCK1)
        masu1.setRole(90)
        masu1.setKind(3)
        masu1.setSpecial(5)

        masu2 = Masu(BlockConst.BLANK)
        masu2.setObj(masu1)
        
        self.assertEqual(masu2.get(), BlockConst.BLOCK1)
        self.assertEqual(masu2.getRole(), 90)
        self.assertEqual(masu2.getKind(), 3)
        self.assertEqual(masu2.getSpecial(), 5)

    def test_set_and_getKind(self):
        masu = Masu(BlockConst.BLANK)
        masu.setKind(4)
        self.assertEqual(masu.getKind(), 4)

    def test_set_and_getSpecial(self):
        masu = Masu(BlockConst.BLANK)
        masu.setSpecial(7)
        self.assertEqual(masu.getSpecial(), 7)

if __name__ == '__main__':
    unittest.main()
