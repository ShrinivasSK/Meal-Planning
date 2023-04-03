from plan import MealPlanner

import logging
import json
import time
import copy

NUM_OBJECTIVES=5

logging.basicConfig(filename='Outputs/output_testing_hybrid.log',
                    filemode='a',
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.WARNING)

logger=logging.getLogger()


def generate_preferences(all_subsets=False):
    ## Generate configs for different preference values
    ## Have various configs for standard constraints and varying pair of positive and negative 
    ## preferences that cover all cuisines
    ## Count of generated configs: All Subsets: False => 10, True => 20
    ## All Subsets flips the positive and negative preferences and generates new config

    configs=[]
    for i in range(10):
        file_name="./configs/preferences/config"+str(i+1)+".json"
        with open(file_name) as f:
            config=json.load(f)
        if all_subsets:
            config2=copy.deepcopy(config)
            config2["groups"][0]["positive_preferences"]=config["groups"][0]["negative_preferences"]
            config2["groups"][0]["negative_preferences"]=config["groups"][0]["positive_preferences"]
            configs.append(config2)
        configs.append(config)
    return configs


def generate_constraints(all_subsets=False):
    ## Generate configs for different constraint satisfaction values
    ## The config file name specifies which nutrition or weight constraint is higher than standard 
    ##           => lets call the config constraint config
    ## Count of generated configs: All Subsets: False => 5, True => 32
    ## All Subsets is the case when we generate all subsets from the 5 types of constraint configs

    configs=[]
    for constraint in ["calories","fats","proteins","carbohydrates","weights"]:
        file_name="./configs/constraints/config_"+constraint+".json"
        with open(file_name) as f:
            config=json.load(f)
        configs.append(config)
    if not all_subsets:
        return configs
    else:
        with open("./configs/config_standard.json") as f:
            standard_config=json.load(f)
        subset_configs=[]
        
        for i in range(32):
            config=copy.deepcopy(standard_config)
            for j in range(5):
                if ((i>>j) & 1): 
                    if j!=4:
                        config["groups"][0]["daily_nutrient_requirements"][j]=configs[j]["groups"][0]["daily_nutrient_requirements"][j]
                    else:
                        config["groups"][0]["daily_weight_requirements"]=configs[j]["groups"][0]["daily_weight_requirements"]
            subset_configs.append(config)
        
        return subset_configs
    

def generate_all_single():
    ## Generates configs for all types of one person: constraints and preferences
    ## Total configs generated is 5 x 10 = 50

    pref_subsets=generate_preferences()
    cons_subsets=generate_constraints()
    configs=[]
    for cons in cons_subsets:
        for pref in pref_subsets:
            cfg=copy.deepcopy(pref)
            cfg["groups"][0]["daily_nutrient_requirements"]=cons["groups"][0]["daily_nutrient_requirements"]
            cfg["groups"][0]["daily_weight_requirements"]=cons["groups"][0]["daily_weight_requirements"]
            configs.append(cfg)
    return configs

def generate_all_multiple(plan_type):
    ## Generates configs for different sizes of groups with individuals having varying constraints and preferences
    ## Total Configs generated: 10+10+10+5+5 = 40
    ## Can specify plan type to plan with a given type of algorithm
    ## Options: multiple (plan separate and combine), many_in_one (plan in one go)

    configs=[] 
    group_sizes={  ## group_size : num_groups_for_size
        2:10,
        3:10,
        5:10,
        7:5,
        10:5,
    }
    single_configs=generate_all_single()
    with open("./configs/config_standard.json") as f:
        standard_config=json.load(f)

    for size,cnt in group_sizes.items():
        for i in range(cnt):
            cfg=copy.deepcopy(standard_config)
            cfg["planning"]["plan_type"]=plan_type
            cfg["planning"]["group_count"]=size
            for id,j in enumerate(range(i,len(single_configs),cnt)):
                if id>=size:
                    break
                cfg["groups"].append(
                    single_configs[j]["groups"][0]
                )
                ## Group Size 3, Group Index 5 will have indices [5,15,25] of the single configs
                ## Group Size 3, Group Index 7 will have indices [7,17,27]
                ## Group Size 7, Group Index 3 will have indices [3,8,13,18,23,28,33]
                ## Group Size 10, Group Index 4 will have indices [4,9,14,19,24,29,34,39,44,49]
            configs.append(cfg)

    return configs

