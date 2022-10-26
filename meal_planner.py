from NSGA.dataset_ import Dataset
from NSGA.evolution_ import Evolution
from NSGA.problem_ import ProblemConfig
from NSGA.individual_ import Individual

import logging
import json
from sklearn.cluster import KMeans
from scipy.spatial import KDTree
import numpy as np

logging.basicConfig(filename='Outputs/output.log',
                    filemode='a',
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger=logging.getLogger()

class NSGAMealPlanner:
    
    @staticmethod
    def plan(config:dict) -> "list[Individual]":
        
        logger.info("Initialising Variables.....")
        
        dataset=Dataset()
        problem_config=ProblemConfig(config,dataset)
        
        evolution=Evolution(dataset,problem_config)

        logger.info("Running")
        
        pareto_front=evolution.evolve()
        

        logger.info("NSGA Complete")
        logger.info("Front Size: "+ str(len(pareto_front)))

        logger.info("Objective Values History: ")
        logger.info(evolution.history_objectives)

        res_objectives=[] 
        for individual in pareto_front:
            res_objectives.append(individual.objectives)

        logger.info("Objective Values of Pareto Front: ")
        logger.info(str(res_objectives))

        final_pop=NSGAMealPlanner.post_process(pareto_front,res_objectives)
        
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



if __name__=="__main__":
    
    with open("config.json") as f:
        config=json.load(f)

    final_res = NSGAMealPlanner.plan(config)

