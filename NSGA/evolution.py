## Main NSGA Loop

"""
1. Create Initial Population
2. Fast Dominated Sort
3. Calculate Crowding Distance of Fronts
4. Create Children
5. In Each Generation
    a. Add Children to population
    b. Fast Dominated Sort
    c. Add top citizens into next generation
    d. Save returned population
    e. Fast Dominated Sort, Crowding Distance and Create Children
6. Return returned Population

Attributes
1. Objective Functions
    a. History Values
"""

from plan import Dataset, Individual, ProblemConfig
from NSGA.utils import NSGAUtils
from NSGA.population import NSGAPopulation

from tqdm import tqdm
import logging

logger=logging.getLogger()

class Evolution:

    def __init__(self,dataset: Dataset,problem_config:ProblemConfig) -> None:
        self.utils=NSGAUtils(dataset,problem_config)

        self.problem_config=problem_config
        self.population:NSGAPopulation=None
        self.history_objectives:"list[list[float]]"=[]

    def evolve(self,group_index:int =0 )->"list[Individual]":
        logger.info("Creating Initial Population...")
        if self.problem_config.planning.plan_type=="many_in_one":
            self.population=self.utils.create_initial_population_many()
        else:
            self.population=self.utils.create_intitial_population(group_index)
        
        logger.info("Initial Population Size: "+str(len(self.population)))

        for pop in self.population:
            pop.calculate_objectives(group_index)

        # logger.info("Fast Non Dominated Sorting")
        self.utils.fast_nondominated_sort(self.population)

        logger.info("Random Initial Meal Plan: ")
        logger.info(self.population.fronts[0][0])

        # logger.info("Calculating Crowding Distance")
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)

        # logger.info("Creating Children")
        children=self.utils.create_children(self.population,group_index)

        logger.info("Initial Avg Objectives: "+str(self.population.calculate_average_objectives(group_index)))

        logger.info("Starting Evolution..")
        for i in tqdm(range(self.utils.problem_config.NSGA.number_of_generations)):
            # logger.info("\nIteration: ",i+1)

            self.population.extend(children)
            # logger.info("Fast Non Dominated Sorting")
            self.utils.fast_nondominated_sort(self.population)

            # logger.info("Creating new population")
            new_population=NSGAPopulation()

            front_num=0
            while len(new_population) + len(self.population.fronts[front_num]) <= self.utils.problem_config.NSGA.population_size:
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1

            self.utils.calculate_crowding_distance(self.population.fronts[front_num])
            self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
            new_population.extend(self.population.fronts[front_num][0:self.utils.problem_config.NSGA.population_size-len(new_population)])

            if(i%10==0):
                obj=new_population.calculate_average_objectives(group_index)
                logger.info("Iteration "+str(i)+": Objective Value: "+str(obj))
                self.history_objectives.append(obj)

            # logger.info("Preparing for next iteration")
            self.population = new_population
            self.utils.fast_nondominated_sort(self.population)
            for front in self.population.fronts:
                self.utils.calculate_crowding_distance(front)
            children = self.utils.create_children(self.population,group_index)

        
        logger.info("Objective Value: "+str(obj))
        
        return self.population.fronts[0]

