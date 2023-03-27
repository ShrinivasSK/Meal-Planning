## Defining the Dish Class
import numpy as np

VEC_SIZE=300

class Dish:
    def __init__(self,id:int,quantity:int,vector:"list[float]",title:str,meal:str,cuisine:float,tags:str,category:str) -> None:
        self.id=id
        self.title=title
        self.quantity=quantity
        self.meal=meal
        vec=[id]
        vec.extend(vector)
        vec.append(quantity)
        self.vector=np.array(vec,dtype='float64')
        self.cuisine=cuisine
        self.tags=tags
        self.category=category

    @staticmethod
    def get_padding_dish():
        return Dish(0,0,[0]*VEC_SIZE,"","",-1,"","")

    def __str__(self) -> str:
        if(self.quantity==0):
            return self.title
        return self.title+" : "+str(self.quantity)+" : "+str(self.cuisine)+ " : "+str(self.category)+" : "+str(self.tags)