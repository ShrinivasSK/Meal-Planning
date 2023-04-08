## Population Class: Has a list of citizens
import itertools
from typing import Iterator
from plan.individual import Individual

NUM_OBJECTIVES=4

class HybridGAPopulation:
    
    def __init__(self) -> None:
        self.population:"dict[str,list[Individual]]"={
            "feasible":[],
            "infeasible":[]
        }

    def __len__(self) -> int:
        return len(self.population["feasible"])+len(self.population["infeasible"])
    
    def __getitem__(self,which)->"list[Individual]":
        return self.population[which]
    
    def __iter__(self)->Iterator[Individual]:
        return itertools.chain(self.population["feasible"],self.population["infeasible"])

    def extend(self,new_inds:"dict[str,list[Individual]]"):
        self.population["feasible"].extend(new_inds["feasible"])
        self.population["infeasible"].extend(new_inds["infeasible"])

    def extend_list(self,new_inds:"list[Individual]"):
        for ind in new_inds:
            if ind.feasiblity==True:
                self.population["feasible"].append(ind)
            else:
                self.population["infeasible"].append(ind)

    def append(self,new_ind:Individual,which:str):
        self.population[which].append(new_ind)

    def calculate_objectives(self,penalty_wts,group_index:int=0)->"list[float]":
        for citizen in self.population["feasible"]:
            citizen.calculate_objectives(penalty_wts,group_index)

        for citizen in self.population["infeasible"]:
            citizen.calculate_objectives(penalty_wts,group_index)

    def calculate_average_objectives(self,penalty_wts,group_index:int=0)->"list[float]":
        obj=[0.0]*NUM_OBJECTIVES
        if len(self.population["feasible"])==0:
            return obj
        
        for citizen in self.population["feasible"]:
            cit_obj=citizen.calculate_objectives(penalty_wts,group_index)
            for i in range(NUM_OBJECTIVES):
                obj[i]+=cit_obj[i]
        
        for i in range(len(obj)):
            obj[i]/=len(self.population["feasible"])
        
        return obj