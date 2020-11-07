import csv
import pandas as pd
from csv import reader
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import linear_model
import joblib 

#this is a test main method
def main():
    datafile = open('courseLog.csv', 'r')
    datareader = csv.reader(datafile, delimiter=',')
    courseLog = []
    for row in datareader:
        courseLog.append(row)    

    course0Model = initialTrain(0,courseLog)
    print(getWeights(course0Model))
    print('saving model')
    saveModel(course0Model, "course0Model")
    course0Model = getModel("course0Model")
    courseLog[0][5] = .7
    courseLog[0][2] = .5
    updateModel(0, course0Model, courseLog)
    print(getWeights(course0Model))
    print('saving model')
    saveModel(course0Model, "course0Model")

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

def getWeights(model):
    return model.coef_

def getModel(modelName):
    return joblib.load(modelName)

def saveModel(model, modelName):
    # Save the model as a pickle in a file 
    joblib.dump(model, modelName) 
  

