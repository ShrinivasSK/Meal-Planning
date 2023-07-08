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

from plan import Dataset, Individual, ProblemConfig

from HybridGA.utils import HybridGAUtils
from HybridGA.population import HybridGAPopulation

from tqdm import tqdm

import logging

logger=logging.getLogger()

class Evolution:

    def __init__(self,dataset: Dataset,problem_config:ProblemConfig) -> None:
        self.utils=HybridGAUtils(dataset,problem_config)

        self.problem_config=problem_config
        self.population:HybridGAPopulation=None
        self.history_objectives:"list[list[float]]"=[]

    def evolve(self,group_index:int =0 )->"list[Individual]":
        ## 1. Creating Initial Population
        logger.info("Creating Initial Population...")
        if self.problem_config.planning.plan_type=="many_in_one":
            self.population=self.utils.create_initial_population_many(limit=self.problem_config.HybridGA.population_size)
        else:
            self.population=self.utils.create_intitial_population(limit=self.problem_config.HybridGA.population_size,
                                                                group_index=group_index)

        logger.info("Initial Population Size: "+str(len(self.population)))

        ## 2. Initialise Weights
        penalty_wts=[
            self.problem_config.HybridGA.nutri_penalty_wt,
            self.problem_config.HybridGA.wt_penalty_wt
        ]
        iter_without_improvement=0

        logger.info("Initial Avg Objectives: "+str(self.population.calculate_average_objectives(penalty_wts,group_index)))
        
        ## Note best solution
        for ind in self.population["infeasible"]:
            ind.calculate_objectives(penalty_wts=penalty_wts,group_index=group_index)

        logger.info("Random Initial Meal Plan: ")
        if len(self.population["feasible"])!=0:
            logger.info(self.population["feasible"][0])
        else:
            logger.info(self.population["infeasible"][0])

        # self.utils.get_biased_fitness_values(self.population)
        self.utils.calculate_rank_and_crowding(self.population)
        _,best_val=self.utils.find_best_solution(self.population)

        logger.info("Starting Evolution..")
        for i in tqdm(range(self.utils.problem_config.HybridGA.number_of_generations)):
            ## Creating Children
            ## 1. Choose Parents with tournament selection
            ## 2. Cross Over
            ## 3. Mutation
            ## 4. Add to correct sub population
            children=self.utils.create_children(self.population,penalty_wts=penalty_wts,group_index=group_index,limit=len(self.population))

            ## Local Search: Enhance Children
            children=self.utils.educate(children,penalty_wts,group_index)
            
            self.population.extend(children)

            ## Survivor Selection
            self.population=self.utils.survivor_selection(self.population,limit=len(self.population)//2)

            ## Note best solution
            _,curr_val=self.utils.find_best_solution(self.population)
            if curr_val>=best_val:
                _,best_val=_,curr_val
                iter_without_improvement=0
            else:
                iter_without_improvement+=1

            ## Weight Adjustment
            feas_prop=len(self.population["feasible"])/len(self.population)
            if feas_prop <= self.problem_config.HybridGA.target_proportion - 0.05:
                penalty_wts=[min(10,wt*1.2) for wt in penalty_wts]
            elif feas_prop >= self.problem_config.HybridGA.target_proportion + 0.05:
                penalty_wts=[wt*0.85 for wt in penalty_wts]

            ## Diversification
            if iter_without_improvement!=0 and (iter_without_improvement%self.problem_config.HybridGA.diversification_iter==0):
                ## Select Top 30% of the population and re-create the rest
                logger.info("Diversifying Population")
                self.population=self.utils.survivor_selection(self.population,limit=int(len(self.population)*0.3))
                
                if self.problem_config.planning.plan_type=="many_in_one":
                    new_population=self.utils.create_initial_population_many(limit=int(self.problem_config.HybridGA.population_size*0.7))
                else:
                    new_population=self.utils.create_intitial_population(limit=int(self.problem_config.HybridGA.population_size*0.7),
                                                                        group_index=group_index)

                self.population["feasible"].extend(new_population["feasible"])
                self.population["infeasible"].extend(new_population["infeasible"])
                
                self.population.calculate_objectives(penalty_wts,group_index)
                self.utils.calculate_rank_and_crowding(self.population)

                iter_without_improvement=0


            ## Logging State
            if(i%10==0):
                obj=self.population.calculate_average_objectives(penalty_wts,group_index)
                logger.info("Iteration "+str(i)+": Objective Value: "+str(obj))
                logger.info("Iteration "+str(i)+": Feasible: "+str(len(self.population["feasible"]))+" Infeasible: "+str(len(self.population["infeasible"])))
                self.history_objectives.append(obj)

        
        logger.info("Objective Value: "+str(obj))
        
        ## Get Pareto Front
        pareto_front= self.utils.get_pareto_front(self.population)

        if len(pareto_front)==0:
            logger.info("Pareto Front Empty")
            return self.population["feasible"]

        return pareto_front

