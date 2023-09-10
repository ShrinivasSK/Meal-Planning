from plan import MealPlanner, Individual
import logging
import copy
import random
import numpy as np
import time
import json
import sys

DEBUG = True

logging.basicConfig(filename='Outputs/output_ablation.log',
                    filemode='a',
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO if DEBUG else logging.ERROR)

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

    if not DEBUG:
        for ind in final_res:
            save_plans(outfile,ind,cfg_id)

    end=time.time()

    logger.warning(f"Time Required:\n{end-start}")

    return end-start

def save_plans(outfile,individual: Individual,cfg_id):
    with open(outfile,'a') as f:
        for dish in individual.meal_plan.plan:
            f.write(str(dish.id)+'\t'+str(dish.quantity)+'\t')
        f.write(str(cfg_id)+'\n')

def run_configs(title,configs):
    logger.error(f"Running {title}")
    avg_time=0
    times=[]
    outfile = f'Outputs/ablation_study/{title}.tsv'
    if not DEBUG:
        with open(outfile,'w') as f:
            for i in range(15):
                f.write(f'Dish {i+1} id\tDish {i+1} qty\t')
            f.write('Cfg Id\n')
    for cfg_id,cfg in enumerate(configs):
        try: 
            time=run_config(cfg,outfile,cfg_id)
            avg_time+=time

            times.append(time)
        except Exception as e:
            logger.info(f"Exception {str(e)} in cfg {cfg_id}")

    avg_time/=len(configs)
    
    logger.error(f"{title}\nAvg Time:\n{str(avg_time)}\n")

    return time

if __name__=="__main__":
    all_single = generate_all_single()
    
    objective_names = ['diversity','combination','preference']
    objectives=[
        ['constraint']
    ]
    for i in range(1,8):
        curr_obj=[]
        for j in range(3):
            if (i & (1 << j))!=0:
                curr_obj.append(objective_names[j])
        objectives.append(curr_obj)
    
    if not DEBUG:
        ablation_id = int(sys.argv[1])
    else:
        ablation_id = 7

    all_single_copy = copy.deepcopy(all_single)
    for cfg in all_single_copy:
        cfg["planning"]["objectives"] = objectives[ablation_id]
        cfg["planning"]["ga"] = "nsga"
        if ablation_id == 0:
            cfg["planning"]["num_objectives"] = 1
        else:
            cfg["planning"]["num_objectives"] = bin(ablation_id).count('1')
    if DEBUG:
        run_config(all_single_copy[0],"",0)
    else:
        run_configs(f"Ablation_Study{ablation_id+1}",all_single_copy)
