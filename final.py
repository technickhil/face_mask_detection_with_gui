from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
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

button2 = Label(face_mask)
button2 = Button(face_mask,text="Exit",command=face_mask.destroy)
button2.config(font='times 15 bold',background="#000000", foreground="#00ffff")
button2.pack()
button2.place(x=600, y=420)

face_mask.geometry('1000x510')

def detect_and_predict_mask(frame, faceNet, maskNet):
	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()
	print(detections.shape)

	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the detection
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > 0.5:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# ensure the bounding boxes fall within the dimensions of
			# the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

			# add the face and bounding boxes to their respective
			# lists
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		# for faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions
		# in the above `for` loop
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)
# remove if not useful
def call_me():
# load our serialized face detector model from disk
	prototxtPath = r"face_detector\deploy.prototxt"
	weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
	faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
	maskNet = load_model("mask_detector.model")

# initialize the video stream
	print("[INFO] starting video stream...")
	vs = VideoStream(src="http://192.168.43.160:8080/video").start()

# loop over the frames from the video stream
	while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=1000)

	# detect faces in the frame and determine if they are wearing a
	# face mask or not
		(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

	# loop over the detected face locations and their corresponding
	# locations
		for (box, pred) in zip(locs, preds):
		# unpack the bounding box and predictions
			(startX, startY, endX, endY) = box
			(mask, withoutMask) = pred

		# determine the class label and color we'll use to draw
		# the bounding box and text
		label = "Mask" if mask > withoutMask else "No Mask"
		label1 = "Now You Can Enter" if mask > withoutMask else "Sorry You are Restricted"
		color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
		color2 = (0, 255, 0) if label1 == "Now You Can Enter" else (0, 0, 255)

		# include the probability in the label
		label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

		# display the label and bounding box rectangle on the output
		# frame
		cv2.putText(frame, label, (startX, startY - 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

		cv2.putText(frame, label1, (startX , startY - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, color2, 2)
		cv2.rectangle(frame, (startX, startY), (endX, endY), color2, 2)

	# show the output frame
		cv2.imshow("Detect Face Mask", frame)
		key = cv2.waitKey(10) & 0xFF

	# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

button1 = Label(face_mask)
button1 = Button(face_mask,text="Detect Face Mask",command= call_me)
button1.config(font='times 15 bold',background="#000000", foreground="#00ffff")
button1.pack()
button1.place(x=320, y=420)	

face_mask.resizable(0,0)
face_mask.mainloop()
