# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 14:35:13 2016

@author: gcarrillo
"""
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import numpy as np
import cv2
import re

#import subprocess
#subprocess.call(["ls", "-l", "/etc/resolv.conf"])
outfile = open("result.txt", 'w')
import os
os.system('ffmpeg -i videoprueba.mp4 -acodec copy -f segment -segment_time 60 -vcodec copy -reset_timestamps 1 -map 0 out/fff%d.mp4 -an')
fgbg = cv2.createBackgroundSubtractorMOG2(500,16,False)
start_path = 'out' # current directory
mov_am = {}
for path,dirs,files in os.walk(start_path):
    for filename in files:
        if filename.endswith(".mp4"):
            file_path = os.path.join(start_path,filename)
            
            filenumber = re.findall('\d+', filename)
            minuto = int(filenumber[0]) + 1
            
            #leer el archivo

            cap = cv2.VideoCapture(file_path)
            frame_counter = 0
            #cap = cv2.VideoCapture('/home/gcarrillo/Documentos/MCC/tesis/multimodal/2016-08-25/fff4.mp4')
            #fgbg = cv2.createBackgroundSubtractorMOG2()
            total_motion = 0
            while(1):
                ret, frame = cap.read()
                frame_counter += 1
                fgmask = fgbg.apply(frame)
                #if (fgmask.shape) :
                if hasattr(fgmask, 'shape'):
                    h, w = fgmask.shape
                    motion = np.sum(np.where(fgmask == 255,1,0))
                    motion /= float(h*w)
                    total_motion += motion
                    
                if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    break
                
            #guardar el total de movimiento en ese minuto
            
            mov_am[minuto]=total_motion
            #outfile.write(str(minuto)+","+total_motion+"\n")
            #print total_motion
            
#print mov_am            
for k, v in mov_am.items():
    line = '{}, {}'.format(k, v) 
    print line
    outfile.write(line+"\n")
    #print(line, file=outfile)        
outfile.close()




#for minu in mov_am:
    #print minu, 'corresponds to', mov_am[minu]
 #   outfile.write(str(minu)+","+mov_am[minu]+"\n")
#outfile.write("\n".join(mov_am))

          
#            #[int(s) for s in filename.split() if s.isdigit()]
#cap = cv2.VideoCapture('/home/gcarrillo/Documentos/MCC/tesis/multimodal/2016-08-25/fff4.mp4')
#cont = 0
#nframe = 0
#seg = 0
##cap = cv2.VideoCapture('/home/gcarrillo/Documentos/MCC/tesis/multimodal/2016-08-25/fff4.mp4')
##fgbg = cv2.createBackgroundSubtractorMOG2()
#fgbg = cv2.createBackgroundSubtractorMOG2(500,16,False)
#while(1):
#    ret, frame = cap.read()
#    cont = cont + 1
#    nframe = nframe + 1
#    if nframe >= 30 :
#        seg = seg + 1
#        nframe = 0
#    fgmask = fgbg.apply(frame)
#    h, w = fgmask.shape
#    motion = np.sum(np.where(fgmask == 255,1,0))
#    motion /= float(h*w)
#    print seg
#    print motion
#    
#    cv2.imshow('frame',fgmask)
#    k = cv2.waitKey(30) & 0xff
#    if k == 27:
#        break
#
#cap.release()
#cv2.destroyAllWindows()
