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

from NSGA.dataset_ import Dataset
from NSGA.individual_ import Individual
from NSGA.population_ import Population
from NSGA.problem_ import ProblemConfig
from NSGA.utils import NSGAUtils

from tqdm import tqdm

class Evolution:

    def __init__(self,dataset: Dataset,problem_config:ProblemConfig) -> None:
        self.utils=NSGAUtils(dataset,problem_config)

        self.population:Population=None
        self.history_objectives:list[list[float]]=[]

    def evolve(self)->list[Individual]:
        print("Creating Initial Population...")
        self.population=self.utils.create_intitial_population()
        print(len(self.population))

        print("Fast Non Dominated Sorting")
        self.utils.fast_nondominated_sort(self.population)

        print(self.population.fronts[0][0])

        print("Calculating Crowding Distance")
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)

        print("Creating Children")
        children=self.utils.create_children(self.population)

        returned_population=None

        print("Initial Objectives")
        print(self.population.calculate_average_objectives())

        print(len(self.population))
        # for front in self.population.fronts:
        #     if(len(front)==0):
        #         continue
        #     print(front[0].calculate_objectives())
        objs=[]
        print("Starting Evolution..")
        for i in tqdm(range(self.utils.problem_config.NSGA.number_of_generations)):
            # print("\nIteration: ",i+1)

            self.population.extend(children)
            # print("Fast Non Dominated Sorting")
            self.utils.fast_nondominated_sort(self.population)

            # print("Creating new population")
            new_population=Population()

            front_num=0
            while len(new_population) + len(self.population.fronts[front_num]) <= self.utils.problem_config.NSGA.population_size:
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1

            self.utils.calculate_crowding_distance(self.population.fronts[front_num])
            self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
            new_population.extend(self.population.fronts[front_num][0:self.utils.problem_config.NSGA.population_size-len(new_population)])
            returned_population = self.population

            if(i%10==0):
                print("Objective Value: ",new_population.calculate_average_objectives())
                self.history_objectives.append(new_population.calculate_average_objectives())

            # print("Preparing for next iteration")
            self.population = new_population
            self.utils.fast_nondominated_sort(self.population)
            for front in self.population.fronts:
                self.utils.calculate_crowding_distance(front)
            children = self.utils.create_children(self.population)

            # print("Fronts", len(self.population.fronts))
            # for front in self.population.fronts:
            #     if(len(front)==0):
            #         continue
            #     print(front[0].calculate_objectives())

            # for front in self.population.fronts:
            #     for pop in front:
            #         print(pop.objectives)
            #     print()

            # break
        
        print("Objective Value: ",new_population.calculate_average_objectives())
        
        return self.population.fronts[0]

