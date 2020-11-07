#MAIN APP LOOP
import random
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from dataclasses import make_dataclass

#making user dataclass
User = make_dataclass('User', [('style', list), ('courses', list)])
user = User([], []) # style is formatted [Auditory#, Visual#, Tacticle#]


LARGEFONT =("Verdana", 35)

#multiple page implementation from https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/ 
class tkinterApp(tk.Tk): 
      
    # __init__ function for class tkinterApp  
    def __init__(self, *args, **kwargs):  
          
        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs) 
        self.geometry("300x410")
        # creating a container 
        container = tk.Frame(self)   
        container.pack(side = "top", fill = "both", expand = True) 
   
        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) 
   
        # initializing frames to an empty array 
        self.frames = {}   
   
        # iterating through a tuple consisting 
        # of the different page layouts 
        for F in (StartPage, analyticsPage, mainPage, gradesPage): 
   
            frame = F(container, self) 
   
            # initializing frame of that object from 
            # startpage, page1, page2 respectively with  
            # for loop 
            self.frames[F] = frame  
   
            frame.grid(row = 0, column = 0, sticky ="nsew") 
   
        self.show_frame(StartPage) 
   
    # to display the current frame passed as 
    # parameter 
    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.tkraise() 

def whichSelectedCourseBox():
    print("At {0}".format(coursesBox.curselection()))
    try:
        return int(coursesBox.curselection()[0])
    except:
        return 0

def addCourseEntry():
    user.courses.append([coursevar.get()])
    setSelectCourses()

def updateEntry():
    phonelist[whichSelected()] = [fnamevar.get(),
                                   lnamevar.get(),
                                   phonevar.get()]

def deleteCourseEntry():
    del user.courses[whichSelectedCourseBox()]
    setSelectCourses()

def loadEntry():
    fname, lname, phone = phonelist[whichSelectedCourseBox()]
    fnamevar.set(fname)
    lnamevar.set(lname)
    phonevar.set(phone)

def buildStartPage(frame1):
    global coursevar, coursesBox, scaleT, scaleV, scaleA
    courseFrame = Frame(frame1)
    courseFrame.grid(row = 1, column = 0)
    Label(courseFrame, text="Course: ").pack(side=LEFT)
    coursevar = StringVar()
    course = Entry(courseFrame, textvariable=coursevar)
    course.pack(side=LEFT)

    #Buttons in btnFrame
    btnFrame = Frame(frame1)
    btnFrame.grid(row=2, column=0)
    bt1 = Button(btnFrame, text='Add Course', command=addCourseEntry)
    bt1.pack(side=LEFT)
    bt2 = Button(btnFrame, text='Delete Course', command=deleteCourseEntry)
    bt2.pack(side=LEFT)

    #Scroll box with currently added courses
    scrollFrame = Frame(frame1)
    scrollFrame.grid(row = 3, column = 0)
    scroll = Scrollbar(scrollFrame, orient=VERTICAL)
    coursesBox = Listbox(scrollFrame, yscrollcommand=scroll.set, height=6)
    scroll.config(command=coursesBox.yview)
    scroll.pack(side=RIGHT, fill=Y)
    coursesBox.pack(side=LEFT, fill=BOTH, expand=1)

    #Learning Type Scales
    scaleFrame = Frame(frame1)
    scaleFrame.grid(row = 4, column = 0, pady=10)
    scaleT = ttk.Scale(scaleFrame, from_=0, to=10, orient=HORIZONTAL)
    scaleT.grid(row= 1, column=1)
    scaleA = ttk.Scale(scaleFrame, from_=0, to=10, orient=HORIZONTAL)
    scaleA.grid(row= 2, column=1)
    scaleV = ttk.Scale(scaleFrame, from_=0, to=10, orient=HORIZONTAL)
    scaleV.grid(row= 3, column=1)

    #Scale labels
    Label(scaleFrame, text='Choose Your Learning Style Preferences').grid(row = 0, column = 1)
    Label(scaleFrame, text='Tacticle').grid(row = 1, column=0)
    Label(scaleFrame, text='Auditory').grid(row = 2, column=0)
    Label(scaleFrame, text='Visual').grid(row = 3, column=0)

    #update Scale button
    AVTbtn = ttk.Button(scaleFrame, text='Update', command=lambda : slide(scaleFrame))
    AVTbtn.grid(row = 4, column = 0)


