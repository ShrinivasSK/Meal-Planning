## Class to Manage the Data
import pandas as pd
import numpy as np
from collections import defaultdict
import networkx as nx
from gensim.models.keyedvectors import KeyedVectors
from typing import Tuple
import random
from scipy.spatial import KDTree

from NSGA.dish_ import Dish

class Dataset:

    def __init__(self) -> None:
        df_dishes=pd.read_csv("./Data/Processed/dishes.csv")
        df_ings=pd.read_csv("./Data/Processed/ingredients.csv")
        df_dish_ings=pd.read_csv("./Data/Processed/rec_ing.csv")
              
        self.titles=df_dishes['Title'].values
        self.ings=df_ings['Name'].values

        dishes=df_dishes.to_dict('records')
        self.id2dish={}
        for dish in dishes:
            self.id2dish[dish['ID']]={
                'Title': dish['Title'],
                'Nutrition': [dish['Calories'],dish['Fats'],dish['Proteins'],dish['Carbohydrates']],
                'Serving Size': dish['Typical_serving_size'],
                'Ingredients': '',
                'Breakfast': dish['Breakfast'],
                'Lunch': dish['Lunch'],
                'Snacks': dish['Snacks'],
                'Dinner': dish['Dinner'],
                'Cuisine':dish['Cuisine'],
                'Category':dish['Category'],
                'Tags':dish['Tags']
            }

        dish=df_dish_ings['Recipe ID'].values
        ings=df_dish_ings['Ingredient ID'].values
        for i in range(len(dish)):
            self.id2dish[dish[i]]['Ingredients']+=self.ings[ings[i]-1]+"^"

        self.dish_vecs=np.load("Data/Processed/rec_vecs.npy")
        self.kdTree=KDTree(self.dish_vecs)

        self.ing_vector_model=KeyedVectors.load_word2vec_format("./Data/Recipe1M/vocab.bin", binary=True)
        self.ing_vocab=list(set(self.ing_vector_model.key_to_index.keys()))

        self.combi_model=KeyedVectors.load_word2vec_format("models/graph_combi.bin",binary=True)
        self.combi_vocab=set(self.combi_model.key_to_index.keys())

        self.cuisines=['North America', 'United States', 'Europe', 'Italy',
            'Middle East', 'South East Asia', 'Canada', 'France', 'Mexico',
            'British Isles', 'Australia & NZ', 'Greece', 'Eastern Europe',
            'Asia', 'South America', 'China', 'Japan', 'Africa',
            'Indian Subcontinent', 'Korea']
            

    def get_dish_vector(self,id:int):
        return self.dish_vecs[int(id)-1]

    def get_graph(self,file:str):
        return nx.read_edgelist("Data/Processed/graphs/"+file+".edgelist")
    
    def get_random_ingredients(self,count:int=5)->"list[list[float]]":
        vecs=[]
        for i in range(count):
            random_ing=self.ing_vocab[random.randint(0,len(self.ing_vocab)-1)]
            vecs.append(self.ing_vector_model[random_ing])
        return vecs

    def get_closest_dish(self,vec:"list[float]")->Tuple[int,"list[float]"]:
        _,index=self.kdTree.query(vec)
        return index+1,self.dish_vecs[index]

    def get_dish_nutri(self,dish: Dish)->"list[float]":
        return [n*dish.quantity for n in self.id2dish[int(dish.id)]['Nutrition'] ]

    def get_dish_weight(self,dish: Dish)->int:
        return self.id2dish[int(dish.id)]['Serving Size']*dish.quantity

    def get_combi_dish(self,dish1:Dish,dish2:Dish)->float:
        if dish1.id not in self.combi_vocab or dish2.id not in self.combi_vocab:
            return 0
        return self.combi_model.similarity(dish1.id,dish2.id)##*abs(np.dot(dish1.vector[1:-1],dish2.vector[1:-1]))
    
    def get_dish_title(self,dish_id:int)->str:
        return self.id2dish[int(dish_id)]['Title']
    
    def get_dish_tags(self,dish_id:int)->str:
        return self.id2dish[int(dish_id)]['Tags']
    
    def get_dish_category(self,dish_id:int)->str:
        return self.id2dish[int(dish_id)]['Category']

    def get_dish_cuisine(self,dish_id:int)->str:
        cuisine=self.id2dish[int(dish_id)]['Cuisine']
        # print(cuisine)
        if(cuisine not in self.cuisines):
            return -1
        else:
            return cuisine

    def get_random_dish(self,meal)->Dish:
        id=random.randint(0,len(self.titles)-1)
        while self.id2dish[id+1][meal]!=1:
            id=random.randint(0,len(self.titles)-1)
        return id+1,self.dish_vecs[id]

    


        