## Utility Functions for NSGA

from NSGA.population import NSGAPopulation
from plan import MealPlan, Individual, ProblemConfig, Dataset, Dish, PlanUtils
from typing import Tuple
import random

class NSGAUtils:

    def __init__(self,dataset:Dataset,problem_config:ProblemConfig) -> None:
        self.problem_config=problem_config
        self.dataset=dataset
        self.plan_utils=PlanUtils(dataset,problem_config)
        random.seed()

    def create_initial_population_many(self) -> NSGAPopulation:
        breakfast_options=self.plan_utils.get_cliques(self.dataset,"breakfast",lower_limit=1,higher_limit=3)
        lunch_options=self.plan_utils.get_cliques(self.dataset,"lunch",lower_limit=1,higher_limit=5)
        snacks_options=self.plan_utils.get_cliques(self.dataset,"snacks",lower_limit=1,higher_limit=3)
        dinner_options=self.plan_utils.get_cliques(self.dataset,"dinner",lower_limit=1,higher_limit=5)

        population=NSGAPopulation()

        while (len(population)<self.problem_config.NSGA.population_size):
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
            
            ## Check Validity
            if(self.plan_utils.isValidChild(meal_plan)):
                population.append(
                    Individual(
                        meal_plan=meal_plan
                        )
                    )
        
        return population
            

    def create_intitial_population(self,group_index=0) -> NSGAPopulation:
        breakfast_options=self.plan_utils.get_cliques(self.dataset,"breakfast",lower_limit=1,higher_limit=3)
        lunch_options=self.plan_utils.get_cliques(self.dataset,"lunch",lower_limit=3,higher_limit=5)
        snacks_options=self.plan_utils.get_cliques(self.dataset,"snacks",lower_limit=1,higher_limit=3)
        dinner_options=self.plan_utils.get_cliques(self.dataset,"dinner",lower_limit=3,higher_limit=5)

        population=NSGAPopulation()

        while (len(population)<self.problem_config.NSGA.population_size):
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
            
            ## Check Validity
            if(self.plan_utils.isValidChild(meal_plan,group_index)):
                # print(meal_plan.plan)
                population.append(
                    Individual(
                        meal_plan=meal_plan
                        )
                    )

        return population
    
    

    def fast_nondominated_sort(self, population:NSGAPopulation ) -> None:
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

    def crossover(self,ind1: Individual,ind2: Individual) -> Tuple[Individual,Individual]:
        meal_plan_child1=[]
        meal_plan_child2=[]
        for i in range(len(ind1.meal_plan.plan)):
            if(PlanUtils.choose_with_prob(0.5)):
                meal_plan_child1.append(ind1.meal_plan.plan[i])
                meal_plan_child2.append(ind2.meal_plan.plan[i])
            else:
                meal_plan_child1.append(ind2.meal_plan.plan[i])
                meal_plan_child2.append(ind1.meal_plan.plan[i])
        
        return [
            Individual(MealPlan(self.problem_config,self.dataset,meal_plan_child1)),
            Individual(MealPlan(self.problem_config,self.dataset,meal_plan_child2))
        ]

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

    def crowding_operator(self, individual: Individual, other_individual: Individual) -> int:
        if (individual.rank < other_individual.rank) or \
            ((individual.rank == other_individual.rank) and (individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1
        
    def tournament(self, population):
        participants = random.sample(population.population, self.problem_config.NSGA.number_of_tournament_participants)
        best = None
        for participant in participants:
            if best is None or (self.crowding_operator(participant, best) == 1 and PlanUtils.choose_with_prob(self.problem_config.NSGA.tournament_probability)):
                best = participant

        return best
    
    def mutate(self,ind:Individual,group_index=0)-> Individual:
        meal_plan=[]
        for id,dish in enumerate(ind.meal_plan.plan):
            if(PlanUtils.choose_with_prob(self.problem_config.NSGA.mutation_parameter)):
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
                        quantity=self.get_random_quantity(group_index),
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


    def create_children(self,population:NSGAPopulation,group_index:int=0)-> "list[Individual]":
        ## May lead to infinite loop if enough children are never valid
        children=[]

        while len(children)<len(population):
            parent1=self.tournament(population)
            parent2=parent1
            # print(parent1==parent2)
            while parent1==parent2:
                parent2=self.tournament(population)
            
            child1, child2 = self.crossover(parent1,parent2)

            child1=self.mutate(child1,group_index)
            child2=self.mutate(child2,group_index)

            if(self.plan_utils.isValidChild(child1.meal_plan,group_index)):
                child1.calculate_objectives(group_index)
                children.append(child1)

            if(self.plan_utils.isValidChild(child2.meal_plan,group_index)):
                child2.calculate_objectives(group_index)
                children.append(child2)

        return children

