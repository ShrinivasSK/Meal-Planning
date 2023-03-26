from NSGA.meal_planner_ import NSGAMealPlanner

import logging
import json
import numpy as np

logging.basicConfig(filename='Outputs/output_hyper_parameter_tuning.log',
                    filemode='a',
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)

logger=logging.getLogger()

if __name__=="__main__":
    
    with open("config.json") as f:
        config=json.load(f)

    # mutation_params=[0.1,0.2,0.3]
    # tournament_participants=[2,5,7]
    # tournament_prob=[0.7,0.8,0.9]
    # num_gen=[50,100,200]
    # pop_size=[70,100,150]

    mutation_params=[0.1]
    tournament_participants=[2]
    tournament_prob=[0.9]
    num_gen=[100]
    pop_size=[150,200,300,400,500]

    for mut in mutation_params:
        for tp in tournament_participants:
            for tprob in tournament_prob:
                for ng in num_gen:
                    for ps in pop_size:
                        config["NSGA"]["mutation_parameter"]=mut
                        config["NSGA"]["number_of_tournament_participants"]=tp
                        config["NSGA"]["tournament_probability"]=tprob
                        config["NSGA"]["number_of_generations"]=ng
                        config["NSGA"]["population_size"]=ps

                        logger.error(f"Config:\n {config}")

                        if config['planning']['plan_type']=='multiple':
                            final_res=NSGAMealPlanner.plan_multiple(config,logger)
                        else:
                            final_res = NSGAMealPlanner.plan(config,logger)

                        obj=[0.0]*4
                        for ind in final_res:
                            obj=[obj[i]+ind.objectives[i] for i in range(len(obj))]
                        obj=[v/5 for v in obj]
                        logger.error("Average Objectives: "+str(obj))

                        


    



