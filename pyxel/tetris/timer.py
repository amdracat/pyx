
class Timer:
    def __init__(self,interval_ms):
        self.intrtval_ms = interval_ms
        self.count=0
        self.targeet_ms=0
        self.isTimerComp=False
        self.isCountup=False
    
    def restart(self,aim_ms):
        self.count=0
        self.targeet_ms=aim_ms
        self.isTimerComp=False
        self.isCountup=True
    
    def cyclic(self):
        if self.isCountup != True:
            return
        self.count=self.count+1
        if self.targeet_ms < self.count * self.intrtval_ms:
            self.isTimerComp=True
            self.isCountup=False

    def isTimerComplate(self):
        return self.isTimerComp

    def isTimerRunning(self):
        return self.isCountup


    def cancel_timer(self):
        self.count=0
        self.targeet_ms=0
        self.isTimerComp=False
        self.isCountup=False

    def get_count(self):
        return self.count
