from plan import MealPlanner

import logging
import json
import time

logging.basicConfig(filename='Outputs/output.log',
                    filemode='a',
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger=logging.getLogger()

# TODO: 
# Threshold on individual objectives when selecting representatives

if __name__=="__main__":
    
    with open("config.json") as f:
        config=json.load(f)

    logger.info(f"Config:\n {config}")

    start=time.time()

    if config['planning']['plan_type']=='multiple':
        final_res=MealPlanner.plan_multiple(config,logger)
    else:
        final_res = MealPlanner.plan(config,logger)

    end=time.time()

    logger.info(f"Time Required: {end-start}")

