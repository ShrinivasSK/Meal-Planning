## Putting it all together

from plan import Dish, Dataset, MealPlan, ProblemConfig, Individual
import NSGA as nsg
import HybridGA as hbd

from sklearn.cluster import KMeans
from scipy.spatial import KDTree
import numpy as np
import random
from collections import defaultdict
import copy

## TODO: Model Nutrition as a soft constraint
class MealPlanner:
    
    @staticmethod
    def plan(config:dict,logger) -> "list[Individual]":
        
        logger.info("Initialising Variables.....")
        
        dataset=Dataset()
        problem_config=ProblemConfig(**config)
        problem_config.init_other(dataset)
        
        if problem_config.planning.ga=="hybrid":
            evolution=hbd.Evolution(dataset,problem_config)
        else:
            evolution=nsg.Evolution(dataset,problem_config)

        logger.info("Running")
        
        pareto_front=evolution.evolve()

        logger.info("NSGA Complete")
        logger.info("Front Size: "+ str(len(pareto_front)))

        logger.info("Objective Values History: ")
        logger.info(evolution.history_objectives)

        res_objectives=[] 
        for individual in pareto_front:
            res_objectives.append(individual.objectives)

        final_pop=MealPlanner.post_process(pareto_front,res_objectives)
        
        logger.info("Meal Plan Generated: ")
        for individual in final_pop:
            logger.info(str(individual)+"\n")

        return final_pop
    
    @staticmethod
    def post_process(population:"list[Individual]",objectives:"list[float]"):
        obj_to_index={}

        X=[]
        for id,obj in enumerate(objectives):
            X.append([obj[0],obj[1]])

        X=np.array(X)
        
        kdTree=KDTree(X)

        kmeans=KMeans(n_clusters=5,init='k-means++',random_state=42).fit(X)

        representatives=[]
        for center in kmeans.cluster_centers_:
            _,id=kdTree.query(center)
            representatives.append(population[id])

        return representatives


    @staticmethod
    def get_difference_dish(d1:Dish,d2:Dish)->float:
        return np.linalg.norm(d1.vector[1:-1]-d2.vector[1:-1])
    
    @staticmethod
    def difference_between_meal_plans(m1: MealPlan,m2:MealPlan, problem_config: ProblemConfig)->float:
        diff=0
        for id in range(len(m1.plan)):
            if problem_config.get_meal_from_id(id)=='Breakfast':
                diff+=abs(MealPlanner.get_difference_dish(m1.plan[id],m2.plan[id])/problem_config.meal.breakfast_dishes)
            elif problem_config.get_meal_from_id(id)=='Lunch':
                diff+=abs(MealPlanner.get_difference_dish(m1.plan[id],m2.plan[id])/problem_config.meal.lunch_dishes)
            elif problem_config.get_meal_from_id(id)=='Snacks':
                diff+=abs(MealPlanner.get_difference_dish(m1.plan[id],m2.plan[id])/problem_config.meal.snacks_dishes)
            elif problem_config.get_meal_from_id(id)=='Dinner':
                diff+=abs(MealPlanner.get_difference_dish(m1.plan[id],m2.plan[id])/problem_config.meal.dinner_dishes)
        return diff
    
    
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
                        MealPlanner.difference_between_meal_plans(
                            plan1.meal_plan,plan2.meal_plan,config),
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

        matched_reps=list(map(lambda l:[l],group_reps[0]))
        for suggestion_id in range(config.planning.num_suggestions):
            for group_id in range(config.planning.group_count-1):
                matched_reps[suggestion_id].append(group_reps[group_id+1][matchings[group_id][suggestion_id]])
        
        return matched_reps ## NUM_SUGGESTIONS X NUM_GROUPS
    
    @staticmethod
    def merge_dishes(dishes:list[Dish],limit,problem_config,dataset,ratio,brute_force=False)->"list[Dish]":
        ## Choose half the dishes from breakfast, lunch, dinner, snacks
        ## TODO: apply a distance threshold
        ## TODO: add logic to select one of the dishes (here preference to first 1 arbitrarily)
        if not brute_force:
            distances=[]
            for id1,dish1 in enumerate(dishes):
                for id2,dish2 in enumerate(dishes):
                    if id1<id2:
                        distances.append(
                        [
                            MealPlanner.get_difference_dish(dish1,dish2),
                            (id1,id2)
                        ])
            distances=sorted(distances)

            removed=defaultdict(lambda: False)
            num_dishes=len(dishes)
            cur_id=0
            while num_dishes>(len(dishes))//1.5 and cur_id<len(distances):
                dish_id1=distances[cur_id][1][0]
                dish_id2=distances[cur_id][1][1]
                if removed[dish_id1] or removed[dish_id2]:
                    cur_id+=1
                    continue ## Take the other dish, i.e do not remove anything
                else:
                    if random.random()<=0.5: ## remove one randomly for now
                        removed[dish_id1]=True   
                        dishes[dish_id2].quantity+=dishes[dish_id1].quantity
                    else:
                        removed[dish_id2]=True
                        dishes[dish_id1].quantity+=dishes[dish_id2].quantity
                    cur_id+=1
                    num_dishes-=1

            merged_dishes=[]
            for id,dish in enumerate(dishes):
                if not removed[id]:
                    merged_dishes.append(dish)

            return merged_dishes
        else:
            nutri_req=np.array(problem_config.groups[0].daily_nutrient_requirements)*ratio
            wt_req=np.array(problem_config.groups[0].daily_weight_requirements)*ratio
            for group in problem_config.groups[1:]:
                wt_req+=np.array(group.daily_weight_requirements)*ratio
                nutri_req+=np.array(group.daily_nutrient_requirements)*ratio
            num_dishes=len(dishes)
            total_subsets=2**num_dishes
            best_subset=[]
            best_optim=[0]*4
            tot_quantity=0
            for dish in dishes:
                tot_quantity+=dish.quantity
            for i in range(total_subsets):
                temp_q=tot_quantity
                meal=[]
                for j in range(num_dishes):
                    temp=i
                    if j!=0:
                        temp=i>>(j-1)
                    if ((temp & 1)):
                        meal.append(copy.deepcopy(dishes[j]))
                        temp_q-=dishes[j].quantity
                
                if len(meal)<2 or len(meal)>limit:
                    continue
                ## maintain food quantity
                while temp_q>0:
                    for dish in meal:
                        dish.quantity+=1
                        temp_q-=1
                        if temp_q<=0:
                            break

                meal_plan=MealPlan(problem_config,dataset,meal)
                
                # if not MealPlanner.isValid(meal_plan,nutri_req,wt_req):
                #     # print(len(meal))
                #     continue
                optim=[
                    meal_plan.get_pos_preference(),
                    -1*meal_plan.get_neg_preference(),
                    meal_plan.get_combi_value(),
                    meal_plan.get_diversity(),
                ]
                if MealPlanner.is_better(optim,best_optim,len(meal),len(best_subset)):
                    best_optim=optim
                    best_subset=meal
            
            return best_subset
        
    @staticmethod
    def checkIfSatisfied(vals,limits) -> bool:
        for i in range(len(vals)):
            if not (limits[i][0]<=vals[i]):
                return False
        return True
    
    @staticmethod
    def isValid(meal_plan:MealPlan,nutri_req,wt_req)->bool:
        wt=meal_plan.calculate_wt()
        nutri=meal_plan.calculate_nutri()
        dishes=set()
        for dish in meal_plan.plan:
            dishes.add(dish.id)
        t=[
            MealPlanner.checkIfSatisfied([nutri[0][0]],nutri_req),
            MealPlanner.checkIfSatisfied([wt[0][0]],wt_req),
            # len(dishes)==len(meal_plan.plan), ## no repeat
        ]
        # print(t)
        return all(t)
        
    @staticmethod
    def is_better(val1:"list[float]",val2:"list[float]",l1:int,l2:int)->bool:
        if val1[1]==0 and val2[1]!=0:
            return True
        if val2[1]==0 and val1[1]!=0:
            return False
        if val1==val2:
            return l1<=l2
        return val1>=val2
        

    @staticmethod
    def merge_group_plans(group_reps:list[Individual],config:ProblemConfig,dataset:Dataset)->Individual:
        dishes_breakfast=[]
        dishes_lunch=[]
        dishes_snacks=[]
        dishes_dinner=[]

        for ind in group_reps:
            for meal_id in range(len(ind.meal_plan.plan)):
                dish=ind.meal_plan.plan[meal_id]
                if dish.id==0:
                    continue
                if dish.meal=='Breakfast':
                    dishes_breakfast.append(dish)
                elif dish.meal=='Lunch':
                    dishes_lunch.append(dish)
                elif dish.meal=='Snacks':
                    dishes_snacks.append(dish)
                else:
                    dishes_dinner.append(dish)

        suggested_meal_plan=[]

        merged_breakfast=MealPlanner.merge_dishes(dishes_breakfast,
                        (config.meal.breakfast_dishes*config.planning.group_count)/1.5,
                        config,dataset,0.15,brute_force=True)
        config.meal.breakfast_dishes=len(merged_breakfast)
        suggested_meal_plan.extend(merged_breakfast) 
        
        merged_lunch=MealPlanner.merge_dishes(dishes_lunch,
                        (config.meal.lunch_dishes*config.planning.group_count)/1.5,
                        config,dataset,0.3,brute_force=True)
        config.meal.lunch_dishes=len(merged_lunch)
        suggested_meal_plan.extend(merged_lunch) 

        merged_snacks=MealPlanner.merge_dishes(dishes_snacks,
                        (config.meal.snacks_dishes*config.planning.group_count),
                        config,dataset,0.15,brute_force=True)
        config.meal.snacks_dishes=len(merged_snacks)
        suggested_meal_plan.extend(merged_snacks) 

        merged_dinner=MealPlanner.merge_dishes(dishes_dinner,
                        (config.meal.dinner_dishes*config.planning.group_count)/1.5,
                        config,dataset,0.2,brute_force=True)
        config.meal.dinner_dishes=len(merged_dinner)
        suggested_meal_plan.extend(merged_dinner) 

        return Individual(MealPlan(config,dataset,suggested_meal_plan))

    @staticmethod
    def plan_multiple(config: dict,logger):
        logger.info("Initialising Variables.....")
        
        dataset=Dataset()

        problem_config=ProblemConfig(**config)
        problem_config.init_other(dataset)

        if problem_config.planning.ga=="hybrid":
            evolution=hbd.Evolution(dataset,problem_config)
        else:
            evolution=nsg.Evolution(dataset,problem_config)

        logger.info("Running")
        group_reps=[]
        for group_index in range(problem_config.planning.group_count):
            logger.info(f"Group Index {group_index}")
            evolution.history_objectives=[]
            pareto_front=evolution.evolve(group_index)

            logger.info("NSGA Complete")
            logger.info("Front Size: "+ str(len(pareto_front)))

            res_objectives=[] 
            for individual in pareto_front:
                res_objectives.append(individual.objectives)

            logger.info("Objective Values of Pareto Front: ")
            logger.info(str(res_objectives))

            group_rep=MealPlanner.post_process(pareto_front)
            group_reps.append(group_rep)

        logger.info("Group Plans Ready")
        logger.info("Matching Group Plans")
        matched_reps=MealPlanner.match_group_plans(group_reps,problem_config)

        logger.info("Meal Plan Generated: ")
        final_pop=[]
        for matched_rep in matched_reps:
            suggested=MealPlanner.merge_group_plans(matched_rep,problem_config,dataset)
            logger.info(str(suggested)+"\n")
            final_pop.append(suggested)

        return final_pop

        


    
