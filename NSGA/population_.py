## Population Class: Has a list of citizens

from NSGA.individual_ import Individual


NUM_OBJECTIVES=4

class Population:
    
    def __init__(self) -> None:
        self.population:list[Individual]=list()
        self.fronts:list[list[Individual]]=[]

    def __len__(self) -> int:
        return len(self.population)
    
    def __iter__(self):
        return self.population.__iter__()

    def extend(self,new_inds:list[Individual]):
        self.population.extend(new_inds)

    def append(self,new_ind:Individual):
        self.population.append(new_ind)

    def calculate_average_objectives(self)->list[float]:
        obj=[0.0]*NUM_OBJECTIVES
        
        for citizen in self.population:
            cit_obj=citizen.calculate_objectives()
            for i in range(NUM_OBJECTIVES):
                obj[i]+=cit_obj[i]
        
        for i in range(len(obj)):
            obj[i]/=len(self.population)
        
        return obj