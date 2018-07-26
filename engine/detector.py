import cv2
import sqlite3
import numpy as np

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(1);
rec=cv2.createLBPHFaceRecognizer();
rec.load("recognizer\\trainingData.yml")
font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,2,1,0,1)

def getProfile(id):
    conn=sqlite3.connect("Face.db")
    cmd="SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    return profile

while(True):
    ret,img=cam.read();
    if ret is True:
		
    	    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY);
    else:
	    continue
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,100),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        print id
        profile=getProfile(id)
        if(profile!=None):
            cv2.cv.PutText(cv2.cv.fromarray(img),"Name:"+str(profile[1]),(x,y+h+30),font,(100,255,0))
            cv2.cv.PutText(cv2.cv.fromarray(img),"Age:"+str(profile[2]),(x,y+h+60),font,(100,255,0))
            
    cv2.imshow("Face",img);
    if(cv2.waitKey(1)==ord('q')):
        break;
cam.release()
cv2.destroyAllWindows()
    
