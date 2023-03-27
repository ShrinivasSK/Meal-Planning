from plan import MealPlan, Individual, ProblemConfig, Dataset, Dish, PlanUtils
from HybridGA.population import Population

import random
from typing import Tuple

class HybridGAUtils:
    def __init__(self,dataset:Dataset,problem_config:ProblemConfig) -> None:
        self.problem_config=problem_config
        self.dataset=dataset
        random.seed()

    def create_initial_population_many(self)->Population:
        pass

    def create_intitial_population(self,group_index:int=0)->Population:
        pass

    def find_best_solution(self,population)->Tuple[Individual,float]:
        pass

    def create_children(self,population,group_index:int=0)->dict[str,list[Individual]]:
        pass

    def survivor_selection(self,population)->Population:
        pass

    def get_pareto_front(self,population)-> list[Individual]:
        pass

