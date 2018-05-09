import codecs
import os
import numpy as np
from ExtractExercises import *
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import random

MG = [[0,1,2],[3,4],[5,6,7,8],[9,10,11,12,13,14],[15,16,17],[18,19,20],[21,22,23],[24]]
MuscleGroups = [
'Hip Adductors',
'Hip Flexors',
'Tensor fasciae latae',
'Gluteus Maximus',
'Gluteus Medius',
'Calves',
'Hamstring',
'Quads',
'Sartorius',
'Tibialis Anterior',
'Erector Spinae',
'Infraspinatus',
'Latissimus Dorsi',
'Teres',
'Trapezius',
'Anterior Delts',
'Lateral Delts',
'Posterior Delts',
'Biceps',
'Forearms',
'Triceps',
'Abdominals',
'Obliques',
'Seratus Anterior',
'Cardio']

df = pd.read_excel('Exercises.xlsx', sheetname='Sheet1')
df = df.fillna(0)
X = df.as_matrix()
row1 = df.iloc[1:2,:]
Exercises = list(df['Exercise'])
Group = df[MuscleGroups[1]]
ExDict = {}

#Extract data from excel file and place in a dictionary
for row in X:
    ExDict[row[0]] = row[1:]

Ex = Exercises[1]
Similarity = []


def normalize(p):
    p = p/np.sum(p)
##    dif = 1.0 - np.sum(p)
##    p[0] += dif
    return p


def Generate_Circuit(num_exercises, ExList,dist):
    circuit = []
    for i in range(num_exercises):
        #Select Random exercise based on distribution
        dist = normalize(dist)
        choice = np.random.choice(len(dist),1, p = dist)[0]
        circuit.append(ExList[choice])
        
    return circuit

def calculate_circuit_similarity(ckt1, ckt2):
    score = np.zeros(len(ExDict[Ex]))
    for Ex1 in ckt1:
        for Ex2 in ckt2:
            dif = ExDict[Ex1] - ExDict[Ex2]
            score = score + dif
    return score


        
def Generate_Random_Workouts(ExList, num_ckts, emphasis):
    global ExDict
    dist = np.full(len(ExList),1/(len(ExList)))

    for emph in emphasis:
        for i,ex in enumerate(ExList):
            if ExDict[ex][emph[0]] > 0.5:
                dist[i] *= emph[1]
                
    dist = normalize(dist)
    Circuits = []

    for i in range(num_ckts):
        num_exercises = np.random.randint(5,10)
        Circuits.append(Generate_Circuit(num_exercises, ExList, dist))

    return Circuits

def Circuit_Vector(ckt):
    vec = np.zeros(len(ExDict[Ex]))
    for Ex1 in ckt:
        vec = vec + ExDict[Ex1]
    return vec
    
def cos_vec_sim(vec1,vec2):
    
    return np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))

def cos_ckt_sim(ckt1, ckt2):
    vec1 = Circuit_Vector(ckt1)
    vec2 = Circuit_Vector(ckt2)
    return cos_vec_sim(vec1,vec2)
    

class Mover(object):
    def __init__(self, name='Client', Circuits = [[]], fitness_goal = np.full((len(ExDict[Ex])), 1)):
        self.name = name
        self.Body_Vec = np.full((len(ExDict[Ex])), 1)
        self.Circuits = Circuits
        self.fitness_goal = fitness_goal

    def Perform_Ckt(self, ckt):
        self.Body_Vec = self.Body_Vec + Circuit_Vector(ckt)
        
    def Clear_History(self):
        self.Body_Vec = np.zeros(len(ExDict[Ex]))

    
    def Recommend_Diverse_Ckt(self):
        Similarities = np.zeros(len(self.Circuits))
        for i,ckt in enumerate(self.Circuits):
            Similarities[i] = cos_vec_sim(Circuit_Vector(ckt), self.Body_Vec)
            
        return self.Circuits[np.argmin(Similarities)]

    def Recommend_Fitness_Goal_Ckt(self):
        
        Similarities = np.zeros(len(self.Circuits)) 
        for i,ckt in enumerate(self.Circuits):
            vec1 = np.add(Circuit_Vector(ckt), self.Body_Vec) 
            Similarities[i] = cos_vec_sim(vec1, self.fitness_goal)
            
        return self.Circuits[np.argmax(Similarities)]
            
            
        
        
         


    
emphasis = [(0,1.5), (1,1.2)]
arm_emphasis = [(18,1.5), (19,1.2)]
emphaCKT = []
Circuits = []
for i in range(len(ExDict[Ex])):
    emphaCKT.append(Generate_Random_Workouts(Exercises, 20, [(i,2)]))

for emph in emphaCKT:
    Circuits = Circuits + emph
    
goal = np.full((len(ExDict[Ex])), 1)

for i in MG[random.randint(0,len(MG)-1)]:
    print(MuscleGroups[i])
    goal[i] *= random.randint(100,2000)/100
    
Cade = Mover(name = 'Cade',Circuits = Circuits,fitness_goal = goal)
John = Mover(name = 'Cade',Circuits = Circuits,fitness_goal = goal)

print('Cade: ',cos_vec_sim(Cade.Body_Vec, Cade.fitness_goal))
print('John: ',cos_vec_sim(John.Body_Vec, John.fitness_goal))


print("################\n")

for i in range(20):
    print(Cade.Recommend_Fitness_Goal_Ckt())
    Cade.Perform_Ckt(Cade.Recommend_Fitness_Goal_Ckt())

    
print('Cade: ',cos_vec_sim(Cade.Body_Vec, Cade.fitness_goal))






