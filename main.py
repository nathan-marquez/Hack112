#MAIN APP LOOP
import random
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from dataclasses import make_dataclass
import pickle, time, csv

#importing ML
from ml import *

#import csv read
from input2CSV import *

#making user dataclass
User = make_dataclass('User', [('style', tuple), ('courses', list)])
testcourses = [('15112', 50), ('21127', 75), ('32141',60)]
teststyle = (3,7,9)
user = User(teststyle, testcourses) # style is formatted (Auditory#, Visual#, Tacticle#)
courseLog = []
#four categories of sessions
types = ['HW','Reading','Note-Taking','Zoom']

#nasty globals
status = 'Waiting to Start'

#setup for appearances
LARGEFONT =("Verdana", 35)

def updateLocalCourseLog(courseLog):
    datafile = open('courseLog.csv', 'r')
    datareader = csv.reader(datafile, delimiter=',')
    courseLog = []
    for row in datareader:
        courseLog.append(row) 

#multiple page implementation from https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/ 
class tkinterApp(tk.Tk): 
      
    # __init__ function for class tkinterApp  
    def __init__(self, *args, **kwargs):  
        #create initial courseLog
        updateLocalCourseLog(courseLog)

        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs) 
        # self.geometry("300x410")
        # creating a container 
        container = tk.Frame(self)   
        container.pack(side = "top", fill = "both", expand = True) 
   
        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) 
   
        # initializing frames to an empty dictionary
        self.frames = {}   
   
        # iterating through a tuple consisting 
        # of the different page layouts 
        for F in (StartPage, analyticsPage, mainPage, gradesPage, sessionPage): 
   
            frame = F(container, self) 
   
            # initializing frame of that object from 
            # startpage, page1, page2 respectively with  
            # for loop 
            self.frames[F] = frame  
   
            frame.grid(row = 0, column = 0, sticky ="nsew") 
   
        self.show_frame(mainPage) 
   
    # to display the current frame passed as 
    # parameter 
    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.tkraise() 