def slide(scaleFrame):
    user.style = [int(scaleA.get()), int(scaleV.get()), int(scaleT.get())]
    l1 = Label(scaleFrame, text=f'A-V-T Rating: {user.style[0]}-{user.style[1]}-{user.style[2]}')
    l1.grid(row = 4, column=1)

def buildButtons(win):
    # Row of buttons
    frame2 = Frame(win)
    b1 = ttk.Button(frame2, text=" Add  ", command=addEntry)
    b2 = ttk.Button(frame2, text="Update", command=updateEntry)
    b3 = ttk.Button(frame2, text="Delete", command=deleteEntry)
    b4 = ttk.Button(frame2, text="Load  ", command=loadEntry)
    b5 = ttk.Button(frame2, text="Refresh", command=setSelect)
    b1.grid(row = 2, column = 1, padx = 10, pady = 10) 

def buildScrollingListOfNames(win):
    global select
    frame3 = Frame(win)
    frame3.grid(row = 3, column = 1)
    scroll = Scrollbar(frame3, orient=VERTICAL)
    select = Listbox(frame3, yscrollcommand=scroll.set, height=6)
    scroll.config(command=select.yview)
    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT, fill=BOTH, expand=1)

def setSelectCourses():
    user.courses.sort(key=lambda record: record)
    coursesBox.delete(0, END)
    for course in user.courses:
        coursesBox.insert(END, "{0}".format(course))

def startCheck(controller):
    if len(user.courses) == 0:
        messagebox.showinfo('Course Box Error', 'Please enter at least 1 course!')
    elif len(user.style) == 0:
        messagebox.showinfo('Learning Style Error', 'Please update your learning style!')
    else:
        controller.show_frame(mainPage)

# first window frame startpage 
   
class StartPage(tk.Frame): 
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent) 
          
        # label of frame Layout 2 
        label = ttk.Label(self, text ="Start", font = LARGEFONT) 
          
        # putting the grid in its place by using 
        # grid 
        label.grid(row = 0, column = 0, padx = 10, pady = 10)  
   
        ## button to change page
        button2 = ttk.Button(self, text ="Done", command = lambda : startCheck(controller))  
      
        # putting the button in its place by 
        # using grid 
        button2.grid(row = 5, column = 0, padx = 10, pady = 10) 
        buildStartPage(self) 
           
# second window frame mainPage 
class mainPage(tk.Frame): 
      
    def __init__(self, parent, controller): 
          
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text ="Main Page", font = LARGEFONT) 
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 
   
        # button to show frame 2 with text 
        # layout2 
        button1 = ttk.Button(self, text ="StartPage", 
                            command = lambda : controller.show_frame(StartPage)) 
      
        # putting the button in its place  
        # by using grid 
        button1.grid(row = 1, column = 1, padx = 10, pady = 10) 
   
        # button to show frame 2 with text 
        # layout2 
        button2 = ttk.Button(self, text ="Analytics Page", 
                            command = lambda : controller.show_frame(analyticsPage)) 
      
        # putting the button in its place by  
        # using grid 
        button2.grid(row = 2, column = 1, padx = 10, pady = 10) 


        # button to show frame 2 with text 
        # layout2 
        button3 = ttk.Button(self, text ="Update Grades", 
                            command = lambda : controller.show_frame(gradesPage)) 
      
        # putting the button in its place by  
        # using grid 
        button3.grid(row = 2, column = 2, padx = 10, pady = 10) 
   
# third window frame analytics
class analyticsPage(tk.Frame):  
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text ="Analytics", font = LARGEFONT) 
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 
   
        # button to show frame 2 with text 
        # layout2 
        button1 = ttk.Button(self, text ="Done", 
                            command = lambda : controller.show_frame(mainPage)) 
      
        # putting the button in its place by  
        # using grid 
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
      
        # putting the button in its place by 
        # using grid 
        button1.grid(row = 2, column = 1, padx = 10, pady = 10) 

#main loop driver
app = tkinterApp()
app.mainloop()
