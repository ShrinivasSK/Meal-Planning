## Individual of the Population: Meal Plan
from NSGA.meal_plan_ import MealPlan

import numpy as np

class Individual:

    def __init__(self, meal_plan: MealPlan) -> None:
        self.rank=None
        self.crowding_distance=None
        self.domination_count=None
        self.dominated_solutions=None
        self.objectives:"list[float]"=list()

        self.meal_plan=meal_plan
        self.features,self.ids=self.getFeaturesAndIds()

    def getFeaturesAndIds(self):
        vec=[meal.vector for meal in self.meal_plan.plan]
        ids=[meal.vector[0] for meal in self.meal_plan.plan]
        return np.array(vec),ids

    
    def __eq__(self, other: object) -> bool:
        if isinstance(self,other.__class__):
            return (self.features==other.features).all()
        return False

    def dominates(self,other:object) -> bool:
        and_condition = True
        or_condition = False
        for first, second in zip(self.objectives, other.objectives):
            # print(first,second)
            and_condition = and_condition and first >= second
            or_condition = or_condition or first > second
        return (and_condition and or_condition)

    def calculate_objectives(self,group_index:int=0)->"list[float]":
        self.objectives= [
            self.meal_plan.get_combi_value(),
            self.meal_plan.get_diversity(),
            self.meal_plan.get_pos_preference(group_index),
            -1*self.meal_plan.get_neg_preference(group_index),
        ]
        return self.objectives

    def __str__(self) -> str:
        if len(self.objectives)==0:
            self.calculate_objectives()
        res=""
        res+="\n"+"Nutrition Values: "+str(self.meal_plan.calculate_nutri()[0])
        res+="\n"+"Weight: "+str(self.meal_plan.calculate_wt()[0][0])
        res+="\n"+"Objective Values: "+str(self.objectives)
        
        res+="\n"+"\n Meal Plan: "
        for id,dish in enumerate(self.meal_plan.plan):
            if dish.id==0:
                continue
            res+="\n"+str(self.meal_plan.problem_config.get_meal_from_id(id))+" "+dish.__str__()

        return res