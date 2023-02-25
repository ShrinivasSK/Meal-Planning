## Defining the NSGA Problem
from NSGA.dataset_ import Dataset

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
    
    def init_other(self):
        self.breakfast_id_limit=self.meal.breakfast_dishes
        self.lunch_id_limit=self.breakfast_id_limit+self.meal.lunch_dishes
        self.snacks_id_limit=self.lunch_id_limit+self.meal.snacks_dishes
        self.dinner_id_limit=self.snacks_id_limit+self.meal.dinner_dishes

        self.nutri_limits:list[int]=[]
        self.wt_limits:list[int]=[]
        self.preferred_dishes:list[set]=[]
        self.rejected_dishes:list[set]=[]

        for i in range(self.planning.group_count):
            self.nutri_limits.append(
                self.groups[i].daily_nutrient_requirements,
            )
            self.wt_limits.append(
               self.groups[i].daily_weight_requirements,
            )

            self.preferred_dishes.append(
               set(self.groups[i].positive_preferences)
            )
            self.rejected_dishes.append(
               set(self.groups[i].negative_preferences)
            )

    def get_meal_from_id(self,id):
        if(id<self.breakfast_id_limit):
            return 'Breakfast'
        elif(id<self.lunch_id_limit):
            return 'Lunch'
        elif(id<self.snacks_id_limit):
            return 'Snacks'
        else:
            return 'Dinner'

        flag1,self.preferred_cuisines=self.get_cuisines(config['preferred_cuisines'],data.cuisines)
        flag2,self.rejected_cuisines=self.get_cuisines(config['rejected_cuisines'],data.cuisines)

        if(flag1==-1 or flag2==-1):
            self.cuisine_invalid=1
        else:
            self.cuisine_invalid=0

        # print(self.preferred_cuisines,self.rejected_cuisines,self.cuisine_invalid)

    def get_cuisines(self,data,cuisines):
        ret=set()
        for val in data:
            if val in cuisines:
                ret.add(cuisines.index(val))
            else:
                return -1,[]
        return 1,ret   

