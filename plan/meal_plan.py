## Class for Meal Plan
from plan.dataset import Dataset
from plan.dish import Dish
from plan.problem import ProblemConfig

from operator import add
import numpy as np
import math

class MealPlan:
    def __init__(self,problem_config:ProblemConfig,dataset:Dataset,dishes:"list[Dish]"=[]) -> None:
        self.plan:"list[Dish]"=dishes
        self.problem_config=problem_config
        self.dataset=dataset

    def add_dish(self,dish:Dish):
        self.plan.append(dish)

    def calculate_nutri(self)->"list[list[int]]":
        ## Calculated for all meals in the day so that we can check individual limits in the future
        nutri_day=[0]*self.problem_config.planning.number_of_nutrients
        nutri_breakfast=[0]*self.problem_config.planning.number_of_nutrients
        nutri_lunch=[0]*self.problem_config.planning.number_of_nutrients
        nutri_snacks=[0]*self.problem_config.planning.number_of_nutrients
        nutri_dinner=[0]*self.problem_config.planning.number_of_nutrients

        for id,dish in enumerate(self.plan):
            if(dish.id==0):
                continue
            nutri_dish=self.dataset.get_dish_nutri(dish)
            # print(nutri_dish)

            nutri_day=list(map(add,nutri_dish,nutri_day))

            if(id<self.problem_config.breakfast_id_limit):
                nutri_breakfast=list(map(add,nutri_dish,nutri_breakfast))
            elif(id<self.problem_config.lunch_id_limit):
                nutri_lunch=list(map(add,nutri_dish,nutri_lunch))
            elif(id<self.problem_config.snacks_id_limit):
                nutri_snacks=list(map(add,nutri_dish,nutri_snacks))
            else:
                nutri_dinner=list(map(add,nutri_dish,nutri_dinner))

        return [
            nutri_day,
            nutri_breakfast,
            nutri_lunch,
            nutri_snacks,
            nutri_dinner
        ]
    
    def calculate_wt(self)->"list[list[int]]":
        ## Calculated for all meals in the day so that we can check individual limits in the future
        wt_day=0
        wt_breakfast=0
        wt_lunch=0
        wt_snacks=0
        wt_dinner=0

        for id,dish in enumerate(self.plan):
            if(dish.id==0):
                continue
            wt_dish=self.dataset.get_dish_weight(dish)
            
            wt_day+=wt_dish
            
            if(id<self.problem_config.breakfast_id_limit):
                wt_breakfast+=wt_dish
            
            elif(id<self.problem_config.lunch_id_limit):
                wt_lunch+=wt_dish
            
            elif(id<self.problem_config.snacks_id_limit):
                wt_snacks+=wt_dish
            
            else:
                wt_dinner+=wt_dish

        return [
            [wt_day],
            [wt_breakfast],
            [wt_lunch],
            [wt_snacks],
            [wt_dinner]
        ]


    @staticmethod
    def checkIfSatisfied(vals,limits) -> bool:
        for i in range(len(vals)):
            if not (limits[i][0]<=vals[i] and vals[i]<=limits[i][1]):
                return False
        return True

    def check_nutri(self,group_index) -> bool:
        nutri=self.calculate_nutri()
        return MealPlan.checkIfSatisfied(
                [nutri[0][0]],
                [self.problem_config.groups[group_index].daily_nutrient_requirements[0]]
            )
   

    def check_wt(self,group_index) -> bool:
        wt=self.calculate_wt()
        return MealPlan.checkIfSatisfied(
                [wt[0][0]],
                [self.problem_config.groups[group_index].daily_weight_requirements[0]]
            )

    def check_no_repeat(self) -> bool:
        dishes=set()
        cnt=0
        for meal in self.plan:
            if(meal.id!=0):
                cnt+=1
                dishes.add(meal.id)
        return cnt==len(dishes)

    def get_combi_value(self)->float:
        value=0
        cnt=0
        for i in range(len(self.plan)):
            if self.plan[i].id==0:
                continue
            for j in range(i+1,len(self.plan)):
                if self.plan[j].id==0 or self.plan[j].meal!=self.plan[i].meal:
                    continue
                cnt+=1
                value+=(self.dataset.get_combi_dish(self.plan[i],self.plan[j]))
        if cnt==0:
            return 0
        return (value/cnt)
    
    @staticmethod
    def sim(v1,v2):
        v1=v1/np.linalg.norm(v1)
        v2=v2/np.linalg.norm(v2)
        return np.linalg.norm(v1-v2)/math.sqrt(2)

    def get_diversity(self)->float:
        value=0
        cnt=0
        for i in range(len(self.plan)):
            if self.plan[i].id==0:
                continue
            for j in range(i+1,len(self.plan)):
                if self.plan[j].id==0 or self.plan[j].meal!=self.plan[i].meal:
                    continue
                cnt+=1
                value+=MealPlan.sim(self.plan[i].vector[1:-1],self.plan[j].vector[1:-1])
        if cnt==0:
            return 0
        return value/cnt
    
    @staticmethod
    def intersection(l1:list,l2:list)->int:
        cnt=0
        for val in l1:
            if val in l2:
                cnt+=1
        return cnt


    def get_pos_preference(self,group_index:int=0,is_final_multiple=False)->float:
        dish_ids=[ dish.cuisine for dish in self.plan for _ in range(dish.quantity)]
        if(len(dish_ids)==0):
            return 0
        prefered_dishes=[]
        if self.problem_config.planning.plan_type=="many_in_one" or is_final_multiple:
            for group in self.problem_config.groups:
                prefered_dishes.extend(group.positive_preferences)
        else:
            prefered_dishes=self.problem_config.groups[group_index].positive_preferences
        return MealPlan.intersection(dish_ids,prefered_dishes)/len(dish_ids)

    def get_neg_preference(self,group_index:int=0,is_final_multiple=False)->float:
        dish_ids=[ dish.cuisine for dish in self.plan for _ in range(dish.quantity)]
        if(len(dish_ids)==0):
            return 0
        rejected_dishes=[]
        if self.problem_config.planning.plan_type=="many_in_one" or is_final_multiple:
            for group in self.problem_config.groups:
                rejected_dishes.extend(group.negative_preferences)
        else:
            rejected_dishes=self.problem_config.groups[group_index].negative_preferences
        return MealPlan.intersection(dish_ids,rejected_dishes)/len(dish_ids)
    
    @staticmethod
    def get_penalty_value(vals,limits):
        p=0
        cnt=0
        for i in range(len(vals)):
            ## lower limit penalty
            if vals[i]<limits[i][0]:
                p+=vals[i]/limits[i][0]-1
                cnt+=1
            ## upper limit penalty
            if vals[i]>limits[i][1]:
                p+=max(-1,1-(vals[i]/limits[i][1]))
                cnt+=1
        if cnt==0:
            return 0
        return p/cnt

    def get_penalty(self,penalty_wts,group_index:int =0):
        if self.problem_config.planning.ga!="hybrid":
            return 0
        nutri=self.calculate_nutri()
        nutri_penalty=MealPlan.get_penalty_value(
            [nutri[0][0]],
            [self.problem_config.groups[group_index].daily_nutrient_requirements[0]]
        )
        
        wt=self.calculate_wt()
        wt_penalty=MealPlan.get_penalty_value(
            [wt[0][0]],
            [self.problem_config.groups[group_index].daily_weight_requirements[0]]
        )

        return penalty_wts[0] * nutri_penalty + penalty_wts[1] * wt_penalty
    