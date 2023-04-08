from collections import defaultdict
import copy
from plan import MealPlan, Individual, ProblemConfig, Dataset, Dish, PlanUtils
from HybridGA.population import HybridGAPopulation

import random
from typing import Tuple
import numpy as np

## Current Error: Length of Meal Plans is changing due to some reason
class HybridGAUtils:
    def __init__(self,dataset:Dataset,problem_config:ProblemConfig) -> None:
        self.problem_config=problem_config
        self.dataset=dataset
        self.plan_utils=PlanUtils(dataset,problem_config)
        random.seed()

    def create_initial_population_many(self,limit:int)->HybridGAPopulation:
        breakfast_options=self.plan_utils.get_cliques(self.dataset,"breakfast",lower_limit=1,higher_limit=3)
        lunch_options=self.plan_utils.get_cliques(self.dataset,"lunch",lower_limit=1,higher_limit=5)
        snacks_options=self.plan_utils.get_cliques(self.dataset,"snacks",lower_limit=1,higher_limit=3)
        dinner_options=self.plan_utils.get_cliques(self.dataset,"dinner",lower_limit=1,higher_limit=5)

        population=HybridGAPopulation()

        while (len(population)<limit):
            meal_plan=[]

            ## Add Breakfast Dishes
            for group_index in range(self.problem_config.planning.group_count):
                breakfast=breakfast_options[random.randint(0,len(breakfast_options)-1)]
                for i_ in range(self.problem_config.meal.breakfast_dishes):
                    if i_<len(breakfast):
                        meal_plan.append(
                            Dish(
                                id=breakfast[i_],
                                quantity=self.plan_utils.get_random_quantity(group_index),
                                vector=self.dataset.get_dish_vector(breakfast[i_]),
                                title=self.dataset.get_dish_title(breakfast[i_]),
                                meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                                cuisine=self.dataset.get_dish_cuisine(breakfast[i_]),
                                category=self.dataset.get_dish_category(breakfast[i_]),
                                tags=self.dataset.get_dish_tags(breakfast[i_])
                            )
                        )
                    else:
                        meal_plan.append(Dish.get_padding_dish())

            ## Add Lunch Dishes
            for group_index in range(self.problem_config.planning.group_count):
                lunch=lunch_options[random.randint(0,len(lunch_options)-1)]
                for i_ in range(self.problem_config.meal.lunch_dishes):
                    if i_<len(lunch):
                        meal_plan.append(
                            Dish(
                                id=lunch[i_],
                                quantity=self.plan_utils.get_random_quantity(group_index),
                                vector=self.dataset.get_dish_vector(lunch[i_]),
                                title=self.dataset.get_dish_title(lunch[i_]),
                                meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                                cuisine=self.dataset.get_dish_cuisine(lunch[i_]),
                                category=self.dataset.get_dish_category(lunch[i_]),
                                tags=self.dataset.get_dish_tags(lunch[i_])
                            )
                        )
                    else:
                        meal_plan.append(Dish.get_padding_dish())
            
            ## Add Snacks Dishes
            for group_index in range(self.problem_config.planning.group_count):
                snacks=snacks_options[random.randint(0,len(snacks_options)-1)]
                for i_ in range(self.problem_config.meal.snacks_dishes):
                    if i_<len(snacks):
                        meal_plan.append(
                            Dish(
                                id=snacks[i_],
                                quantity=self.plan_utils.get_random_quantity(group_index),
                                vector=self.dataset.get_dish_vector(snacks[i_]),
                                title=self.dataset.get_dish_title(snacks[i_]),
                                meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                                cuisine=self.dataset.get_dish_cuisine(snacks[i_]),
                                category=self.dataset.get_dish_category(snacks[i_]),
                                tags=self.dataset.get_dish_tags(snacks[i_])
                            )
                        )
                    else:
                        meal_plan.append(Dish.get_padding_dish())

            ## Add Dinner Dishes
            for group_index in range(self.problem_config.planning.group_count):
                dinner=dinner_options[random.randint(0,len(dinner_options)-1)]
                for i_ in range(self.problem_config.meal.dinner_dishes):
                    if i_<len(dinner):
                        meal_plan.append(
                            Dish(
                                id=dinner[i_],
                                quantity=self.plan_utils.get_random_quantity(group_index),
                                vector=self.dataset.get_dish_vector(dinner[i_]),
                                title=self.dataset.get_dish_title(dinner[i_]),
                                meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                                cuisine=self.dataset.get_dish_cuisine(dinner[i_]),
                                category=self.dataset.get_dish_category(dinner[i_]),
                                tags=self.dataset.get_dish_tags(dinner[i_])
                            )
                        )
                    else:
                        meal_plan.append(Dish.get_padding_dish())
            
            meal_plan=MealPlan(self.problem_config,self.dataset,meal_plan)
            
            ## Check Validity and add to correct group
            dishes=set()
            for id,dish in enumerate(meal_plan):
                if dish.id!=0:
                    tot+=1
            if len(dishes)!=tot:
                continue
            if(self.plan_utils.isValidChild(meal_plan)):
                if len(population["feasible"])>=self.problem_config.init_feasible_population_limit:
                    continue
                population["feasible"].append(
                    Individual(
                        meal_plan=meal_plan
                        )
                    )
            else:
                if len(population["feasible"])>=self.problem_config.init_infeasible_population_limit:
                    continue
                population["infeasible"].append(
                    Individual(
                        meal_plan=meal_plan
                        )
                )
                
        
        return population

    def create_intitial_population(self,limit:int,group_index:int=0)->HybridGAPopulation:
        breakfast_options=self.plan_utils.get_cliques(self.dataset,"breakfast",lower_limit=1,higher_limit=3)
        lunch_options=self.plan_utils.get_cliques(self.dataset,"lunch",lower_limit=3,higher_limit=5)
        snacks_options=self.plan_utils.get_cliques(self.dataset,"snacks",lower_limit=1,higher_limit=3)
        dinner_options=self.plan_utils.get_cliques(self.dataset,"dinner",lower_limit=3,higher_limit=5)

        population=HybridGAPopulation()

        while (len(population)<limit):
            meal_plan=[]

            ## Add Breakfast Dishes
            breakfast=breakfast_options[random.randint(0,len(breakfast_options)-1)]
            for i_ in range(self.problem_config.meal.breakfast_dishes):
                if i_<len(breakfast):
                    meal_plan.append(
                        Dish(
                            id=breakfast[i_],
                            quantity=self.plan_utils.get_random_quantity(group_index),
                            vector=self.dataset.get_dish_vector(breakfast[i_]),
                            title=self.dataset.get_dish_title(breakfast[i_]),
                            meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                            cuisine=self.dataset.get_dish_cuisine(breakfast[i_]),
                            category=self.dataset.get_dish_category(breakfast[i_]),
                            tags=self.dataset.get_dish_tags(breakfast[i_])
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
                            quantity=self.plan_utils.get_random_quantity(group_index),
                            vector=self.dataset.get_dish_vector(lunch[i_]),
                            title=self.dataset.get_dish_title(lunch[i_]),
                            meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                            cuisine=self.dataset.get_dish_cuisine(lunch[i_]),
                            category=self.dataset.get_dish_category(lunch[i_]),
                            tags=self.dataset.get_dish_tags(lunch[i_])
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
                            quantity=self.plan_utils.get_random_quantity(group_index),
                            vector=self.dataset.get_dish_vector(snacks[i_]),
                            title=self.dataset.get_dish_title(snacks[i_]),
                            meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                            cuisine=self.dataset.get_dish_cuisine(snacks[i_]),
                            category=self.dataset.get_dish_category(snacks[i_]),
                            tags=self.dataset.get_dish_tags(snacks[i_])
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
                            quantity=self.plan_utils.get_random_quantity(group_index),
                            vector=self.dataset.get_dish_vector(dinner[i_]),
                            title=self.dataset.get_dish_title(dinner[i_]),
                            meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                            cuisine=self.dataset.get_dish_cuisine(dinner[i_]),
                            category=self.dataset.get_dish_category(dinner[i_]),
                            tags=self.dataset.get_dish_tags(dinner[i_])
                        )
                    )
                else:
                    meal_plan.append(Dish.get_padding_dish())


            meal_plan=MealPlan(self.problem_config,self.dataset,meal_plan)
            
            ## Check Validity and add to correct group
            if not meal_plan.check_no_repeat():
                continue
            if(self.plan_utils.isValidChild(meal_plan)):
                # if len(population["feasible"])>=self.problem_config.init_feasible_population_limit:
                #     continue

                ind=Individual(
                        meal_plan=meal_plan
                        )
                ind.feasiblity=True
                population["feasible"].append(
                        ind
                    )
            else:
                # if len(population["infeasible"])>=self.problem_config.init_infeasible_population_limit:
                #     continue
                ind=Individual(
                        meal_plan=meal_plan
                        )
                ind.feasiblity=False
                population["infeasible"].append(
                        ind
                    )

        return population

    def find_best_solution(self,population:HybridGAPopulation)->Tuple[Individual,float]:
        best_obj=0
        best_ind=None
        for ind in population["feasible"]:
            ## Sum is taken to get one metric to quantify quality of solution
            ## Biased Fitness not considered as that is based on ranks that depends on the 
            ## population at that time
            obj=sum(ind.objectives)

            if best_obj<obj:
                best_obj=obj
                best_ind=ind

        return best_ind,best_obj
    
    def better(self,individual:Individual,other_individual:Individual)->bool:
        ## Returns True if Ind1 is better than Ind2 based on biased fitness function
        # return ind1.biased_fitness>=ind2.biased_fitness

        ## Better based on crowding operator
        if (individual.rank < other_individual.rank) or \
            ((individual.rank == other_individual.rank) and (individual.crowding_distance > other_individual.crowding_distance)):
            return True
        else:
            return False
    
    def tournament(self, population:HybridGAPopulation):
        choices=[]
        choices.extend(population["feasible"])
        choices.extend(population["infeasible"])

        participants = random.sample(choices, self.problem_config.HybridGA.number_of_tournament_participants)
        best = None
        for participant in participants:
            if best is None or (self.better(participant,best) and PlanUtils.choose_with_prob(self.problem_config.NSGA.tournament_probability)):
                best = participant

        return best
    
    def educate(self,children:"dict[str,list[Individual]]",penalty_wts,group_index:int=0)->"dict[str,list[Individual]]":
        updated_children={
            'feasible':[],
            'infeasible':[],
        }
        ## Improve Feasible
        for child in children["feasible"]:
            if random.random()<=self.problem_config.HybridGA.education_probability:
                dishes_by_meal=defaultdict(list)
                for id,dish in enumerate(child.meal_plan.plan):
                    dishes_by_meal[self.problem_config.get_meal_from_id(id)].append(dish)

                ## Improve dishes by meal individually
                ## by sampling meals from better candidates
                improved_plan=[]
                for meal,dishes in dishes_by_meal.items():
                    improved_plan.extend(self.improve_meal(dishes,meal,group_index))
                
                improved_plan=MealPlan(self.problem_config,self.dataset,improved_plan)
                
                # best_ind=None
                # best_val=0
                # for i in range(3**4):
                #     curr_plan=[]
                #     curr_plan.extend(improved[0][i%(len(improved[0]))])
                #     curr_plan.extend(improved[1][(i//3)%(len(improved[1]))])
                #     curr_plan.extend(improved[2][(i//9)%(len(improved[2]))])
                #     curr_plan.extend(improved[3][(i//27)%(len(improved[3]))])

                #     meal_plan=MealPlan(self.problem_config,self.dataset,curr_plan)
                #     if(self.plan_utils.isValidChild(meal_plan)):
                #         temp_ind=Individual(meal_plan)
                #         obj=temp_ind.calculate_objectives(penalty_wts,group_index)
                #         if best_val<sum(obj):
                #             best_val=sum(obj)
                #             best_ind=copy.deepcopy(temp_ind)
                
                if self.plan_utils.isValidChild(improved_plan):
                    improved_ind=Individual(improved_plan)
                    improved_ind.calculate_objectives(penalty_wts,group_index)
                    improved_ind.feasiblity=True
                    updated_children["feasible"].append(improved_ind)
                else:
                    updated_children["feasible"].append(child)        
            else:
                updated_children["feasible"].append(child)
        
        ## Improve Infeasible
        for child in children["infeasible"]:
            if random.random()<=self.problem_config.HybridGA.education_probability:
                dishes_by_meal=defaultdict(list)
                for id,dish in enumerate(child.meal_plan.plan):
                    dishes_by_meal[self.problem_config.get_meal_from_id(id)].append(dish)

                ## Improve dishes by meal individually
                ## by sampling meals from better candidates
                improved_plan=[]
                for meal,dishes in dishes_by_meal.items():
                    improved_plan.extend(self.improve_meal(dishes,meal,group_index))
                
                improved_plan=MealPlan(self.problem_config,self.dataset,improved_plan)
                # best_ind=None
                # best_val=0
                # for i in range(3**4):
                #     curr_plan=[]
                #     curr_plan.extend(improved[0][i%(len(improved[0]))])
                #     curr_plan.extend(improved[1][(i//3)%(len(improved[1]))])
                #     curr_plan.extend(improved[2][(i//9)%(len(improved[2]))])
                #     curr_plan.extend(improved[3][(i//27)%(len(improved[3]))])

                    
                #     temp_ind=Individual(meal_plan)
                #     obj=temp_ind.calculate_objectives(penalty_wts,group_index)
                #     if best_val<sum(obj):
                #         best_val=sum(obj)
                #         best_ind=copy.deepcopy(temp_ind)
                improved_ind=Individual(improved_plan)
                improved_ind.calculate_objectives(penalty_wts,group_index)
                if self.plan_utils.isValidChild(improved_plan):
                    improved_ind.feasiblity=True
                    updated_children["feasible"].append(improved_ind)
                else:
                    improved_ind.feasiblity=False
                    updated_children["infeasible"].append(improved_ind)
            else:
                updated_children["infeasible"].append(child)
        
        return updated_children
    
    def improve_meal(self,dishes:"list[Dish]",which_meal:str,group_index:int=0)->"list[Dish]":
        """
        Improve a set of dishes corresponding to one meal 
        """
        non_padding_dishes=[dish for dish in dishes if dish.id!=0]
        if len(non_padding_dishes)==1: 
            return dishes
        
        random_dish=random.choice(non_padding_dishes)

        if len(self.problem_config.groups[group_index].positive_preferences)!=0:
            choices=[1,2,3]
        else:
            choices=[1,2]

        choice=random.choice(choices)

        if choice==1:
            ## Improve combination
            other_avg=[]
            for dish in dishes:
                if dish.id!=random_dish.id and dish.id!=0:
                    other_avg.append(self.dataset.get_combi_vector(dish))
            if len(other_avg)==0:
                print(non_padding_dishes,dishes)
                return dishes
            other_avg=np.mean(other_avg)
            combi_dish_id=int(self.dataset.get_combi_similar(other_avg))
            combi_dish=Dish(
                id=combi_dish_id,
                quantity=random_dish.quantity,
                vector=self.dataset.get_dish_vector(combi_dish_id),
                title=self.dataset.get_dish_title(combi_dish_id),
                meal=which_meal,
                cuisine=self.dataset.get_dish_cuisine(combi_dish_id),
                category=self.dataset.get_dish_category(combi_dish_id),
                tags=self.dataset.get_dish_tags(combi_dish_id)
            )
            
            improved_combi=[combi_dish]
            for dish in dishes:
                if dish.id!=random_dish.id:
                    improved_combi.append(dish)
            return improved_combi
        elif choice==2:
            ## Improve diversity
            other_avg=[]
            for dish in dishes:
                if dish.id!=random_dish.id and dish.id!=0:
                    other_avg.append(dish.vector[1:-1])
            if len(other_avg)==0:
                return dishes
            other_avg=np.mean(other_avg)
            other_dishes=self.dataset.sample_dishes(count=5)
            best_id=np.argmax([np.linalg.norm(other_avg-self.dataset.get_dish_vector(id)) for id in other_dishes])
            div_dish_id=other_dishes[best_id]
            div_dish=Dish(
                id=div_dish_id,
                quantity=random_dish.quantity,
                vector=self.dataset.get_dish_vector(div_dish_id),
                title=self.dataset.get_dish_title(div_dish_id),
                meal=which_meal,
                cuisine=self.dataset.get_dish_cuisine(div_dish_id),
                category=self.dataset.get_dish_category(div_dish_id),
                tags=self.dataset.get_dish_tags(div_dish_id)
            )
            improved_div=[div_dish]
            for dish in dishes:
                if dish.id!=random_dish.id:
                    improved_div.append(dish)
            return improved_div
        elif choice==3:
            ## Improve preference
            pref_dish_id=self.dataset.get_preferred(self.problem_config.groups[group_index].positive_preferences)
            pref_dish=Dish(
                id=pref_dish_id,
                quantity=random_dish.quantity,
                vector=self.dataset.get_dish_vector(pref_dish_id),
                title=self.dataset.get_dish_title(pref_dish_id),
                meal=which_meal,
                cuisine=self.dataset.get_dish_cuisine(pref_dish_id),
                category=self.dataset.get_dish_category(pref_dish_id),
                tags=self.dataset.get_dish_tags(pref_dish_id)
            )
            improved_pref=[pref_dish]
            for dish in dishes:
                if dish.id!=random_dish.id:
                    improved_pref.append(dish)
            return improved_pref


    
    @staticmethod
    def intersection(l1:list,l2:list)->int:
        cnt=0
        for val in l1:
            if val in l2:
                cnt+=1
        return cnt
    
    @staticmethod
    def get_edit_distance(ind1:Individual, ind2:Individual)->int:
        ## Number of dishes that need to be changed to convert one meal plan to another
        ## Need to change the un-common dishes
        dish_ids_1=[ dish.id for dish in ind1.meal_plan.plan for _ in range(dish.quantity)]
        dish_ids_2=[ dish.id for dish in ind2.meal_plan.plan for _ in range(dish.quantity)]

        common=HybridGAUtils.intersection(dish_ids_1,dish_ids_2)
        
        return (len(dish_ids_1)-common)

    def find_diversity_ranks_for_pop(self,population:HybridGAPopulation)->None:
        N_CLOSEST=5
        diversity_scores=[]
        for id1,ind1 in enumerate(population):
            least_n=[1000]*N_CLOSEST
            for id2,ind2 in enumerate(population):
                if id2==id1:
                    continue
                
                dist=HybridGAUtils.get_edit_distance(ind1,ind2)
                
                ## Insert at appropriate location in the least n list
                inserted_flag=0
                for i in range(N_CLOSEST-1,0,-1):
                    if least_n[i]==dist:
                        least_n.insert(i,dist)
                        least_n.pop()
                        inserted_flag=1
                        break
                    elif least_n[i]<dist:
                        if i+1<N_CLOSEST:
                            least_n.insert(i+1,dist)
                            least_n.pop()
                            inserted_flag=1
                            break
                    else: ## least_n[i]>dist
                        continue
                if inserted_flag==0: ## it is the smallest
                    least_n.insert(0,dist)
                    least_n.pop()

            diversity_scores.append(sum(least_n)/N_CLOSEST)
        
        diversity_scores=np.array(diversity_scores)
        diversity_ranks=HybridGAUtils.get_rank_array(diversity_scores,type="desc")

        HybridGAUtils.normalise_rank_array(diversity_ranks)

        return diversity_ranks

    def find_obj_ranks_for_pop(self,population:"list[Individual]"):
        ## Fast Non Dominated Sorting
        fronts = [[]]
        cnt=0
        for individual in population:
            # print("Current Ind Obj",individual.objectives)
            individual.domination_count = 0
            individual.dominated_solutions = []
            for other_individual in population: 
                if(individual.ids==other_individual.ids):
                    # same
                    continue
                if individual.dominates(other_individual):
                    # current dominates
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    # other dominates
                    individual.domination_count += 1
                # else:
                    # neither dominates
            if individual.domination_count == 0:
                individual.rank = 0
                cnt+=1
                fronts[0].append(individual)

        i = 0
        count = 0
        while len(fronts[i]) > 0:
            temp = []
            for individual in fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i+1
                        count = count + 1
                        temp.append(other_individual)
            i = i+1
            fronts.append(temp)

        ranks=[]
        for ind in population:
            ranks.append(ind.rank)

        HybridGAUtils.normalise_rank_array(ranks)
        
        return ranks

    @staticmethod
    def normalise_rank_array(arr):
        """
        Inplace normalisation of rank array: Divide by maximum
        """
        maxV=max(arr)
        # if maxV==0:
        #     return
        for i in range(len(arr)):
            arr[i]=arr[i]/maxV
        

    def get_biased_fitness_values(self,population:HybridGAPopulation):
        ## Diversity ranks are calculated for the complete population 
        ## But the objective ranks are calculated separately
        ## in order to ensure, that the elite solutions survive
        div_ranks=self.find_diversity_ranks_for_pop(population)
        obj_ranks_feasible=self.find_obj_ranks_for_pop(population["feasible"])
        obj_ranks_infeasible=self.find_obj_ranks_for_pop(population["infeasible"])

        curr_id=0
        for id,ind in enumerate(population["feasible"]):
            ind.biased_fitness=obj_ranks_feasible[id]+(1-self.problem_config.HybridGA.number_elite/self.problem_config.HybridGA.population_size)*div_ranks[curr_id]
            curr_id+=1

        for id,ind in enumerate(population["infeasible"]):
            ind.biased_fitness=obj_ranks_infeasible[id]+(1-self.problem_config.HybridGA.number_elite/self.problem_config.HybridGA.population_size)*div_ranks[curr_id]
            curr_id+=1
        
    @staticmethod
    def get_rank_array(arr,type="asc"):
        """
        This helper function returns an array indicating the rank of the value at each position
        Args:
            arr: NumpyArray
            type: asc or desc
        """

        length_array = len(arr)
        if type == "asc":
            sort_key = arr.argsort()
        else:
            sort_key = (-arr).argsort()

        rank_array = [True] * length_array
        for i in range(length_array):
            # get the position of the value in the original array that is at rank i
            val_pos = sort_key[i]
            # set the rank i at position val_pos
            rank_array[val_pos] = i

        return rank_array
    
    def create_children(self,population,penalty_wts,limit:int,group_index:int=0)->"dict[str,list[Individual]]":
        children={
            "feasible":[],
            "infeasible":[]
        }

        while len(children["feasible"])+len(children["infeasible"])<limit:
            parent1=self.tournament(population)
            parent2=parent1
            # print(parent1==parent2)
            try:
                while parent1==parent2:
                    parent2=self.tournament(population)
            except Exception as e:
                print(e)
                print(len(parent1.features),len(parent2.features))
                continue
            
            child = self.crossover(parent1,parent2)

            child=self.mutate(child,group_index)

            if not child.meal_plan.check_no_repeat():
                continue

            if(self.plan_utils.isValidChild(child.meal_plan,group_index)):
                child.calculate_objectives(penalty_wts,group_index)
                child.feasiblity=True
                children["feasible"].append(child)
            else:
                child.calculate_objectives(penalty_wts,group_index)
                child.feasiblity=False
                children["infeasible"].append(child)

        return children
    
    def mutate(self,ind:Individual,group_index=0)-> Individual:
        meal_plan=[]
        for id,dish in enumerate(ind.meal_plan.plan):
            if(PlanUtils.choose_with_prob(self.problem_config.HybridGA.mutation_parameter)):
                # dish_vec= np.array(deepcopy(dish.vector)[1:-1]).astype('float64')
                # ings=self.dataset.get_random_ingredients()
                # for ing in ings:
                #     # print(ing)
                #     if(PlanUtils.choose_with_prob(0.5)):
                #         dish_vec=np.add(ing*random.random(),dish_vec)
                #     else:
                #         dish_vec=np.subtract(ing*random.random(),dish_vec)
                # id,dish_vec=self.dataset.get_closest_dish(dish_vec)
                random_dish_id,random_dish_vec=self.dataset.get_random_dish(self.problem_config.get_meal_from_id(id))

                meal_plan.append(
                    Dish(
                        id=random_dish_id,
                        quantity=self.plan_utils.get_random_quantity(group_index),
                        vector=random_dish_vec,
                        title=self.dataset.get_dish_title(random_dish_id),
                        meal=self.problem_config.get_meal_from_id(len(meal_plan)),
                        cuisine=self.dataset.get_dish_cuisine(random_dish_id),
                        category=self.dataset.get_dish_category(random_dish_id),
                        tags=self.dataset.get_dish_tags(random_dish_id)
                    )
                )
            else:
                meal_plan.append(dish)

        return Individual(MealPlan(self.problem_config,self.dataset,meal_plan))
    
    
    def survivor_selection(self,population:HybridGAPopulation,limit:int)->HybridGAPopulation:
        ## Remove the weakest individuals based on biased fitness function
        # biased_fitness=[ind.biased_fitness for ind in population]
        # ## Are ranks so select lowest values
        # best_n_indices=sorted(range(len(biased_fitness)),key=lambda x: biased_fitness[x])[:limit]

        # new_pop=HybridGAPopulation()
        # for id,ind in enumerate(population):
        #     if id in best_n_indices:
        #         if ind.feasiblity:
        #             new_pop["feasible"].append(ind)
        #         else:
        #             new_pop["infeasible"].append(ind)

        ## Fast Non Dominated Sorting and crowding distance based survivor selection
        fronts=self.calculate_rank_and_crowding(population)

        new_population=HybridGAPopulation()
        front_num=0
        while len(new_population) + len(fronts[front_num]) <= limit:
            new_population.extend_list(fronts[front_num])
            front_num += 1

        fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
        new_population.extend_list(fronts[front_num][0:self.problem_config.HybridGA.population_size-len(new_population)])
            
        return new_population
    
    def calculate_rank_and_crowding(self,population:HybridGAPopulation)->"list[list[Individual]]":
        fronts = [[]]
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
                fronts[0].append(individual)
        # print("Count",cnt)
        i = 0
        count = 0
        while len(fronts[i]) > 0:
            temp = []
            for individual in fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i+1
                        count = count + 1
                        temp.append(other_individual)
            i = i+1
            fronts.append(temp)

        for front in fronts:
            self.calculate_crowding_distance(front)

        return fronts
    
    def calculate_crowding_distance(self, front:"list[Individual]") -> None:
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

        

    def get_pareto_front(self, population:HybridGAPopulation )-> "list[Individual]":
        pareto_front = []
        for individual in population["feasible"]:
            individual.calculate_objectives()

            individual.domination_count = 0
            for other_individual in population["feasible"]: 
                if(individual.ids==other_individual.ids):
                    # same
                    continue
                if individual.dominates(other_individual):
                    # current dominates
                    continue
                elif other_individual.dominates(individual):
                    # other dominates
                    individual.domination_count += 1
                # else:
                    # neither dominates

            if individual.domination_count == 0:
                individual.rank = 0
                pareto_front.append(individual)

        return pareto_front
    
    def crossover(self,ind1: Individual,ind2: Individual) -> Individual:
        meal_plan_child=[]
        ## As suggested by the paper, avoiding a priori determined rules on how
        ## much genetic material the offspring inherits from each parent
        percent_genetic_material_from1=random.random() 

        for i in range(len(ind1.meal_plan.plan)):
            if(PlanUtils.choose_with_prob(percent_genetic_material_from1)):
                meal_plan_child.append(ind1.meal_plan.plan[i])
            else:
                meal_plan_child.append(ind2.meal_plan.plan[i])
        
        return Individual(MealPlan(self.problem_config,self.dataset,meal_plan_child))

