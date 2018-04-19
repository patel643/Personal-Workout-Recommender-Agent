import codecs
import os
import numpy as np
from ExtractExercises import *



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



Exercises = ExtractExercises()

ExerciseSet = sorted(list(Exercises.keys()))

UniDist = np.full(len(ExerciseSet),1/(len(ExerciseSet)))

TargetAreas = ['Legs', 'Arms', 'Chest', 'Abs', 'Back']
InitialDist = np.full(len(TargetAreas), 1/(len(TargetAreas)))

#UniDist = normalize(UniDist)
#choice = np.random.choice(len(UniDist),1, p = UniDist)[0]

for i in range(10):
    ckt = Generate_Circuit(100,ExerciseSet,UniDist, i)
##    print(len(set(ckt))/len(ckt))
##    print(len(set(ckt))/len(ckt))

