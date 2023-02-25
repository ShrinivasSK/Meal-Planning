## Putting it all together

from NSGA.dataset_ import Dataset
from NSGA.evolution_ import Evolution
from NSGA.problem_ import ProblemConfig

class NSGAMealPlanner:
    
    @staticmethod
    def plan(config:dict):
        
        print("Initialising Variables.....")
        
        problem_config=ProblemConfig(**config)
        problem_config.init_other()

        dataset=Dataset(config)
        evolution=Evolution(dataset,problem_config)

        print("Running")
        
        final_population=evolution.evolve()

        print("Meal Plan Generated: ")
        print("Front Size: ", len(final_population))
        for individual in final_population:
            print(individual)
            print()
        
        print("Objective Values History: ")
        print(evolution.history_objectives)

    @staticmethod
    def plan_multiple(config: dict):
        pass
    