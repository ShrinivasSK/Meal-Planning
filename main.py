from NSGA.meal_planner_ import NSGAMealPlanner

import json

if __name__=="__main__":
    
    with open("F:\SHRINIVAS\KGP\BTP\Meal-Planning\config.json") as f:
        config=json.load(f)

    NSGAMealPlanner.plan(config)