# first window frame startpage 
class StartPage(tk.Frame): 
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent) 
        self.controller = controller

        # label of frame Layout 2 
        label = ttk.Label(self, text ="Start", font = LARGEFONT) 
        label.grid(row = 0, column = 0, padx = 10, pady = 10)  

        # button to change page and initialize user input
        button2 = ttk.Button(self, text ="Done", command = self.done)  
        button2.grid(row = 5, column = 0, padx = 10, pady = 10) 

        courseFrame = Frame(self)
        courseFrame.grid(row = 1, column = 0)
        Label(courseFrame, text="Course/Grade: ").pack(side=LEFT)
        self.coursevar = StringVar()
        self.gradevar = StringVar()
        course = Entry(courseFrame, textvariable=self.coursevar)
        course.pack(side=LEFT)
        grade = Entry(courseFrame, textvariable=self.gradevar, width=2)
        grade.pack(side=LEFT)

        #Buttons in btnFrame
        btnFrame = Frame(self)
        btnFrame.grid(row=2, column=0)
        bt1 = Button(btnFrame, text='Add Course', command=self.addCourseEntry)
        bt1.pack(side=LEFT)
        bt2 = Button(btnFrame, text='Delete Course', command=self.deleteCourseEntry)
        bt2.pack(side=LEFT)

        #Scroll box with currently added courses
        scrollFrame = Frame(self)
        scrollFrame.grid(row = 3, column = 0)
        scroll = Scrollbar(scrollFrame, orient=VERTICAL)
        self.coursesBox = Listbox(scrollFrame, yscrollcommand=scroll.set, height=6)
        scroll.config(command=self.coursesBox.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.coursesBox.pack(side=LEFT, fill=BOTH, expand=1)

        #Learning Type Scales
        self.scaleFrame = Frame(self)
        self.scaleFrame.grid(row = 4, column = 0, pady=10)
        self.scaleT = ttk.Scale(self.scaleFrame, from_=0, to=10, orient=HORIZONTAL)
        self.scaleT.grid(row= 1, column=1)
        self.scaleA = ttk.Scale(self.scaleFrame, from_=0, to=10, orient=HORIZONTAL)
        self.scaleA.grid(row= 2, column=1)
        self.scaleV = ttk.Scale(self.scaleFrame, from_=0, to=10, orient=HORIZONTAL)
        self.scaleV.grid(row= 3, column=1)

        #Scale labels
        Label(self.scaleFrame, text='Choose Your Learning Style Preferences').grid(row = 0, column = 1)
        Label(self.scaleFrame, text='Tacticle').grid(row = 1, column=0)
        Label(self.scaleFrame, text='Auditory').grid(row = 2, column=0)
        Label(self.scaleFrame, text='Visual').grid(row = 3, column=0)

        #update Scale button
        AVTbtn = ttk.Button(self.scaleFrame, text='Update', command=self.slide)
        AVTbtn.grid(row = 4, column = 0)
        
    def startCheck(self):
        if len(user.courses) == 0:
            messagebox.showinfo('Course Box Error', 'Please enter at least 1 course!')
        elif len(user.style) == 0:
            messagebox.showinfo('Learning Style Error', 'Please update your learning style!')
        else:
            return True

    #update user style list based on slide position
    def slide(self):
        user.style = (int(self.scaleA.get()), int(self.scaleV.get()), int(self.scaleT.get()))
        l1 = Label(self.scaleFrame, text=f'A-V-T Rating: {user.style[0]}-{user.style[1]}-{user.style[2]}')
        l1.grid(row = 4, column=1)

    def initData(self):
        user.courses 
    
    def done(self):
        if self.startCheck() == True:
            self.controller.show_frame(mainPage)
            self.initializeCourseLogs()
    
    #return dictionary
    def initializeCourseLogs(self): #inputs are ints 0 - 100
        A, V, T = user.style
        #assigning corellation weights to each learning style and activity
        hw = .5*(A) + .5*(T)
        zoom = .5*(A) + .5*(V)
        notes = .5*(V) + .5*(T)
        reading = V
        d = dict()
        for course, grade in user.courses:
            d[course] = [[hw,1],[zoom,1],[notes,1],[reading,1], grade]
        
        #writing the dict to courseLog.csv
        writeCSV(d)

    #Course Selection Helpers
    def setSelectCourses(self):
        self.coursesBox.delete(0, END)
        print(user.courses)
        for course, grade in user.courses:
            self.coursesBox.insert(END, course)

    def deleteCourseEntry(self):
        del user.courses[self.whichSelectedCourseBox()]
        self.setSelectCourses()

    def whichSelectedCourseBox(self):
        print("At {0}".format(self.coursesBox.curselection()))
        try:
            return int(self.coursesBox.curselection()[0])
        except:
            return 0

    def addCourseEntry(self):
        course = self.coursevar.get()
        grade = self.gradevar.get()
        if (grade == '') or (course == ''):
            messagebox.showerror('Course Entry Error', 'Please enter course and grade!')
        else:
            user.courses.append((course, grade))
            self.setSelectCourses()

#END startPage



# second window frame mainPage 
class mainPage(tk.Frame): 
      
    def __init__(self, parent, controller): 
          
        tk.Frame.__init__(self, parent) 
   
        # button to show start page
        button1 = ttk.Button(self, text ="StartPage", 
                            command = lambda : controller.show_frame(StartPage)) 
        button1.grid(row = 1, column = 1, padx = 10, pady = 10) 
   
        # button to show analytics page with text 
        button2 = ttk.Button(self, text ="View Analytics", 
                            command = lambda : controller.show_frame(analyticsPage)) 
        button2.grid(row = 2, column = 1, padx = 10, pady = 10) 

        # button to show grades page  
        button3 = ttk.Button(self, text ="Update Grades", 
                            command = lambda : controller.show_frame(gradesPage)) 
        button3.grid(row = 3, column = 1, padx = 10, pady = 10) 


        button4 = ttk.Button(self, text ="Start Session", 
                            command = lambda: controller.show_frame(sessionPage)) 
        button4.grid(row = 4, column = 1, padx = 10, pady = 10) 
   
# third window frame analytics
class analyticsPage(tk.Frame):  
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text ="Analytics", font = LARGEFONT) 
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 
   
        # button to show main page
        button1 = ttk.Button(self, text ="Done", 
                            command = lambda : controller.show_frame(mainPage)) 
        button1.grid(row = 1, column = 1, padx = 10, pady = 10) 
   
        # buildButtons(self)
        # buildScrollingListOfNames(self)


