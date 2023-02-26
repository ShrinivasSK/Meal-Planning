## Putting it all together

from NSGA import Dish, Individual, MealPlan, ProblemConfig, Dataset, Evolution

from sklearn_extra.cluster import KMedoids
import numpy as np

class NSGAMealPlanner:
    
    @staticmethod
    def plan(config:dict):
        
        print("Initialising Variables.....")
        
        problem_config=ProblemConfig(**config)
        problem_config.init_other()

        dataset=Dataset()
        evolution=Evolution(dataset,problem_config)

        print("Running")
        
        final_population=evolution.evolve()

        print("Meal Plan Generated: ")
        print("Front Size: ", len(final_population))

        final_reps=NSGAMealPlanner.cluster_front(final_population,problem_config)
        for individual in final_reps:
            print(individual)
            print()
        
        print("Objective Values History: ")
        print(evolution.history_objectives)

    @staticmethod
    def get_difference_dish(d1:Dish,d2:Dish)->float:
        return np.mean(d1.vector[1:-1]-d2[1:-1])
    
    @staticmethod
    def difference_between_meal_plans(m1: MealPlan,m2:MealPlan, problem_config: ProblemConfig)->float:
        diff=0
        for id in range(len(m1.plan)):
            if problem_config.get_meal_from_id(id)=='Breakfast':
                diff+=NSGAMealPlanner.get_difference_dish(m1.plan[id],m2.plan[id])/problem_config.meal.breakfast_dishes
            elif problem_config.get_meal_from_id(id)=='Lunch':
                diff+=NSGAMealPlanner.get_difference_dish(m1.plan[id],m2.plan[id])/problem_config.meal.lunch_dishes
            elif problem_config.get_meal_from_id(id)=='Snacks':
                diff+=NSGAMealPlanner.get_difference_dish(m1.plan[id],m2.plan[id])/problem_config.meal.snacks_dishes
            elif problem_config.get_meal_from_id(id)=='Dinner':
                diff+=NSGAMealPlanner.get_difference_dish(m1.plan[id],m2.plan[id])/problem_config.meal.dinner_dishes
        return diff
    
    @staticmethod
    def cluster_front(front: list[Individual],config: ProblemConfig) -> list[Individual]:
        x=[]
        for ind in front:
            x.append(ind.objectives)
        x=np.array(x)

        representatives=KMedoids(n_clusters=config.planning.num_suggestions).fit(x).medoid_indices_

        final_suggestions=[]
        for rep in representatives:
            final_suggestions.append(rep)

        return final_suggestions
    
    @staticmethod
    def match_group_plans(group_reps:list[list[Individual]], config: ProblemConfig)->list[list[Individual]]:
        # INPUT: NUM_GROUPS x NUM_SUGGESTIONS
        matchings=[]
        for id in range(1,len(group_reps)):
            distances=[]
            for id1,plan1 in enumerate(group_reps[id]):
                for id2,plan2 in enumerate(group_reps[id-1]):
                    distances.append(
                        [ 
                        NSGAMealPlanner.difference_between_meal_plans(
                            plan1.meal_plan,plan2.meal_plan),
                        (id1,id2)
                        ]
                    )
            
            distances=sorted(distances)
            matching={}
            for distance in distances:
                if distance[1][0] not in matching and distance[1][1] not in matching:
                    matching[distance[1][0]]=distance[1][1]
                    matching[distance[1][1]]=distance[1][0]

            matchings.append(matching)

        matched_reps=group_reps[0]
        for suggestion_id in range(config.planning.num_suggestions):
            for group_id in range(config.planning.group_count-1):
                matched_reps[suggestion_id].append(group_reps[group_id+1][matchings[group_id][suggestion_id]])
        
        return matched_reps ## NUM_SUGGESTIONS X NUM_GROUPS

    @staticmethod
    def merge_group_plans(group_reps:list[Individual],config:ProblemConfig,dataset:Dataset)->Individual:
        distance_breakfast=[]
        distance_lunch=[]
        distance_snacks=[]
        distance_dinner=[]
        for id1,ind1 in enumerate(group_reps):
            for id2,ind2 in enumerate(group_reps):
                if id1<id2:
                    for meal_id in range(len(ind1.meal_plan.plan)):
                        if config.get_meal_from_id(meal_id)=='Breakfast':
                            distance_breakfast.append(
                                [
                                    NSGAMealPlanner.get_difference_dish(ind1.meal_plan.plan[meal_id],ind2.meal_plan.plan[meal_id])
                                    (id1,id2,meal_id)
                                ])
                        if config.get_meal_from_id(meal_id)=='Lunch':
                            distance_lunch.append(
                                [
                                    NSGAMealPlanner.get_difference_dish(ind1.meal_plan.plan[meal_id],ind2.meal_plan.plan[meal_id])
                                    (id1,id2,meal_id)
                                ])
                        if config.get_meal_from_id(meal_id)=='Snacks':
                            distance_snacks.append(
                                [
                                    NSGAMealPlanner.get_difference_dish(ind1.meal_plan.plan[meal_id],ind2.meal_plan.plan[meal_id])
                                    (id1,id2,meal_id)
                                ])
                        if config.get_meal_from_id(meal_id)=='Dinner':
                            distance_dinner.append(
                                [
                                    NSGAMealPlanner.get_difference_dish(ind1.meal_plan.plan[meal_id],ind2.meal_plan.plan[meal_id])
                                    (id1,id2,meal_id)
                                ])
                            
        ## Choose half the dishes from breakfast, lunch, dinner, snacks
        ## TODO: apply a distance threshold
        ## TODO: add logic to select one of the dishes (here preference to first 1 arbitrarily)
        distance_breakfast=sorted(distance_breakfast)
        taken={}
        removed={}
        suggested_meal_plan=[]
        num_breakfast=0
        for id in range(len(distance_breakfast)/2):
            if not taken[distance_breakfast[id][0]] and not removed[distance_breakfast[id][0]]:
                suggested_meal_plan.append(group_reps[distance_breakfast[id][0]].meal_plan.plan[distance_breakfast[id][2]])
                taken[distance_breakfast[id][0]]=1
                num_breakfast+=1
                removed[distance_breakfast[id][1]]=1
            elif not taken[distance_breakfast[id][1]] and not removed[distance_breakfast[id][1]] :
                suggested_meal_plan.append(group_reps[distance_breakfast[id][1]].meal_plan.plan[distance_breakfast[id][2]])
                taken[distance_breakfast[id][1]]=1
                num_breakfast+=1
                removed[distance_breakfast[id][0]]=1
        config.meal.breakfast_dishes=num_breakfast

        distance_lunch=sorted(distance_lunch)
        taken={}
        removed={}
        num_lunch=0
        for id in range(len(distance_lunch)/2):
            if not taken[distance_lunch[id][0]] and not removed[distance_lunch[id][0]]:
                suggested_meal_plan.append(group_reps[distance_lunch[id][0]].meal_plan.plan[distance_lunch[id][2]])
                taken[distance_lunch[id][0]]=1
                num_lunch+=1
                removed[distance_lunch[id][1]]=1
            elif not taken[distance_lunch[id][1]] and not removed[distance_lunch[id][1]] :
                suggested_meal_plan.append(group_reps[distance_lunch[id][1]].meal_plan.plan[distance_lunch[id][2]])
                taken[distance_lunch[id][1]]=1
                num_lunch+=1
                removed[distance_lunch[id][0]]=1
        config.meal.lunch_dishes=num_lunch

        distance_snacks=sorted(distance_snacks)
        taken={}
        removed={}
        num_snacks=0
        for id in range(len(distance_snacks)/2):
            if not taken[distance_snacks[id][0]] and not removed[distance_snacks[id][0]]:
                suggested_meal_plan.append(group_reps[distance_snacks[id][0]].meal_plan.plan[distance_snacks[id][2]])
                taken[distance_snacks[id][0]]=1
                num_snacks+=1
                removed[distance_snacks[id][1]]=1
            elif not taken[distance_snacks[id][1]] and not removed[distance_snacks[id][1]] :
                suggested_meal_plan.append(group_reps[distance_snacks[id][1]].meal_plan.plan[distance_snacks[id][2]])
                taken[distance_snacks[id][1]]=1
                num_snacks+=1
                removed[distance_snacks[id][0]]=1
        config.meal.snacks_dishes=num_snacks

        distance_dinner=sorted(distance_dinner)
        taken={}
        removed={}
        suggested_meal_plan=[]
        num_dinner=0
        for id in range(len(distance_dinner)/2):
            if not taken[distance_dinner[id][0]] and not removed[distance_dinner[id][0]]:
                suggested_meal_plan.append(group_reps[distance_dinner[id][0]].meal_plan.plan[distance_dinner[id][2]])
                taken[distance_dinner[id][0]]=1
                num_dinner+=1
                removed[distance_dinner[id][1]]=1
            elif not taken[distance_dinner[id][1]] and not removed[distance_dinner[id][1]] :
                suggested_meal_plan.append(group_reps[distance_dinner[id][1]].meal_plan.plan[distance_dinner[id][2]])
                taken[distance_dinner[id][1]]=1
                num_dinner+=1
                removed[distance_dinner[id][0]]=1
        config.meal.dinner_dishes=num_dinner
        

        suggested_meal_plan=MealPlan(config,dataset,suggested_meal_plan)
        return Individual(suggested_meal_plan)

    @staticmethod
    def plan_multiple(config: dict):
        print("Initialising Variables.....")
        
        problem_config=ProblemConfig(**config)
        problem_config.init_other()

        dataset=Dataset()
        evolution=Evolution(dataset,problem_config)

        print("Running")
        group_reps=[]
        for group_index in range(problem_config.planning.group_count):
            final_population=evolution.evolve(group_index)

            group_rep=NSGAMealPlanner.cluster_front(final_population,problem_config)
            group_reps.append(group_rep)

        matched_reps=NSGAMealPlanner.match_group_plans(group_reps,problem_config)

        print("Suggested Combined Meal Plans")
        for matched_rep in matched_reps:
            suggested=NSGAMealPlanner.merge_group_plans(matched_rep,problem_config,dataset)
            print(suggested)
            print()

        


    
