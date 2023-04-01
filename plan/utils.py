from plan import MealPlan, ProblemConfig, Dataset

import networkx as nx
from operator import add
import random
from collections import defaultdict
from typing import Tuple

class PlanUtils:
    def __init__(self,dataset:Dataset,problem_config:ProblemConfig) -> None:
        self.problem_config=problem_config
        self.dataset=dataset
        random.seed()

    def get_cliques(self,dataset: Dataset,file:str,lower_limit:int,higher_limit:int)->list:
        G=dataset.get_graph(file)

        cliques=list(nx.enumerate_all_cliques(G))

        clean=[]
        for c in cliques:
            if(len(c)>=lower_limit and len(c)<=higher_limit):
                clean.append(c)

        return clean

    def get_random_quantity(self,group_index=0) -> int:
        return random.randint(self.problem_config.groups[group_index].user_count,self.problem_config.groups[group_index].user_count*2)

    def isValidChild(self,child: MealPlan,group_index:int=0) -> bool:
        if self.problem_config.planning.plan_type=="many_in_one":
            nutri=[0]*self.problem_config.planning.number_of_nutrients
            wt=0
            dishes=set()
            tot=0
            dish_cnts=defaultdict(int)
            for id,dish in enumerate(child.plan):
                if dish.id!=0:
                    dish_cnts[self.problem_config.get_meal_from_id(id)]+=1
                    tot+=1
                    dishes.add(dish.id)
                    nutri=list(map(add,self.dataset.get_dish_nutri(dish),nutri))
                    wt+=self.dataset.get_dish_weight(dish)
            meal_dish_cnt=[
                dish_cnts['Breakfast'],
                dish_cnts['Lunch'],
                dish_cnts['Snacks'],
                dish_cnts['Dinner'],
            ]
            
            nutri_req=nutri_req=self.problem_config.groups[0].daily_nutrient_requirements
            wt_req=self.problem_config.groups[0].daily_weight_requirements
            for group in self.problem_config.groups[1:]:
                wt_req=list(map(lambda l1,l2: list(map(add,l1,l2)),group.daily_weight_requirements,wt_req))
                nutri_req=list(map(lambda l1,l2: list(map(add,l1,l2)),group.daily_nutrient_requirements,nutri_req))

            cnt_limits=[
                [0,(self.problem_config.meal.breakfast_dishes*self.problem_config.planning.group_count)/1.5],
                [0,(self.problem_config.meal.lunch_dishes*self.problem_config.planning.group_count)/1.5],
                [0,(self.problem_config.meal.snacks_dishes*self.problem_config.planning.group_count)],
                [0,(self.problem_config.meal.dinner_dishes*self.problem_config.planning.group_count)/1.5],
            ]

            t=[
                MealPlan.checkIfSatisfied(nutri,nutri_req),
                MealPlan.checkIfSatisfied([wt],wt_req),
                MealPlan.checkIfSatisfied(meal_dish_cnt,cnt_limits), ## Count Limit to Dishes
                len(dishes)==tot, ## no repeat
            ]

            return all(t)


        return all([
            child.check_nutri(group_index),
            child.check_wt(group_index),
            child.check_no_repeat()
        ])


    @staticmethod
    def choose_with_prob(prob: float)->bool:
        if random.random() <= prob:
            return True
        return False
