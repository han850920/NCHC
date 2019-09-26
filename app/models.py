import random
import os
class ImgObject():
    def __init__(self):
        self.ID = str()
        self.road = str()
        self.time = str()
        self.name = str()
        self.path = str()
        self.state = bool()
    def set_(self,info,func_id):
        if func_id == 0:
            self.ID = info
        elif func_id == 1:
            self.road = info
        elif func_id == 2:
            self.time = info
        elif func_id == 3:
            self.name = info
        elif func_id == 4:
            self.path = info
        else:
            raise Exception("Json File Format Is Wrong")
    def get_img(self):
        
        file_name = 'img/'+self.name
        
        return file_name

    