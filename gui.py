from tkinter import * 
import tkinter
from pyglet import window
import requests
import json
import time
from PIL import Image, ImageTk
from itertools import count
import webbrowser





face_mask = Tk()
face_mask.title("Face Mask Detection")
face_mask.iconbitmap('face.ico')
face_mask.geometry('1000x510')


img = PhotoImage(file="bg.png")
label = Label(face_mask,image=img)
label.place(x=0, y=0)

def clock():
    t=time.strftime('%I:%M:%S  %p',time.localtime())
    if t!='':
        label1.config(text=t,font='times 15 bold',background="#34282C",foreground="#FFFFFF")
    face_mask.after(100,clock)
label1=Label(face_mask,anchor="e",justify="left")
label1.pack()
label1.place(x=830,y=40)
clock()


def clock1():
    t=time.strftime('%B-%d-%Y',time.localtime())
    if t!='':
        label2.config(text=t,font='times 15 bold',background="#34282C",foreground="#FFFFFF")
    face_mask.after(100,clock1)
label2=Label(face_mask,justify='left')
label2.pack()
label2.place(x=830,y=70)
clock1()

class ImageLabel(tkinter.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[1])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

lbl = ImageLabel(face_mask)
lbl.pack()
lbl.place(x=50,y=40)
lbl.load('glob.gif')
lbl.config(background="black")

lbl1 = ImageLabel(face_mask)
lbl1.pack()
lbl1.place(x=330,y=80)
lbl1.load('face_big.gif')
lbl1.config(background="black")



img2 = PhotoImage(file="peoples.png")
label3 = Label(face_mask,image=img2)
label3.config(background="black")
label3.place(x=685, y=270)




def callback(url):
    webbrowser.open_new(url)
link1 = Label(face_mask)
link1 = Button(face_mask,text="CoWin")
link1.config(font='times 15 bold',background="#000000", foreground="#00ffff")
link1.pack()
link1.place(x=510, y=420)
link1.bind("<Button-1>", lambda e: callback("https://www.cowin.gov.in/"))

button1 = Label(face_mask)
button1 = Button(face_mask,text="Detect Face Mask")
button1.config(font='times 15 bold',background="#000000", foreground="#00ffff")
button1.pack()
button1.place(x=320, y=420)

button2 = Label(face_mask)
button2 = Button(face_mask,text="Exit",command=face_mask.destroy)
button2.config(font='times 15 bold',background="#000000", foreground="#00ffff")
button2.pack()
button2.place(x=600, y=420)



face_mask.resizable(0,0)
face_mask.mainloop()