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
    def __init__(self,config:dict,data:Dataset) -> None:
        self.user_count=config['user_count']
        self.population_size=config['population_size']

        self.num_nutrients=config['number_of_nutrients']
        
        self.breakfast_dishes=config['breakfast_dishes']
        self.lunch_dishes=config['lunch_dishes']
        self.snacks_dishes=config['snacks_dishes']
        self.dinner_dishes=config['dinner_dishes']

        self.breakfast_id_limit=self.breakfast_dishes
        self.lunch_id_limit=self.breakfast_id_limit+self.lunch_dishes
        self.snacks_id_limit=self.lunch_id_limit+self.snacks_dishes
        self.dinner_id_limit=self.snacks_id_limit+self.dinner_dishes

        self.id2meal={
            0:'Breakfast',
            1 :'Breakfast',
            2: 'Breakfast',
            3:'Lunch',
            4 :'Lunch',
            5 :'Lunch',
            6: 'Lunch',
            7 :'Lunch',
            8: 'Snacks',
            9: 'Snacks',
            10 :'Dinner',
            11: 'Dinner',
            12: 'Dinner',
            13: 'Dinner',
            14: 'Dinner', 
        }

        self.nutri_reqs_day=config['daily_nutrient_requirements']
        self.nutri_reqs_breakfast=config['breakfast_nutrient_requirements']
        self.nutri_reqs_lunch=config['lunch_nutrient_requirements']
        self.nutri_reqs_snacks=config['snacks_nutrient_requirements']
        self.nutri_reqs_dinner=config['dinner_nutrient_requirements']
        self.nutri_limits=[
            self.nutri_reqs_day,
            self.nutri_reqs_breakfast,
            self.nutri_reqs_lunch,
            self.nutri_reqs_snacks,
            self.nutri_reqs_dinner
        ]
        
        self.weight_reqs_day=config['daily_weight_requirements']
        self.weight_reqs_breakfast=config['breakfast_weight_requirements']
        self.weight_reqs_lunch=config['lunch_weight_requirements']
        self.weight_reqs_snacks=config['snacks_weight_requirements']
        self.weight_reqs_dinner=config['dinner_weight_requirements']
        self.wt_limits=[
            self.weight_reqs_day,
            self.weight_reqs_breakfast,
            self.weight_reqs_lunch,
            self.weight_reqs_snacks,
            self.weight_reqs_dinner
        ]

        self.mutation_param=config['mutation_parameter']
        self.tournament_participants=config['number_of_tournament_participants']
        self.tournament_prob=config['tournament_probability']
        self.number_of_generations=config['number_of_generations']
        self.dish_dimensions=config['dish_vector_dimensions']

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

