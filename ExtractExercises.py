import codecs
import os
import numpy as np
import re

def ExtractExercises():
    Exercises = {}
    path = "(00)finished"
    for filename in os.listdir(path):
        #Read in Each Workout File
        file = path + "/" + filename #.replace(" ","\ ")
        Workout = codecs.open(file,encoding='utf-8',mode='r').read()

        
        #Separate Workout into Circuits
        Workout = Workout.replace('}','')
        ID = Workout.split('\n')[0]
        Circuits = Workout.split('{')
        
        for circuit in Circuits:
            #Separate by lines
            items = circuit.split('\n')
            
            
            for index in range(1,len(items)-1):
                #Separate by spaces
                temp = items[index].split(' ')
                if len(temp) > 1:
                    reps = temp[0]                  #First spaces is reps
                    exercise = ' '.join(temp[1:])   #merge all words
                    exercise = exercise.lower()     #lowercase
                    exercise = exercise.strip()     #remove whitespace
                    if exercise in Exercises:
                        Exercises[exercise].append(reps)
                    else:
                        Exercises[exercise] = [reps]

                else:
                    continue
    return Exercises



