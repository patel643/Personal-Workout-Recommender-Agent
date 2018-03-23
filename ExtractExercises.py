import codecs
import os


Exercises = {}
path = "(00)finished"
for filename in os.listdir(path):
    
    file = path + "/" + filename #.replace(" ","\ ")

    Workout = codecs.open(file,encoding='utf-8',mode='r').read()
    Workout = Workout.replace('}','')
    ID = Workout.split('\n')[0]
    Circuits = Workout.split('{')
    for circuit in Circuits:
        items = circuit.split('\n')
        reps = items[0]
        for index in range(1,len(items)-1):
            temp = items[index].split(' ')
            if len(temp) > 1:
                reps = temp[0]
                exercise = ' '.join(temp[1:])
                exercise = exercise.lower()
                if exercise in Exercises:
                    Exercises[exercise].append(reps)
                else:
                    Exercises[exercise] = [reps]

            else:
                continue

