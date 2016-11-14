# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 11:21:32 2016

@author: gcarrillo
"""


# coding: utf-8

# In[1]:
import collections
import time 
import requests

import operator


# Display images within Jupyter
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2


# In[3]:

_url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
_key = 'c0958b1e63134377960c2796e82aa14e'
_maxNumRetries = 10


# In[4]:

def processRequest( json, data, headers ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = None )

        if response.status_code == 429: 

            print "Message: %s" % ( response.json()['error']['message'] )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print 'Error: failed after retrying!'
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print "Error code: %d" % ( response.status_code )
            print "Message: %s" % ( response.json()['error']['message'] )

        break
        
    return result


# In[5]:

def renderResultOnImage( result, img ):
    
    """Display the obtained results onto the input image"""
    
    for currFace in result:
        faceRectangle = currFace['faceRectangle']
        cv2.rectangle( img,(faceRectangle['left'],faceRectangle['top']),
                           (faceRectangle['left']+faceRectangle['width'], faceRectangle['top'] + faceRectangle['height']),
                       color = (255,0,0), thickness = 5 )


    for currFace in result:
        faceRectangle = currFace['faceRectangle']
        currEmotion = max(currFace['scores'].iteritems(), key=operator.itemgetter(1))[0]


        textToWrite = "%s" % ( currEmotion )
        cv2.putText( img, textToWrite, (faceRectangle['left'],faceRectangle['top']-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1 )


# In[12]:
#
#pathToFileInDisk = r'/Users/xavierochoa/Downloads/cara.png'
#with open( pathToFileInDisk, 'rb' ) as f:
#    data = f.read()
#
#headers = dict()
#headers['Ocp-Apim-Subscription-Key'] = _key
#headers['Content-Type'] = 'application/octet-stream'
#
#json = None
#
#result = processRequest( json, data, headers )
#
#for currFace in result:
#        faceRectangle = currFace['faceRectangle']
#        currEmotion = max(currFace['scores'].iteritems(), key=operator.itemgetter(1))[0]
#        print currEmotion
#
#
#
## Load the original image from disk
#data8uint = np.fromstring( data, np.uint8 ) # Convert string to an unsigned int array
#img = cv2.cvtColor( cv2.imdecode( data8uint, cv2.IMREAD_COLOR ), cv2.COLOR_BGR2RGB )
#
#renderResultOnImage( result, img )
#
#ig, ax = plt.subplots(figsize=(15, 20))
#ax.imshow( img )


# In[38]:



#cap = cv2.VideoCapture('/Users/xavierochoa/Downloads/VideoHB.mp4')
cap = cv2.VideoCapture('/home/gcarrillo/Documentos/MCC/tesis/multimodal/2016-08-25/fff4.mp4')
#cap = cv2.VideoCapture('/home/gcarrillo/Documentos/MCC/tesis/multimodal/2016-08-09/fff0.mp4')
    

for x in range(0, 100):
    framenumber=x*100
    print framenumber
    cap.set(cv2.CAP_PROP_FPS,framenumber)
    ret, frame = cap.read()
    
    #sub_frame = frame[150:400, 200:540] #video2
    sub_frame = frame[120:450, 200:640]
    #sub_frame = frame
    filename = "video1frame" + `framenumber` +".png"
    cv2.imwrite(filename,sub_frame)


# In[40]:
print "segundo lazo"
for x in range(0, 100):
    framenumber=x*100
    filename = "video1frame" + `framenumber` +".png"
    print framenumber
    pathToFileInDisk = filename
    with open( pathToFileInDisk, 'rb' ) as f:
        data = f.read()

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/octet-stream'

    json = None

    result = processRequest( json, data, headers )
    print result
#    for currFace in result:
#        faceRectangle = currFace['faceRectangle']
#        currEmotion = max(currFace['scores'].iteritems(), key=operator.itemgetter(1))[0]
#        #print currEmotion


#
    # Load the original image from disk
    #data8uint = np.fromstring( data, np.uint8 ) # Convert string to an unsigned int array
    #img = cv2.cvtColor( cv2.imdecode( data8uint, cv2.IMREAD_COLOR ), cv2.COLOR_BGR2RGB )
    img = cv2.imread(pathToFileInDisk)    


    if isinstance(result, collections.Iterable):
        # iterable
        renderResultOnImage( result, img )
    else:
    # not iterable    
        print "no results"

    #ig, ax = plt.subplots(figsize=(15, 20))
    #ax.imshow( img )
    cv2.imshow('imagen',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# In[ ]:



