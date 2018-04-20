import codecs
import os
import numpy as np
from ExtractExercises import *
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


def normalize(p):
    p = p/np.sum(p)
##    dif = 1.0 - np.sum(p)
##    p[0] += dif
    return p


def Generate_Circuit(num_exercises, ExList,dist, factor):
    circuit = []
    for i in range(num_exercises):
        #Select Random exercise based on distribution
        dist = normalize(dist)
        choice = np.random.choice(len(UniDist),1, p = dist)[0]
        circuit.append(ExList[choice])
        
        #affect distribution based on selected exercises
        dist[choice] *= factor
 #       dist = normalize(dist)
        
    return circuit




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

df = pd.read_excel('ExLabels.xlsx', sheetname='Sheet1')

X = df.as_matrix()

row1 = df.iloc[1:2,:]

Exercises = list(df['Exercise'])
Group = df[MuscleGroups[1]]
ExDict = {}

for row in X:
    ExDict[row[0]] = row[1:]

J = ExDict[Exercises[0]] * ExDict[Exercises[4]]


Ex = Exercises[1]
Similarity = []

for i,X in enumerate(Exercises):
    Similarity.append(np.sum(ExDict[Ex] * ExDict[Exercises[i]]))

m = min(Similarity)
Min = [i for i, j in enumerate(Similarity) if j == m]



def calculate_circuit_similarity(ckt1, ckt2):
    score = np.zeros(len(ExDict[Ex]))
    for Ex1 in ckt1:
        for Ex2 in ckt2:
            dif = ExDict[Ex1] - ExDict[Ex2]
            score = score + dif
    return score



A = [Exercises[0],Exercises[1],Exercises[2],Exercises[1]]
B = [Exercises[0],Exercises[2],Exercises[2],Exercises[1]]
C = [Exercises[0],Exercises[1],Exercises[2],Exercises[1]]
D = [Exercises[4],Exercises[4],Exercises[4],Exercises[4]]
E = [Exercises[0],Exercises[0],Exercises[0],Exercises[0]]

print(np.sum(calculate_circuit_similarity(A,B)))
print(np.sum(calculate_circuit_similarity(A,C)))

print(np.sum(calculate_circuit_similarity(D,E)))
