import unittest
from timer import Timer

class TestTimer(unittest.TestCase):
    def test_initial_state(self):
        timer = Timer(100)
        self.assertEqual(timer.intrtval_ms, 100)
        self.assertEqual(timer.count, 0)
        self.assertEqual(timer.targeet_ms, 0)
        self.assertFalse(timer.isTimerComp)
        self.assertFalse(timer.isCountup)

    def test_restart(self):
        timer = Timer(100)
        timer.restart(500)
        self.assertEqual(timer.count, 0)
        self.assertEqual(timer.targeet_ms, 500)
        self.assertFalse(timer.isTimerComp)
        self.assertTrue(timer.isCountup)

    def test_cyclic(self):
        timer = Timer(100)
        timer.restart(500)
        for _ in range(6):  # 6回ループすると、countは6になり、600ms経過したことになる
            timer.cyclic()
        self.assertTrue(timer.isTimerComp)
        self.assertFalse(timer.isCountup)

    def test_isTimerComplate(self):
        timer = Timer(100)
        timer.restart(500)
        self.assertFalse(timer.isTimerComplate())
        for _ in range(5):
            timer.cyclic()
        self.assertFalse(timer.isTimerComplate())
        timer.cyclic()  # ここでタイマーが完了する
        self.assertTrue(timer.isTimerComplate())

    def test_isTimerRunning(self):
        timer = Timer(100)
        self.assertFalse(timer.isTimerRunning())
        timer.restart(500)
        self.assertTrue(timer.isTimerRunning())
        for _ in range(6):  # タイマーが完了するまでサイクルを回す
            timer.cyclic()
        self.assertFalse(timer.isTimerRunning())

    def test_cancel_timer(self):
        timer = Timer(100)
        timer.restart(500)
        timer.cancel_timer()
        self.assertEqual(timer.count, 0)
        self.assertEqual(timer.targeet_ms, 0)
        self.assertFalse(timer.isTimerComp)
        self.assertFalse(timer.isCountup)

    def test_get_count(self):
        timer = Timer(100)
        timer.restart(500)
        for _ in range(3):
            timer.cyclic()
        self.assertEqual(timer.get_count(), 3)

if __name__ == '__main__':
    unittest.main()
