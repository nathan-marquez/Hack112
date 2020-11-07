#MAIN APP LOOP
import random
from tkinter import *
#If you have questions, please let me know: jritze@andrew.cmu.edu
phonelist = [['Jenny', 'Unknown', '180-867-5309'],
             ['Santa', 'Claus', '951-262-3062'],
             ['Donald', 'Trump', '202-456-1414'],
             ['Beyonce', 'Knowles', '212-302-8400'],
             ['Oprah', 'Winfrey', '905-866-7874'],
             ['David', 'Kosbie', 'Unknown'],
             ['Farnam', 'Jahanian', '412-268-2200'],
             ['Andrew', 'Carnegie', 'Unavailable']]


def whichSelected():
    print("At {0}".format(select.curselection()))
    return int(select.curselection()[0])


def addEntry():
    phonelist.append([fnamevar.get(), lnamevar.get(), phonevar.get()])
    setSelect()


def updateEntry():
    phonelist[whichSelected()] = [fnamevar.get(),
                                   lnamevar.get(),
                                   phonevar.get()]


def deleteEntry():
    del phonelist[whichSelected()]
    setSelect()


def loadEntry():
    fname, lname, phone = phonelist[whichSelected()]
    fnamevar.set(fname)
    lnamevar.set(lname)
    phonevar.set(phone)


def makeWindow():
    win = Tk()
    buildTextFrame(win)
    buildButtons(win)
    buildScrollingListOfNames(win)
    return win

def buildTextFrame(win):
    global fnamevar, lnamevar, phonevar
    frame1 = Frame(win)
    frame1.pack()
    Label(frame1, text="First Name").grid(row=0, column=0, sticky=W)
    fnamevar = StringVar()
    fname = Entry(frame1, textvariable=fnamevar)
    fname.grid(row=0, column=1, sticky=W)

    Label(frame1, text="Last Name").grid(row=1, column=0, sticky=W)
    lnamevar = StringVar()
    lname = Entry(frame1, textvariable=lnamevar)
    lname.grid(row=1, column=1, sticky=W)

    Label(frame1, text="Phone").grid(row=2, column=0, sticky=W)
    phonevar = StringVar()
    phone = Entry(frame1, textvariable=phonevar)
    phone.grid(row=2, column=1, sticky=W)

def buildButtons(win):
    frame2 = Frame(win)       # Row of buttons
    frame2.pack()
    b1 = Button(frame2, text=" Add  ", command=addEntry)
    b2 = Button(frame2, text="Update", command=updateEntry)
    b3 = Button(frame2, text="Delete", command=deleteEntry)
    b4 = Button(frame2, text="Load  ", command=loadEntry)
    b5 = Button(frame2, text="Refresh", command=setSelect)
    b1.pack(side=LEFT)
    b2.pack(side=LEFT)
    b3.pack(side=LEFT)
    b4.pack(side=LEFT)
    b5.pack(side=LEFT)

def buildScrollingListOfNames(win):
    global select
    frame3 = Frame(win) 
    frame3.pack()
    scroll = Scrollbar(frame3, orient=VERTICAL)
    select = Listbox(frame3, yscrollcommand=scroll.set, height=6)
    scroll.config(command=select.yview)
    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT, fill=BOTH, expand=1)



def setSelect():
    phonelist.sort(key=lambda record: record[1])
    select.delete(0, END)
    for fname, lname, phone in phonelist:
        select.insert(END, "{0}, {1}".format(lname, fname))


win = makeWindow()
setSelect()
win.mainloop()
