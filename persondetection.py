import cv2
import numpy as np
from PIL import Image
import os
from os import listdir
import os.path
from random import randint, randrange
import random, string
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
import keyboard
import shutil

##FOR TKINTER
##FRAME
##ADD IMAGE TO FRAME
##BUTTON.PLACE x+y
##CLICK SETS VAR TO MATCHING INDEX
##DESTROY FRAME

path = '/home/zeus/Documents/fromssd/testphotos/'
whT = 320
confThreshold = 0.5
nmsThreshold = 0.3

classesFile = 'coco.names'
classNames = []
with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfiguration = 'yolov3.cfg'
modelWeights = 'yolov3.weights'
#modelOnnx = 'tinyyolov2-7.onnx'


net = cv2.dnn.readNetFromDarknet(modelConfiguration,modelWeights)
#net = cv2.dnn.readNetFromONNX(modelOnnx)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObjects(outputs, img, fname):
    dimensions = img.shape
    print(dimensions)
    imcopy = img.copy()
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            ##check only for person class name
            name = (classNames[classId])
            if confidence > confThreshold and name == 'person':
                w,h = int(det[2]*wT), int(det[3]*hT)
                x,y = int((det[0]*wT)-w/2), int((det[1]*hT)-h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))
    #print(len(bbox))

    indices = cv2.dnn.NMSBoxes(bbox,confs,confThreshold,nmsThreshold)

    count = 0
    filterlist = []
    for i in indices:
        count += 1
        box = bbox[i]
        filterlist.append(box)
        pad = 135
        x,y,w,h = box[0], box[1], box[2], box[3]
        #x,y,w,h = x-pad + (pad//2), y-pad + (pad//2), w+pad, h+pad
        randcolor = randint(1, 255)
        cv2.rectangle(img,(x,y),(x+w,y+h),(randcolor,0,255),4)

        #cv2.putText(img,str(w) + "x" + str(h) + " - " + "INDEX: " + str(count) + " - " + f'{classNames[classIds[i] ].upper()} {int(confs[i]*100)}%',
        #((x+w//2),(y+h//2)),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),6)
        #cv2.putText(img,str(w) + "x" + str(h) + " - " + "INDEX: " + str(count) + " - " + f'{classNames[classIds[i] ].upper()} {int(confs[i]*100)}%',
        #((x+w//2),(y+h//2)),cv2.FONT_HERSHEY_SIMPLEX, 1,(randcolor,0,255),2)

        cv2.putText(img, str(count),
        ((x+w//2),(y+h//2)),cv2.FONT_HERSHEY_SIMPLEX, (w//70),(255,255,255),20)
        cv2.putText(img, str(count),
        ((x+w//2),(y+h//2)),cv2.FONT_HERSHEY_SIMPLEX, (w//70),(randcolor,0,255),5)

    count = 0
    for i in filterlist:
        count +=1
        print(count)
        print(i)

    resizepercentX = dimensions[1] // 1280
    resizepercentY = dimensions[0] // 720 

    #imS = cv2.resize(img, (dimensions[1]*resizepercentX, (dimensions[0]*resizepercentY)))
    #cv2.waitKey(1)
    repeat = False
    if len(filterlist) > 1:

        print(resizepercentX)
        print(resizepercentY)

        imS = cv2.resize(img, (dimensions[1]//resizepercentY, (dimensions[0]//resizepercentY)))
        newd = imS.shape
        print(newd)
        print("CALLED")

        ##This fixes drawing bug in dwm/xorg
        for f in range(3):
            cv2.imshow(str(fname), imS)
            cv2.waitKey(1)
            cv2.moveWindow(str(fname),1900,0)
            #if cv2.waitKey(0) == ord('1'):

        while True:
            try:
                index = cv2.waitKey(0)
                #if 1-9, select index
                if int(index) in range(49,58):
                    index = chr(index)
                    print(index)
                    break
                #if 'm' move to review for manual cropping
                elif int(index) == 109:
                    shutil.move(str(path+fname),str(path+"review/"+fname))
                    print(index)
                    break
                #if 's' skip
                elif int(index) == 115:
                    print(index)
                    break
                else:
                    print(index)
                    print('loop')
            except Exception as e:
                print(e)
                #print("EXCEPTION")

        #index = input("NUMBER: ")
        #print(filterlist[int(index)-1])
        cv2.destroyWindow(fname)
    elif len(filterlist) == 0:
        shutil.move(str(path+fname),str(path+"review/"+fname))
    else:
        index = 1


    #if index in ["m", "M"]:
        #print("MARKED FOR REVIEW")
        #print("SRCPATH: " + str(path+fname))
        #print("DSTPATH: " + str(path+"review/"+fname))
        #shutil.move(str(path+fname),str(path+"review/"+fname))
        #cv2.destroyWindow(fname)
        #findObjects(outputs,img, fname)
    #if index in ["s", "S"]:
        #print("HISSS")
        #cv2.destroyWindow(fname)

############
    ##Crop block
    pad = 130
    x, y, w, h = filterlist[int(index)-1][0],filterlist[int(index)-1][1],filterlist[int(index)-1][2],filterlist[int(index)-1][3]
    x, y, w, h = (x-pad + (pad//2)), (y-pad + (pad//2)), (w + pad), (h + pad) 
    if y < 0:
        print("LESSTHANZERO")
        y = 0
    if x < 0:
        x = 0
    if y > dimensions[0]:
        y = dimensions[0] - h
    if x > dimensions[1]:
        x = dimensions[1] - w

    im1 = imcopy[y:y+h, x:x+w]

#############

    randstring = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8)) + ".jpg"
    for f in listdir(path + "outputs/"):
        while randstring == f:
            print("MATCH!")
            #generate new
            randstring = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))+ ".jpg"


    split_tup = os.path.splitext(fname)
    print(split_tup)
    
    # extract the file name and extension
    file_name = split_tup[0]
    file_extension = split_tup[1]

    suffixname = (file_name + "_out" + file_extension)
    try:
        cv2.imwrite(os.path.join(path + "outputs/", suffixname), im1)
    except:
        print("errornaming")
    #cv2.imwrite(randstring, im1)
    #cv2.imwrite(os.path.join(path + "outputs/", randstring), im1)  
    cv2.destroyWindow(fname)

for f in listdir(path):
    print(f)


for f in listdir(path):
    try:
        print("FILENAME")
        print(f)
        img = cv2.imread(path + f) 
        #success, img = cap 
        #success, img  = cap.read()

        blob = cv2.dnn.blobFromImage(img, 1/255,(whT,whT),[0,0,0],1,crop=False)
        net.setInput(blob)

        layerNames = net.getLayerNames()
        outputNames = [layerNames[i-1] for i in net.getUnconnectedOutLayers()]
        #print(outputNames)

        outputs = net.forward(outputNames)
        #print(len(outputs))

        findObjects(outputs,img, f)

        #cv2.imshow('Image', img)
        cv2.imwrite('imagetest.jpg', img)
        cv2.waitKey(1)
    except:
        "ERROR"
        continue
