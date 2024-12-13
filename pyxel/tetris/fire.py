import pyxel

from particle import Particle2
import random



class Fire:
    def __init__(self,x_s=None,y_s=None,y_g=None):
        if x_s==None:
            self.x    = random.randint(20, 200)
            self.y    = random.randint(200, 240)
            self.goal = random.randint(30, 80)
        else:
            self.x=x_s
            self.y=y_s
            self.goal=y_g
        self.speed1=2
        self.speed2= random.randint(6, 9)
        self.count=0
        self.particles = []
        self.isSet=False
    #---------------------
    # パーティクル１
    #---------------------
    def create_explosion(self,x, y):
        for _ in range(50):
            self.particles.append(Particle2(x, y))

    def isEnd(self):
        return not self.particles and self.isSet
        
    def update(self):
        self.count = self.count+1
        if self.speed1 < self.count:
            self.count=0
            self.y=self.y-self.speed2
        if self.y < self.goal:
            if not self.isSet:
                self.isSet = True
                self.create_explosion(self.x,self.y)

        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
        

    def draw(self):
        for particle in self.particles:
            pyxel.pset(particle.x, particle.y, 8 + particle.life % 8)
        if self.y > self.goal:
            pyxel.text(self.x, self.y, "*", pyxel.frame_count % 16)

