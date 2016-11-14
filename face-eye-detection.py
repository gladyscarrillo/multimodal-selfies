# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 20:57:19 2016

@author: gcarrillo
"""
import numpy as np
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

faceDet = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_profileface.xml')
#faceDet1 = cv2.CascadeClassifier("/usr/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml")
#faceDet2 = cv2.CascadeClassifier("/usr/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
#faceDet3 = cv2.CascadeClassifier("/usr/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml")
#faceDet4 = cv2.CascadeClassifier("/usr/share/OpenCV/haarcascades/haarcascade_frontalface_alt_tree.xml")
#


#face_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')
face_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_profileface.xml')

#eye_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_eye.xml')
eye_cascader = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_righteye_2splits.xml')
eye_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_lefteye_2splits.xml')

#cap = cv2.VideoCapture("/home/gcarrillo/Documentos/MCC/tesis/multimodal/2016-08-09/output201608081641.mkv")
#cap = cv2.VideoCapture("/home/gcarrillo/Documentos/MCC/tesis/multimodal/2016-08-09/output_menor.mkv")
cap = cv2.VideoCapture("/home/gcarrillo/Documentos/MCC/tesis/multimodal/2016-08-25/output201608250917.mkv")
min_size = (30, 30)

flags = cv2.CASCADE_SCALE_IMAGE
count = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    
    frame = cv2.resize(frame,(640, 480), interpolation = cv2.INTER_CUBIC)
           
    #cv2.imshow('window-name',frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Detect face using 4 different classifiers
    face = faceDet.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
    #face1 = faceDet1.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
#    face2 = faceDet2.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
#    face3 = faceDet3.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
#    face4 = faceDet4.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

    #Go over detected faces, stop at first detected face, return empty if no face.
    if len(face) == 1:
        faces = face
#    elif len(face1) == 1:
#        faces == face1        
#    elif len(face2) == 1:
#        faces == face2
#    elif len(face3) == 1:
#        faces = face3
#    elif len(face4) == 1:
#        faces = face4
    else:
        faces = ""
            
    
    #faces = face_cascade.detectMultiScale(gray, 1.1, 3,minSize = min_size, flags = flags)
    for (x,y,w,h) in faces:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        cv2.imshow('roi',roi_gray)
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            
        eyesr = eye_cascader.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyesr:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)            
    
    cv2.imshow('img',frame)
   
    
    #cv2.imwrite("frames/frame%d.jpg" % count, frame)
    count = count + 1
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


cap.release()
cap.destroyAllWindows()
