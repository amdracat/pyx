import pyxel

class CrossKey:
    BASE_X=132
    BASE_Y=145
    BASE_SIZE=28
    def __init__(self):
        self.x_base=self.BASE_X
        self.y_base=self.BASE_Y
        self.size=self.BASE_SIZE
    
    def draw(self):
        #x_start=130
        #y_start=145
        #size=30
        x_start=self.x_base
        y_start=self.y_base
        size=self.size
        col=pyxel.COLOR_WHITE
        notActive=1
        active=pyxel.COLOR_WHITE
        colUp=notActive
        colDown=notActive
        colLeft=notActive
        colRight=notActive
        colCenter=notActive
        
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            if self.mouseUp():
                colUp=active
            elif self.mouseDown():
                colDown=active           
            elif self.mouseLeft():
                colLeft=active      
            elif self.mouseRight():
                colRight=active
            elif self.mouseCenter():
                colCenter=active   



        pyxel.line(x_start+size*1,y_start+size*0,x_start+size*2,y_start+size*0, colUp)
        pyxel.line(x_start+size*2,y_start+size*0,x_start+size*2,y_start+size*1, colUp)
        pyxel.line(x_start+size*2,y_start+size*1,x_start+size*3,y_start+size*1, colRight)
        pyxel.line(x_start+size*3,y_start+size*1,x_start+size*3,y_start+size*2, colRight)
        pyxel.line(x_start+size*3,y_start+size*2,x_start+size*2,y_start+size*2, colRight)
        pyxel.line(x_start+size*2,y_start+size*2,x_start+size*2,y_start+size*3, colDown)
        pyxel.line(x_start+size*2,y_start+size*3,x_start+size*1,y_start+size*3, colDown)
        pyxel.line(x_start+size*1,y_start+size*3,x_start+size*1,y_start+size*2, colDown)
        pyxel.line(x_start+size*1,y_start+size*2,x_start+size*0,y_start+size*2, colLeft)
        pyxel.line(x_start+size*0,y_start+size*2,x_start+size*0,y_start+size*1, colLeft)
        pyxel.line(x_start+size*0,y_start+size*1,x_start+size*1,y_start+size*1, colLeft)
        pyxel.line(x_start+size*1,y_start+size*1,x_start+size*1,y_start+size*0, colUp)
        pyxel.circb(x_start+size*1.5, y_start+size*1.5, size/2, colCenter)

    def mouseUp(self):
        pos=[self.x_base+self.size*1,self.x_base+self.size*2,self.y_base+self.size*0,self.y_base+self.size*1]
        return ( pos[0] < pyxel.mouse_x < pos[1] and  pos[2] < pyxel.mouse_y < pos[3])
    def mouseDown(self):
        pos=[self.x_base+self.size*1,self.x_base+self.size*2,self.y_base+self.size*2,self.y_base+self.size*3]
        return ( pos[0] < pyxel.mouse_x < pos[1] and  pos[2] < pyxel.mouse_y < pos[3])
    def mouseLeft(self):
        pos=[self.x_base+self.size*0,self.x_base+self.size*1,self.y_base+self.size*1,self.y_base+self.size*2]
        return ( pos[0] < pyxel.mouse_x < pos[1] and  pos[2] < pyxel.mouse_y < pos[3])
    def mouseRight(self):
        pos=[self.x_base+self.size*2,self.x_base+self.size*3,self.y_base+self.size*1,self.y_base+self.size*2]
        return ( pos[0] < pyxel.mouse_x < pos[1] and  pos[2] < pyxel.mouse_y < pos[3])
    def mouseCenter(self):
        pos=[self.x_base+self.size*1,self.x_base+self.size*2,self.y_base+self.size*1,self.y_base+self.size*2]
        return ( pos[0] < pyxel.mouse_x < pos[1] and  pos[2] < pyxel.mouse_y < pos[3])
