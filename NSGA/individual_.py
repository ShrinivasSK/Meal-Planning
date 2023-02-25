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

    def calculate_objectives(self)->"list[float]":
        self.objectives= [
            self.meal_plan.get_combi_value(),
            self.meal_plan.get_diversity(),
            self.meal_plan.get_pos_preference(),
            -1*self.meal_plan.get_neg_preference(),
        ]
        return self.objectives

    ## Useful to maintain compatibility between validity calls between Meal Plan and Individual
    def check_nutri(self,group_index:int):
        return self.meal_plan.check_nutri(group_index)

    def check_wt(self,group_index:int):
        return self.meal_plan.check_wt(group_index)

    def check_no_repeat(self):
        return self.meal_plan.check_no_repeat()

    def __str__(self) -> str:
        res=""
        res+="\n"+"Nutrition Values: "+str(self.meal_plan.calculate_nutri()[0])
        res+="\n"+"Weight: "+str(self.meal_plan.calculate_wt()[0][0])
        res+="\n"+"Objective Values: "+str(self.objectives)
        
        res+="\n"+"\n Meal Plan: "
        for id,dish in enumerate(self.meal_plan.plan):
            res+="\n"+str(id)+" "+dish.__str__()

        return res