import cv2
import sqlite3
import numpy as np

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(1);
sampleNum = 0

def insertOrUpdate(Id,Name):
        conn=sqlite3.connect("facedb.db")
        cmd="SELECT * FROM People WHERE ID="+str(Id)
        cursor=conn.execute(cmd)
        isRecordExist=0
        for row in cursor:
                isRecordExist=1
        if(isRecordExist==1):
                cmd="UPDATE People SET Name="+str(Name)+" WHERE ID="+str(Id)
        else:
                cmd="INSERT INTO People(ID,Name) VALUES("+str(Id)+","+str(Name)+")"
        conn.execute(cmd)
        conn.commit()
        conn.close()

id=raw_input('Enter user id')
name=raw_input('Enter name')
insertOrUpdate(id,name)
sampleNum=0;

while(True):
        ret,img=cam.read();
        if ret is True:
                gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        else:
                continue
        faces=faceDetect.detectMultiScale(gray,1.3,5);
        for(x,y,w,h) in faces:
                sampleNum=sampleNum+1;
                cv2.imwrite("dataSet/User."+str(id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                cv2.waitKey(100);
        cv2.imshow("Face",img);
        cv2.waitKey(1);
        if(sampleNum>40):
                break
cam.release()
cv2.destroyAllWindows()
