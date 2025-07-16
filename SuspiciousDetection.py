
from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from imutils import paths
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import datetime
from tkinter.filedialog import askopenfilename
import cv2 
import shutil
import os
from imageai.Prediction.Custom import CustomImagePrediction
import os
import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()


main = tkinter.Tk()
main.title("Suspicious Activity Detection")
main.geometry("1200x1200")

global filename

execution_path = os.getcwd()
prediction =CustomImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath("model.h5")
prediction.setJsonPath("model_class.json")
prediction.loadModel(num_objects=2)
k=0
def imv(l):
   root = Toplevel(main)
   root.title("Image viewer application using python")
   root.resizable(0, 0)
   # create frame
   frame=Frame(root, width=600, height=500, bg='white', relief=GROOVE, bd=2)
   frame.pack(padx=10, pady=10)
   # create thumbanials of all images
   global images
   images=[]
   for i in l:
      x= Image.open(i)
      x.thumbnail((550, 450))
      x=ImageTk.PhotoImage(x)
      images.append(x) 
# configure the image to the Label in frame  
   
   
   global image_label
   image_label = Label(frame, image=images[k])
   image_label.pack()
   btn1 = Button(root, text="Previous", bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE, command=previous)
   btn1.pack(side=LEFT, padx=60, pady=5)
   btn2 = Button(root, text="Next", width=8, bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE, command=next)
   btn2.pack(side=LEFT, padx=60, pady=5)
   btn3 = Button(root, text="Exit", width=8, bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE, command=root.destroy)
   btn3.pack(side=LEFT, padx=60, pady=5)
   root.mainloop()

def previous():
    global k
    k = k - 1
    try:
        image_label.config(image=images[k])
    except:
        k = 0
        previous()
def next():
    global k
    k = k + 1
    try:
        image_label.config(image=images[k])
    except:
        k = -1
        next()   
def upload():
   global filename
   filename = askopenfilename(initialdir = "videos")
   pathlabel.config(text=filename)

def generateFrame():
   global filename
   text.delete('1.0', END)
   if not os.path.exists('frames'):
      os.mkdir('frames')
   else:
      shutil.rmtree('frames')
      os.mkdir('frames')
   vidObj = cv2.VideoCapture(filename) 
   count = 0
   success = 1
   while success:
      success, image = vidObj.read() 
      if count < 500:
         cv2.imwrite("frames/frame%d.jpg" % count, image)
         text.insert(END,"frames/frame."+str(count)+" saved\n")
         print("frames/frame."+str(count)+" saved")
         #pathlabel.config(text="frames/frame."+str(count)+" saved")
      else:
         break
      count += 1
   pathlabel.config(text="Frame generation process completed. All frames saved inside frame folder")


def detectActivity():
   imagePaths = sorted(list(paths.list_images("frames")))
   count = 0
   option = 0;
   text1.delete('1.0', END)
   l=[]
   for imagePath in imagePaths:
      predictions, probabilities = prediction.predictImage(imagePath, result_count=1)
      
      for eachPrediction, eachProbability in zip(predictions, probabilities):
         if float(eachProbability) > 85:
            count = count + 1;
         if float(eachProbability) < 85:
            count = 0
         if count > 10:
            option = 1
            print(imagePath+" is predicted as "+eachPrediction+" with probability : " +str(eachProbability))
            text1.insert(END,imagePath+" is predicted as "+eachPrediction+" with probability : " +str(eachProbability)+"\n\n")
            count = 0;
            l.append(imagePath)
      print(imagePath+" processed")
   if option == 0:
      text1.insert(END,"No suspicious activity found in given footage") 
   else:  
      imv(l)   
   

font = ('times', 20, 'bold')
title = Label(main, text='Suspicious Activity Detection From CCTV Footage')
title.config(bg='brown', fg='white')  
title.config(font=font)           
title.config(height=3, width=80)       
title.place(x=5,y=5)

font1 = ('times', 14, 'bold')
upload = Button(main, text="Upload CCTV Footage", command=upload)
upload.place(x=50,y=100)
upload.config(font=font1)  

pathlabel = Label(main)
pathlabel.config(bg='brown', fg='white')  
pathlabel.config(font=font1)           
pathlabel.place(x=300,y=100)

depthbutton = Button(main, text="Generate Frames", command=generateFrame)
depthbutton.place(x=50,y=150)
depthbutton.config(font=font1) 

userinterest = Button(main, text="Detect Suspicious Activity Frame", command=detectActivity)
userinterest.place(x=280,y=150)
userinterest.config(font=font1) 

font1 = ('times', 12, 'bold')
text=Text(main,height=25,width=50)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=200)
text.config(font=font1)

text1=Text(main,height=25,width=50)
scroll=Scrollbar(text1)
text1.configure(yscrollcommand=scroll.set)
text1.place(x=550,y=200)
text1.config(font=font1)


main.config(bg='brown')
main.mainloop()

