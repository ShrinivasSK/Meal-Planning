from testing import generate_all_single
from plan import MealPlanner, Individual
import logging
import copy
import random
import numpy as np
import time
import sys

logging.basicConfig(filename='Outputs/output_ablation.log',
                    filemode='a',
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)

logger=logging.getLogger()

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
    with open(outfile,'w') as f:
        for i in range(15):
            f.write(f'Dish {i+1} id\tDish {i+1} qty\t')
        f.write('Cfg Id\n')
    for cfg_id,cfg in enumerate(configs):
        # try: 
        time=run_config(cfg,outfile,cfg_id)
        avg_time+=time

        times.append(time)
        # except Exception as e:
            # logger.info(f"Exception {str(e)} in cfg {cfg_id}")

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
    
    ablation_id = int(sys.argv[1])

    all_single_copy = copy.deepcopy(all_single)
    for cfg in all_single_copy:
        cfg["planning"]["objectives"] = objectives[ablation_id]
        cfg["planning"]["ga"] = "nsga"
        if ablation_id == 0:
            cfg["planning"]["num_objectives"] = 1
        else:
            cfg["planning"]["num_objectives"] = bin(ablation_id).count('1')
    run_configs(f"Ablation_Study{ablation_id+1}",all_single_copy)
