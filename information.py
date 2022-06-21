from ui import ui
from pokeImage import  getImgAndGenerateTextCloud
from getPokeInfo import _test

class new:
    def __init__(self,item):
        self.item=list(item)
        self.id=str(item[0])
        self.en=str(item[1])
        self.ch=str(item[2])
        
    def pokemon(self):
        getImgAndGenerateTextCloud(self.id,self.en,self.ch)
        #_test(self.ch,self.id)
        ui(self.item)

