from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import linear_model

def main():
            #test log
            #Course HW Notes Zoom Read | Grade    
    courseLog = [['15112',.02,.90,.04,.60,.10],
                ['21241',.20,.30,.40,.10,.50],
                ['07128',.10,.20,.50,.20,.60],
                ['15150',.30,.30,.30,.10,.40],
                ['21242',.90,.10,.70,.30,.80],
                ['08781',.70,.30,.20,.10,.30]]

    course0Model = initialTrain(0, courseLog)
    print("initialModelWeight:",course0Model.coef_)
    courseLog[0][2] = .7 
    courseLog[0][3] = .3
    courseLog[0][5] = .72
    updateModel(0,courseLog,course0Model)
    print(course0Model.coef_)
    courseLog[0][2] = .8 
    courseLog[0][3] = .1
    courseLog[0][5] = .82
    updateModel(0,courseLog,course0Model)
    print(course0Model.coef_)

def getVector(course, courseLog):
    grade = courseLog[course][5]
    x = [courseLog[course][1:5]]
    y = [grade]
    return x,y

def initialTrain(course, courseLog): #returns new model from all initial data
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

def updateModel(course,courseLog, model): #destructive, updates model
    x,y = getVector(course, courseLog)
    model.partial_fit(x, y)

