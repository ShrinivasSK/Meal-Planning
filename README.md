# Meal-Planning
My BTech Term Project (BTP) at IIT Kharagpur

Refer to the [BTP Report]() and my [Final Presentation](https://docs.google.com/presentation/d/1fQsqLScuYwMUZ3CjsdzNRRIdSeeqlTw3ptQ-gWi70uM/edit?usp=sharing) for details. 

A compilation of the slides presented almost every week during the project: [here](https://docs.google.com/presentation/d/1I0NKnkUPOn2wl0MwkUNg6L4UYQskqj8PH4YBrXADFb0/edit?usp=sharing)

### Required Libraries
Sklearn, scipy, Gensim, Numpy, Pandas, Networkx, Tqdm

### How to Run
- Install the required libraries
- Update the config.json file. A standard one has been provided
- Run the main file
`python3 main.py`

### Code Structure
- main.py: The file that needs to be run. Loads the config from the config.json file. 
- hyper_parameter_tuning.py: Contains code to perform a grid search for the best hyper-parameters for the GA
- testing.py: The code for testing the pipeline for a variety of constraints
- Configs: 
    various configs that are used for testing the model for a variety of constraints and preferences. 
- Data: 
    Dataset files. For more details refere [here](./Data/README.md)
- Hybrid GA: 
    Contains the code for Evolution according to [Hybrid GA](https://www.researchgate.net/publication/230846314_A_hybrid_genetic_algorithm_with_adaptive_diversity_management_for_a_large_class_of_vehicle_routing_problems_with_time-windows) algorithm, the Hybrid GA Population maintatining separate lists for feasible and infeasible solutions and Utility files for Hybrid GA.
- NSGA: 
    Contains the code for Evolution according to [NSGA 2](https://ieeexplore.ieee.org/document/996017) algorithm, the standard GA population and utility files
- plan: 
    Contains code for the meal planner. Details [here](./plan/README.md)
- Outputs
    Some output logs that contain suggested meal plans
- Prepro:
    - Contains code for preprocessing the dataset. The Data folder contains the preprocessed files

        
