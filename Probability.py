import codecs
import os
import numpy as np
from ExtractExercises import *

Exercises = ExtractExercises()

ExerciseSet = sorted(list(Exercises.keys()))

UniDist = np.full(len(ExerciseSet),1/(len(ExerciseSet)))

choice = np.random.choice(len(UniDist),1, p = UniDist)[0]

for i,ex in enumerate(Exercises):
    if "push" in ex:
        UniDist[i]*=5

def normalize(p):
    p = p/np.sum(p)
    return p
