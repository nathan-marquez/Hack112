import csv
import pandas as pd
from csv import reader
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import linear_model

def main():
    datafile = open('courseLog.csv', 'r')
    datareader = csv.reader(datafile, delimiter=',')
    courseLog = []
    for row in datareader:
        courseLog.append(row)    

    course0Model = initialTrain(0,courseLog)
    print("initialModelWeight:",course0Model.coef_)


#Helper Function to get training vectors for other functions
def getVector(course,courseLog):
    grade = courseLog[course][5]
    x = [courseLog[course][1:5]]
    y = [grade]
    return x,y

#returns new model from all initial data, only ran at setup
def initialTrain(course,courseLog): 
    x = []
    for row in courseLog:
        current = []
        for col in range(1,len(row)-1):
            current.append(row[col])
        x.append(current)
    y =[]
    for row in courseLog:
        y.append(row[len(row)-1])

    sgd = linear_model.SGDRegressor()
    sgd.fit(x, y)
    return sgd

#destructive, updates model everytime a grade is updated
def updateModel(course, model, courseLog): 
    x,y = getVector(course, courseLog)
    model.partial_fit(x, y)

