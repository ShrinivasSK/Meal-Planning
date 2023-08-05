from testing import generate_all_single
from plan import MealPlanner, Individual
import logging
import copy
import random
import numpy as np
import time
import sys

logging.basicConfig(filename='Outputs/output_weighted_sum.log',
                    filemode='a',
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)

logger=logging.getLogger()

NUM_OBJECTIVES = 2

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
    
    weights_id = int(sys.argv[1])

    # for id, weight in enumerate(weights):
    #     # if id<7:
    #     #     continue
    all_single_copy = copy.deepcopy(all_single)
    for cfg in all_single_copy:
        cfg["planning"]["weights"] = weights[weights_id]
        cfg["planning"]["ga"] = "nsga"
    run_configs(f"Weights{weights_id+1}",all_single_copy)
