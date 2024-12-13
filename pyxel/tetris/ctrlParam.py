

class CtrlParam:
    def score_countup(self,line,baseScore):
        score=baseScore
        if line == 0:
            score = score
        elif line == 1:
            score = score+100
        elif line == 2:
            score = score+250
        elif line == 3:
            score = score+500
        elif line == 4:
            score = score+1000
        else:
            score = score+line*300
        return score

    def block_fall_speed_ctrl(self,score):

        if 5000 < score:
            block_fall_speed = 1
        elif 4000 < score:
            block_fall_speed = 2
        elif 3000 < score:
            block_fall_speed = 5
        elif 2000 < score:
            block_fall_speed = 10
        elif 1000 < score:
            block_fall_speed = 20
        else:
            block_fall_speed = 30
        return block_fall_speed
