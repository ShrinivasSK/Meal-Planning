from plan import MealPlanner, Individual
import logging
import copy
import random
import json
import numpy as np
import time
import sys

DEBUG = True

logging.basicConfig(filename='Outputs/output_weighted_sum.log',
                    filemode='a',
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO if DEBUG else logging.ERROR)

logger=logging.getLogger()

NUM_OBJECTIVES = 2


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

def set_seed(seed:int = 3407):
    random.seed(seed)
    np.random.seed(seed)

def run_config(config,outfile,cfg_id):
    set_seed()

    logger.warning(f"Config:\n {config}")
    
    start=time.time()
    if config['planning']['plan_type']=='multiple':
        final_res=MealPlanner.plan_multiple(config,logger)
    else:
        final_res = MealPlanner.plan(config,logger)

    obj=[0.0]*NUM_OBJECTIVES
    for ind in final_res:
        if config['planning']['plan_type']=='multiple':
            ind.calculate_objectives(is_final_multiple=True)
        if not DEBUG:
            save_plans(outfile,ind,cfg_id)
        temp=[obj[i]+ind.objectives[i] for i in range(len(ind.objectives))]
        dish_cnt=obj[1]
        for dish in ind.meal_plan.plan:
            if dish.id!=0:
                dish_cnt+=dish.quantity
        temp.append(dish_cnt)
        obj=temp

    obj=[v/5 for v in obj]

    end=time.time()

    logger.warning(f"Time Required:\n{end-start}")
    logger.warning("Average Objectives:\n"+str(obj))

    return obj,end-start

def save_plans(outfile,individual: Individual,cfg_id):
    with open(outfile,'a') as f:
        for dish in individual.meal_plan.plan:
            f.write(str(dish.id)+'\t'+str(dish.quantity)+'\t')
        f.write(str(cfg_id)+'\n')

def run_configs(title,configs):
    logger.error(f"Running {title}")
    avg_time=0
    avg_obj=[0.0]*NUM_OBJECTIVES
    objs=[]
    times=[]
    outfile = f'Outputs/single_objective/{title}.tsv'
    if not DEBUG:
        with open(outfile,'w') as f:
            for i in range(15):
                f.write(f'Dish {i+1} id\tDish {i+1} qty\t')
            f.write('Cfg Id\n')
    for cfg_id,cfg in enumerate(configs):
        try: 
            obj,time=run_config(cfg,outfile,cfg_id)
            avg_obj=[avg_obj[i]+obj[i] for i in range(len(obj))]
            avg_time+=time

            objs.append(obj)
            times.append(time)
        except Exception as e:
            logger.info(f"Exception {str(e)} in cfg {cfg_id}")

    avg_obj=[val/len(configs) for val in avg_obj]
    avg_time/=len(configs)
    
    logger.error(f"{title}\nAvg Time:\n{str(avg_time)}\nAvg Objectives:\n {str(avg_obj)}")

    return objs,time

if __name__=="__main__":
    all_single = generate_all_single()
    
    weights1 = [ 1, 1, 1 ]
    weights2 = [ 2, 1, 1 ]
    weights3 = [ 1, 2, 1 ]
    weights4 = [ 1, 1, 2 ]
    weights5 = [ 2, 2, 1 ]
    weights6 = [ 2, 1, 2 ]
    weights7 = [ 1, 2, 2 ]
    weights8 = [ 0.8, 0.7, 1.5 ] ## inversely proportional to their final value

    weights = [weights1,weights2,weights3,weights4,
               weights5,weights6,weights7,weights8]
    
    if DEBUG:
        weights_id = 0
    else:
        weights_id = int(sys.argv[1])

    all_single_copy = copy.deepcopy(all_single)
    for cfg in all_single_copy:
        cfg["planning"]["weights"] = weights[weights_id]
        cfg["planning"]["ga"] = "nsga"
        cfg["planning"]["num_objectives"] = 1
    if DEBUG:
        run_config(all_single_copy[0],"",0)
    else:
        run_configs(f"Weights{weights_id+1}",all_single_copy)