def run_config(config):
    logger.warning(f"Config:\n {config}")
    
    start=time.time()
    if config['planning']['plan_type']=='multiple':
        final_res=MealPlanner.plan_multiple(config,logger)
    else:
        final_res = MealPlanner.plan(config,logger)

    obj=[0.0]*NUM_OBJECTIVES
    for ind in final_res:
        temp=[obj[i]+ind.objectives[i] for i in range(len(ind.objectives))]
        dish_cnt=obj[4]
        for dish in ind.meal_plan.plan:
            if dish.id!=0:
                dish_cnt+=1
        temp.append(dish_cnt)
        obj=temp

    obj=[v/5 for v in obj]

    end=time.time()

    logger.warning(f"Time Required:\n{end-start}")
    logger.warning("Average Objectives:\n"+str(obj))

    return obj,end-start

def run_configs(title,configs):
    logger.error(f"Running {title}")
    avg_time=0
    avg_obj=[0.0]*NUM_OBJECTIVES
    objs=[]
    times=[]

    for cfg in configs:
        obj,time=run_config(cfg)

        avg_obj=[avg_obj[i]+obj[i] for i in range(len(obj))]
        avg_time+=time

        objs.append(obj)
        times.append(time)
    
    avg_obj=[val/len(configs) for val in avg_obj]
    avg_time/=len(configs)
    
    logger.error(f"{title}\nAvg Time:\n{str(avg_time)}\nAvg Objectives:\n {str(avg_obj)}")

    return objs,time

def get_values_for_separate(single_objs,single_times):
    ## Gets Scores if we had planned separately for each group
    ## This will take more time and we will need to make more number of dishes

    logger.error(f"Calculating Score for Separate")
    group_sizes={  ## group_size : num_groups_for_size
        2:10,
        3:10,
        5:10,
        7:5,
        10:5,
    }

    all_avg_objs=[0.0]*NUM_OBJECTIVES
    all_avg_time=[]

    for size,cnt in group_sizes.items():
        for i in range(cnt): ## 50 Groups
            time=0
            cnt=0
            avg_obj=[0.0]*NUM_OBJECTIVES
            ## Find the average objectives if we train the configs separately
            for id,j in enumerate(range(i,len(single_objs),cnt)):
                if id>=size:
                    break
                cnt+=1
                avg_obj=[avg_obj[i]+single_objs[j][i] for i in range(len(single_objs[j]))]
                time+=single_times[j] 

            avg_obj=[val/cnt for  val in avg_obj]
            avg_obj[4]=avg_obj[4]*cnt ## Number of dishes for separate is the sum of individual dishes
            time=time ## Time required for separate is the sum of individual times

            ## Take sum to find average of all averages to report as score of separate
            all_avg_objs=[all_avg_objs[i] + avg_obj[i] for i in range(len(avg_obj))]
            all_avg_time+=time

    all_avg_objs=[val/50 for val in all_avg_objs]
    all_avg_time/=50

    logger.error(f"Scores for Separate\nAvg Time:\n{str(all_avg_time)}\nAvg Objectives:\n{str(all_avg_objs)}")
                    

if __name__=="__main__":
    prefs_configs_all=generate_preferences(all_subsets=True) ## 20 configs
    run_configs("Prefernces Configs",prefs_configs_all) ## Estimated Time 20 minutes (number of users)

    cons_configs_all=generate_constraints(all_subsets=True) ## 32 configs
    run_configs("Constraints Configs",cons_configs_all) ## Estimated Time 32 minutes
    
    single_configs_all=generate_all_single() ## 50 configs
    single_objs,single_times=run_configs("Single Configs",single_configs_all) ## Estimated Time 50 minutes

    # plan_multiple_configs_all=generate_all_multiple("multiple") ## 40 configs
    # run_configs("Plan Multiple Configs",plan_multiple_configs_all) ## Estimated Time 185 minutes
    
    # plan_in_onego_configs_all=generate_all_multiple("many_in_one") ## 40 configs
    # run_configs("Plan In One Go Configs",plan_in_onego_configs_all) ## Estimated Time 185 minutes

    # get_values_for_separate(single_objs,single_times)

    

    ## Estimated Time Required For Complete Run: 470 minutes: 8 hours
    
    