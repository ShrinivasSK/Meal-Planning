## Defining the Dish Class
import numpy as np

VEC_SIZE=300

class Dish:
    def __init__(self,id:int,quantity:int,vector:list[float],title:str,meal:str) -> None:
        self.id=id
        self.title=title
        self.quantity=quantity
        self.meal=meal
        vec=[id]
        vec.extend(vector)
        vec.append(quantity)
        self.vector=np.array(vec,dtype='float64')

    @staticmethod
    def get_padding_dish():
        return Dish(0,0,[0]*VEC_SIZE,"","")

    def __str__(self) -> str:
        return self.title