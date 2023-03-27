## Population Class: Has a list of citizens

from plan.individual import Individual

NUM_OBJECTIVES=4

class Population:
    
    def __init__(self) -> None:
        self.population:"dict[str,list[Individual]]"=list()
        self.fronts:"dict[str,list[list[Individual]]]"=[]

    def __len__(self) -> int:
        return len(self.population["feasible"])+len(self.population["infeasible"])
    
    def __getitem__(self,which)->list[Individual]:
        return self.population[which]

    def extend(self,new_inds:"dict[str,list[Individual]]"):
        self.population["feasible"].extend(new_inds["feasible"])
        self.population["infeasible"].extend(new_inds["infeasible"])

    def append(self,new_ind:Individual,which:str):
        self.population[which].append(new_ind)

    def calculate_average_objectives(self,penalty_wts,which:str,group_index:int=0)->"list[float]":
        obj=[0.0]*NUM_OBJECTIVES
        
        for citizen in self.population[which]:
            cit_obj=citizen.calculate_objectives(penalty_wts,group_index)
            for i in range(NUM_OBJECTIVES):
                obj[i]+=cit_obj[i]
        
        for i in range(len(obj)):
            obj[i]/=len(self.population)
        
        return obj