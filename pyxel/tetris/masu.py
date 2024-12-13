
from blockconst import BlockConst

class Masu:
    def __init__(self, val):
        self.val = val  # マスの種類
        self.role=0
        self.kind=0
        self.special=0
    def set(self,val):
        self.val = val  # マスの種類
    def get(self):
        return self.val
    def setRole(self,val):
        self.role = (self.role + val)%360
    def getRole(self):
        return self.role
    def setObj(self, obj):
        self.val = obj.get()
        self.role = obj.getRole()
        self.kind = obj.getKind()
        self.special = obj.getSpecial()
    def setKind(self,val):
        self.kind = val  # マスの種類
    def getKind(self):
        return self.kind
    def setSpecial(self,val):
        self.special = val  # マスの種類
    def getSpecial(self):
        return self.special


