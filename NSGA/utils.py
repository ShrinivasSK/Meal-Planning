## Utility Functions for NSGA

"""
1. Create Initial Population: From Graph: Done
2. Fast Non Dominated Sort: Done
3. Calculate Crowding Distance, Crowding Operator: Done
5. Is Valid Child: Done
6. Crossover: Done
7. Mutation: Done
8. Tournament, Choose with Prob: Done
9. Create Children
"""

from dis import dis
from NSGA.meal_plan_ import MealPlan
from NSGA.individual_ import Individual
from NSGA.population_ import Population
from NSGA.dataset_ import Dataset
from NSGA.dish_ import Dish
from NSGA.problem_ import ProblemConfig

import networkx as nx
import random
import time
from copy import deepcopy
from typing import Tuple
import numpy as np


class NSGAUtils:

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

    def get_random_quantity(self) -> int:
        return random.randint(self.problem_config.planning.group_count,self.problem_config.planning.group_count*2)

    def create_intitial_population(self,group_index=0) -> Population:
        breakfast_options=self.get_cliques(self.dataset,"breakfast",lower_limit=1,higher_limit=3)
        lunch_options=self.get_cliques(self.dataset,"lunch",lower_limit=3,higher_limit=5)
        snacks_options=self.get_cliques(self.dataset,"snacks",lower_limit=1,higher_limit=3)
        dinner_options=self.get_cliques(self.dataset,"dinner",lower_limit=3,higher_limit=5)

        # print(dinner_options[0])

        population=Population()

        while (len(population)<self.problem_config.NSGA.population_size):
            meal_plan=[]

            ## Add Breakfast Dishes
            breakfast=breakfast_options[random.randint(0,len(breakfast_options)-1)]
            for i_ in range(self.problem_config.meal.breakfast_dishes):
                if i_<len(breakfast):
                    meal_plan.append(
                        Dish(
                            id=breakfast[i_],
                            quantity=self.get_random_quantity(),
                            vector=self.dataset.get_dish_vector(breakfast[i_]),
                            title=self.dataset.get_dish_title(breakfast[i_]),
                            meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                        )
                    )
                else:
                    meal_plan.append(Dish.get_padding_dish())

            ## Add Lunch Dishes
            lunch=lunch_options[random.randint(0,len(lunch_options)-1)]
            for i_ in range(self.problem_config.meal.lunch_dishes):
                if i_<len(lunch):
                    meal_plan.append(
                        Dish(
                            id=lunch[i_],
                            quantity=self.get_random_quantity(),
                            vector=self.dataset.get_dish_vector(lunch[i_]),
                            title=self.dataset.get_dish_title(lunch[i_]),
                            meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                        )
                    )
                else:
                    meal_plan.append(Dish.get_padding_dish())
            
            ## Add Snacks Dishes
            snacks=snacks_options[random.randint(0,len(snacks_options)-1)]
            for i_ in range(self.problem_config.meal.snacks_dishes):
                if i_<len(snacks):
                    meal_plan.append(
                        Dish(
                            id=snacks[i_],
                            quantity=self.get_random_quantity(),
                            vector=self.dataset.get_dish_vector(snacks[i_]),
                            title=self.dataset.get_dish_title(snacks[i_]),
                            meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                        )
                    )
                else:
                    meal_plan.append(Dish.get_padding_dish())

            ## Add Dinner Dishes
            dinner=dinner_options[random.randint(0,len(dinner_options)-1)]
            for i_ in range(self.problem_config.meal.dinner_dishes):
                if i_<len(dinner):
                    meal_plan.append(
                        Dish(
                            id=dinner[i_],
                            quantity=self.get_random_quantity(),
                            vector=self.dataset.get_dish_vector(dinner[i_]),
                            title=self.dataset.get_dish_title(dinner[i_]),
                            meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                        )
                    )
                else:
                    meal_plan.append(Dish.get_padding_dish())

            # for dish in meal_plan:
            #     print(dish)
            # break

            meal_plan=MealPlan(self.problem_config,self.dataset,meal_plan)
            
            ## Check Validity
            if(self.isValidChild(meal_plan,group_index)):
                # print(meal_plan.plan)
                population.append(
                    Individual(
                        meal_plan=meal_plan
                        )
                    )
                # break
            # else:
            #     print("Yo")
            #     break

        return population
    
    def isValidChild(self,child: MealPlan,group_index:int=0) -> bool:
        return all([
            child.check_nutri(group_index),
            child.check_wt(group_index),
            child.check_no_repeat()
        ])

    def fast_nondominated_sort(self, population:Population ) -> None:
        population.fronts = [[]]
        cnt=0
        for individual in population:
            # print("Current Ind Obj",individual.objectives)
            individual.domination_count = 0
            individual.dominated_solutions = []
            for other_individual in population: 
                # print("Other Ind Obj",other_individual.objectives,sep=" ")
                if(individual.ids==other_individual.ids):
                    # print(": same",sep=" ")
                    continue
                if individual.dominates(other_individual):
                    # print(": current dominates",sep=" ")
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    # print(": other dominates",sep=" ")
                    individual.domination_count += 1
                # else:
                    # print(": neither dominates",sep=" ")
            # print()
            if individual.domination_count == 0:
                individual.rank = 0
                cnt+=1
                population.fronts[0].append(individual)
        # print("Count",cnt)
        i = 0
        count = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i+1
                        count = count + 1
                        temp.append(other_individual)
            i = i+1
            population.fronts.append(temp)
        # print(i)

    def calculate_crowding_distance(self, front:list[Individual]) -> None:
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
                front.sort(key=lambda individual: individual.objectives[m])
                front[0].crowding_distance = 10**9
                front[solutions_num-1].crowding_distance = 10**9
                m_values = [individual.objectives[m] for individual in front]
                scale = max(m_values) - min(m_values)
                if scale == 0: scale = 1
                for i in range(1, solutions_num-1):
                    front[i].crowding_distance += (front[i+1].objectives[m] - front[i-1].objectives[m])/scale

    def crowding_operator(self, individual: Individual, other_individual: Individual) -> int:
        if (individual.rank < other_individual.rank) or \
            ((individual.rank == other_individual.rank) and (individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1

    def crossover(self,ind1: Individual,ind2: Individual) -> Tuple[Individual,Individual]:
        meal_plan_child1=[]
        meal_plan_child2=[]
        for i in range(len(ind1.meal_plan.plan)):
            if(NSGAUtils.choose_with_prob(0.5)):
                meal_plan_child1.append(ind1.meal_plan.plan[i])
                meal_plan_child2.append(ind2.meal_plan.plan[i])
            else:
                meal_plan_child1.append(ind2.meal_plan.plan[i])
                meal_plan_child2.append(ind1.meal_plan.plan[i])
        
        return [
            Individual(MealPlan(self.problem_config,self.dataset,meal_plan_child1)),
            Individual(MealPlan(self.problem_config,self.dataset,meal_plan_child2))
        ]


    def mutate(self,ind:Individual)-> Individual:
        meal_plan=[]
        for id,dish in enumerate(ind.meal_plan.plan):
            if(NSGAUtils.choose_with_prob(self.problem_config.NSGA.mutation_parameter)):
                # dish_vec= np.array(deepcopy(dish.vector)[1:-1]).astype('float64')
                # ings=self.dataset.get_random_ingredients()
                # for ing in ings:
                #     # print(ing)
                #     if(NSGAUtils.choose_with_prob(0.5)):
                #         dish_vec=np.add(ing*random.random(),dish_vec)
                #     else:
                #         dish_vec=np.subtract(ing*random.random(),dish_vec)
                # id,dish_vec=self.dataset.get_closest_dish(dish_vec)
                random_dish_id,random_dish_vec=self.dataset.get_random_dish(self.problem_config.get_meal_from_id(id))

                meal_plan.append(
                    Dish(
                        id=random_dish_id,
                        quantity=self.get_random_quantity(),
                        vector=random_dish_vec,
                        title=self.dataset.get_dish_title(random_dish_id),
                        meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                    )
                )
            else:
                meal_plan.append(dish)

        return Individual(MealPlan(self.problem_config,self.dataset,meal_plan))

    def tournament(self, population:Population):
        participants = random.sample(population.population, self.problem_config.NSGA.number_of_tournament_participants)
        best = None
        for participant in participants:
            if best is None or (self.crowding_operator(participant, best) == 1 and NSGAUtils.choose_with_prob(self.problem_config.NSGA.tournament_probability)):
                best = participant

        return best

    @staticmethod
    def choose_with_prob(prob: float)->bool:
        if random.random() <= prob:
            return True
        return False

    def create_children(self,population:Population)-> list[Individual]:
        ## May lead to infinite loop if enough children are never valid
        children=[]

        while len(children)<len(population):
            parent1=self.tournament(population)
            parent2=parent1
            # print(parent1==parent2)
            while parent1==parent2:
                parent2=self.tournament(population)
            
            child1, child2 = self.crossover(parent1,parent2)

            child1=self.mutate(child1)
            child2=self.mutate(child2)

            if(self.isValidChild(child1)):
                child1.calculate_objectives()
                children.append(child1)

            if(self.isValidChild(child2)):
                child2.calculate_objectives()
                children.append(child2)

        return children