# fourth window frame updateGrades
class gradesPage(tk.Frame):  
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text ="Page 2", font = LARGEFONT) 
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 
   
        # button to show frame 3 with text 
        # layout3 
        button1 = ttk.Button(self, text ="Done", 
                            command = lambda : controller.show_frame(mainPage)) 
        button1.grid(row = 2, column = 1, padx = 10, pady = 10) 

class sessionPage(tk.Frame):  
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text ="Press Begin to Start a Session") 
        label.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.controller = controller
        self.recording = False
        global statusL 

        #Select Course and Session Type Drop down menu
        dropFrame = Frame(self)
        dropFrame.grid(row = 1, column = 1)
        label = ttk.Label(self, text ="Make Selections") 
        label.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.course = StringVar()
        self.Type = StringVar()
        courseMenu = OptionMenu(dropFrame, self.course, *user.courses).grid(row=0, column=1)
        typeMenu = OptionMenu(dropFrame, self.Type, *types).grid(row=1, column=1)
        #TODO fix first item in list not appearing in drop down menu
        label1 = ttk.Label(dropFrame, text ="Course").grid(row=0, column=0) 
        label2 = ttk.Label(dropFrame, text ="Session Type").grid(row=1, column=0) 

        #In Session status label
        statusL = ttk.Label(self, text=status, relief=SUNKEN, anchor=W)
        statusL.grid(row=8, columnspan = 2, sticky=W+E)

        #TEMPORARY user input focus
        self.focusVar = StringVar()
        focusEntry = Entry(self, textvariable=self.focusVar)
        focusEntry.grid(row=3, column=1)

        btnFrame = Frame(self)
        btnFrame.grid(row=2, column=0)
        # button to begin session
        button2 = ttk.Button(btnFrame, text ="Begin", 
                            command = self.startSession) 
        button2.pack(side=LEFT) 
        # button to end session appears
        button3 = ttk.Button(btnFrame, text ="Stop", 
                        command = self.endSession) 
        button3.pack(side=LEFT) 

        # button to show main page
        button1 = ttk.Button(btnFrame, text ="Done", 
                            command = self.quit) 
        button1.pack(side=LEFT)

    #start eyegaze routine, 
    def startSession(self):
        #start eyegaze
        self.recording = True
        self.startTime = time.time()
        status = "In Session"
        statusL = ttk.Label(self, text=status, relief=SUNKEN, anchor=W)
        statusL.grid(row=8, columnspan = 2, sticky=W+E)

    def endSession(self):
        #get focus from eyegaze and update the model data
        #focus = getFocus()
        #only update model if time elapsed is greater than 5min
        endTime = time.time()
        if (endTime - self.startTime > 5) and (self.recording):
            self.recording = False
            self.updateData()
            print('Session Completed!')
            status = "Session Recorded"
            statusL = ttk.Label(self, text=status, relief=SUNKEN, anchor=W)
            statusL.grid(row=8, columnspan = 2, sticky=W+E)
        else:
            messagebox.showinfo("Session Error", 'Please allow mininum session time (5min) to elapse!')
        print(self.focusVar.get())

    def updateData(self):
        #take in course, type(int corresponding to column), focus
        data = readCSV()
        typeIndex = types.index(self.course)
        data[course][typeIndex][0] += focus
        data[course][typeIndex][1] += 1
        writeCSV(data)

    def quit(self):
        self.refresh()
        self.controller.show_frame(mainPage)
    
    def refresh(self):
        self.focusVar = ''

#main loop driver
app = tkinterApp()
app.mainloop()
