# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 11:49:22 2016

@author: gcarrillo
"""
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import numpy as np
blank_image = np.ones((6002,9002), np.uint8)


c=0

x1=-1
x2=-1
y1=-1
y2=-1
prev_x=-1
prev_y=-1
tiempo_inicial=-1
tiempo_final=-1
with open("/home/gcarrillo/Documentos/MCC/tesis/multimodal/2016-08-25/notas201608250917.txt", "r") as ins:
#with open("/home/gcarrillo/Documentos/MCC/tesis/multimodal/2016-08-09/notas201608081641.txt", "r") as ins:    
        total_trazos = 0
        trazo_realizado = 0    
        total_puntos = 0
        puntos = []
        tiempos = []
#with open("notas_test.txt", "r") as ins:
 
        for line in ins:
            c = c+1
            if (c>1):
                
                print line
                x,y,p,t,tm = line.split(",")
                coord_x = int(x)+1;
                coord_y = int(y)+1;
                print "==="
    
                if (int(p)>0):
                    if (tiempo_inicial<0):
                        tiempo_inicial = (int(t) *1000) + int(tm)
                    else:
                        tiempo_final =  (int(t) *1000) + int(tm)
                    trazo_realizado = 1
                    total_puntos = total_puntos +1
                    if (x1==-1 and y1==-1):
                        x1=coord_x
                        y1=coord_y
                    else:
                        x1=prev_x
                        y1=prev_y                
                        x2=coord_x
                        y2=coord_y
                        
                    prev_x=coord_x
                    prev_y=coord_y
            
                    blank_image[coord_y,coord_x]=255
                    #dibujar la linea
#                    if (y1>0 and x1>0 and x2>0 and y2>0):
                    if (y1>-1 and x1>-1 and x2>-1 and y2>-1):                        
                        cv2.line(blank_image,(x1,y1),(x2,y2),(255,0,0),5)                
                else:
                    x1=-1
                    x2=-1
                    y1=-1
                    y2=-1
                    prev_x=-1
                    prev_y=-1
                    if (trazo_realizado>0): 
                        trazo_realizado = 0
                        total_trazos = total_trazos +1
                        #agregar la cantidad de puntos a la lista
                        if (total_puntos>3):
                            puntos.append(total_puntos)
                            tiempos.append(tiempo_final - tiempo_inicial)
                        total_puntos = 0
                        tiempo_inicial=-1
                        tiempo_final=-1
                

img_escala = cv2.resize(blank_image,(int(0.95*9002), int(0.95*6002)), interpolation = cv2.INTER_CUBIC)
img_escala1=img_escala
np.bitwise_not(img_escala,img_escala1)                         
cv2.imwrite('salida.png',img_escala1)    
print total_trazos
print puntos
print sum(puntos)/float(len(puntos))
print tiempos
print sum(tiempos)/float(len(tiempos))