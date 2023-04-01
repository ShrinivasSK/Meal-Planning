## Defining the NSGA Problem
from plan.dataset import Dataset

"""
Attributes:

2. Data of Dishes, etc
Methods
1. Calculate Objectives
2. Create Individual
"""

class ProblemConfig:
    def __init__(self,**config) -> None:
        for key, value in config.items():
            if type(value) == dict:
                config[key] = ProblemConfig(**value)
            if type(value)==list:
              config[key]=[]
              for val in value:
                if type(val)==dict:
                  config[key].append(ProblemConfig(**val))
                else:
                  config[key].append(val)
        self.__dict__.update(config)
    
    def init_other(self,data:Dataset):
        self.breakfast_id_limit=self.meal.breakfast_dishes
        self.lunch_id_limit=self.breakfast_id_limit+self.meal.lunch_dishes
        self.snacks_id_limit=self.lunch_id_limit+self.meal.snacks_dishes
        self.dinner_id_limit=self.snacks_id_limit+self.meal.dinner_dishes

        self.init_feasible_population_limit=self.HybridGA.target_proportion*self.HybridGA.population_size
        self.init_infeasible_population_limit=(1-self.HybridGA.target_proportion)*self.HybridGA.population_size
        
        # for group in self.groups:
        #     _,group.positive_preferences=self.get_cuisines(group.positive_preferences,data.cuisines)
        #     _,group.negative_preferences=self.get_cuisines(group.negative_preferences,data.cuisines)

        # print(self.preferred_cuisines,self.rejected_cuisines,self.cuisine_invalid)

    def get_cuisines(self,prefs,cuisines):
        ret=set()
        for val in prefs:
            if val in cuisines:
                ret.add(cuisines.index(val))
            else:
                return -1,[]
        return 1,ret   

    def get_meal_from_id(self,id):
        
        if self.planning.plan_type=="many_in_one":
            self.breakfast_id_limit=self.meal.breakfast_dishes*self.planning.group_count
            self.lunch_id_limit=self.breakfast_id_limit+(self.meal.lunch_dishes*self.planning.group_count)
            self.snacks_id_limit=self.lunch_id_limit+(self.meal.snacks_dishes*self.planning.group_count)
            self.dinner_id_limit=self.snacks_id_limit+(self.meal.dinner_dishes*self.planning.group_count)
        else:
            self.breakfast_id_limit=self.meal.breakfast_dishes
            self.lunch_id_limit=self.breakfast_id_limit+self.meal.lunch_dishes
            self.snacks_id_limit=self.lunch_id_limit+self.meal.snacks_dishes
            self.dinner_id_limit=self.snacks_id_limit+self.meal.dinner_dishes
            
        if(id<self.breakfast_id_limit):
            return 'Breakfast'
        elif(id<self.lunch_id_limit):
            return 'Lunch'
        elif(id<self.snacks_id_limit):
            return 'Snacks'
        else:
            return 'Dinner'


