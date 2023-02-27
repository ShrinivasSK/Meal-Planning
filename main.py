from NSGA.meal_planner_ import NSGAMealPlanner

import logging
import json
from sklearn_extra.cluster import KMedoids
from scipy.spatial import KDTree
import numpy as np

logging.basicConfig(filename='Outputs/output.log',
                    filemode='a',
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger=logging.getLogger()

if __name__=="__main__":
    
    with open("config.json") as f:
        config=json.load(f)

    if config['planning']['plan_type']=='multiple':
        final_res=NSGAMealPlanner.plan_multiple(config,logger)
    else:
        final_res = NSGAMealPlanner.plan(config,logger)

