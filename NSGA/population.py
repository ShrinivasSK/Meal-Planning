## Population Class: Has a list of citizens

from plan import Individual


class NSGAPopulation:
    
    def __init__(self) -> None:
        self.population:"list[Individual]"=list()
        self.fronts:"list[list[Individual]]"=[]

    def __len__(self) -> int:
        return len(self.population)
    
    def __iter__(self):
        return self.population.__iter__()
    
    def __getitem__(self,key):
        return self.population[key]

    def extend(self,new_inds:"list[Individual]"):
        for ind in new_inds:
            if ind not in self.population:
                self.population.append(ind)

    def append(self,new_ind:Individual):
        if new_ind not in self.population:
            self.population.append(new_ind)

    def calculate_average_objectives(self,group_index:int=0)->"list[float]":
        obj=None
        
        for citizen in self.population:
            cit_obj=citizen.calculate_objectives(group_index)
            if obj == None:
                obj = cit_obj
            else:
                for i in range(len(cit_obj)):
                    obj[i]+=cit_obj[i]
        
        for i in range(len(obj)):
            obj[i]/=len(self.population)
        
        return obj