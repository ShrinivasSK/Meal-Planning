## Main NSGA Loop

"""
1. Create Initial Population: both feasible and infeasible
2. Initialise Weights
3. In Each Generation
    a. Create Children: Add to Population
    b. Education 
    c. Survivor Selection
    d. Wt Adjustments
    e. Diversification
6. Return final population front

Attributes
1. Objective Functions
    a. History Values
"""

from plan.dataset import Dataset
from plan.individual import Individual
from NSGA.population import Population
from plan.problem import ProblemConfig
from HybridGA.utils import HybridGAUtils

from tqdm import tqdm

import logging

logger=logging.getLogger()

class Evolution:

    def __init__(self,dataset: Dataset,problem_config:ProblemConfig) -> None:
        self.utils=HybridGAUtils(dataset,problem_config)

        self.problem_config=problem_config
        self.population:Population=None
        self.history_objectives:"list[list[float]]"=[]

    def evolve(self,group_index:int =0 )->"list[Individual]":
        ## 1. Creating Initial Population
        logger.info("Creating Initial Population...")
        if self.problem_config.planning.plan_type=="many_in_one":
            self.population=self.utils.create_initial_population_many()
        else:
            self.population=self.utils.create_intitial_population(group_index)
        
        logger.info("Initial Population Size: "+str(len(self.population)))

        ## 2. Initialise Weights
        penalty_wts=[
            self.problem_config.HybridGA.nutri_penalty_wt,
            self.problem_config.HybridGA.wt_penalty_wt
        ]
        iter_without_improvement=0

        for pop in self.population["feasible"]:
            pop.calculate_objectives(penalty_wts,group_index)
        for pop in self.population["infeasible"]:
            pop.calculate_objectives(penalty_wts,group_index)

        logger.info("Random Initial Meal Plan: ")
        logger.info(self.population["feasible"][0])

        logger.info("Initial Avg Objectives: "+str(self.population.calculate_average_objectives(penalty_wts,group_index)))

        ## Note best solution
        _,best_val=self.utils.find_best_solution(self.population)

        logger.info("Starting Evolution..")
        for i in tqdm(range(self.utils.problem_config.HybridGA.number_of_generations)):
            # Creating Children
            children=self.utils.create_children(self.population,group_index)
            self.population.extend(children)

            ## Survivor Selection
            new_population=self.utils.survivor_selection(self.population)

            ## Note best solution
            _,curr_val=self.utils.find_best_solution(new_population)
            if curr_val>=best_val:
                _,best_val=_,curr_val
                iter_without_improvement=0
            else:
                iter_without_improvement+=1

            ## Weight Adjustment
            feas_prop=len(self.population["feasible"])/len(self.population)
            if feas_prop <= self.problem_config.HybridGA.target_proportion - 0.05:
                penalty_wts=[wt*1.2 for wt in penalty_wts]
            elif feas_prop >= self.problem_config.HybridGA.target_proportion + 0.05:
                penalty_wts=[wt*0.85 for wt in penalty_wts]

            ## Diversification
            if iter_without_improvement!=0 and (iter_without_improvement%self.problem_config.HybridGA.diversification_iter):
                pass
            
            ## Logging State
            if(i%10==0):
                obj=new_population.calculate_average_objectives(penalty_wts,group_index)
                logger.info("Iteration "+str(i)+": Objective Value: "+str(obj))
                self.history_objectives.append(obj)

            self.population = new_population

        
        logger.info("Objective Value: "+str(obj))
        
        ## Get Pareto Front
        pareto_front= self.utils.get_pareto_front(self.population)

        return pareto_front

