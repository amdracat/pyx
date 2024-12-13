import numpy
import random


import math
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 30

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
