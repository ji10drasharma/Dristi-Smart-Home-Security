import cv2
import os
import sys
from facialRecognition import trainer
import psycopg2
import webbrowser



from flask import jsonify

def dataSetCreator_func(noOfSamples):
    
    if not os.path.exists('../facialRecognition/trainer'):
        os.makedirs('../facialRecognition/trainer')

    if not os.path.exists('../facialRecognition/dataSet'):
        os.makedirs('../facialRecognition/dataSet')    

    try:
        conn=psycopg2.connect(database="dristidb", user="postgres", password="admin", port=5432, host='localhost')
        print("connected")
    except:
        print("unable to connect")   

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM userlist")
    last=cursor.fetchall()
    last.sort()
    Id=last.pop()[0]

    avatarcopied=False
    source="../facialRecognition/dataSet/user."+str(Id)+".1.jpg"
    destination="../node/public/img/avatar."+str(Id)+".jpg"
    avatarindb="/img/avatar."+str(Id)+".jpg"
    cursor.execute("UPDATE userlist SET avatarimg=(%s) WHERE id = (%s)", [avatarindb,Id]);
    conn.commit()
    cursor.close()
    conn.close()
        
    cam = cv2.VideoCapture(0)
    faceDetector = cv2.CascadeClassifier("../facialRecognition/haarcascade_frontalface_default.xml")
    
    sampleNum = 0
    # Id = id

    while(True):
        ret, image = cam.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face = faceDetector.detectMultiScale(gray, 1.3, 5)
        for(x,y,w,h) in face:
            sampleNum += 1
            cv2.imwrite("../facialRecognition/dataSet/user."+str(Id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
            if(avatarcopied==False):
                #shutil.copy(source,destination)
                cv2.imwrite(destination,image)
                avatarcopied==True
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.waitKey(200)

      
        cv2.imshow("show", image)
        cv2.waitKey(1)  
        if(sampleNum >= noOfSamples):
            break    
    cam.release()
    cv2.destroyAllWindows()
    trainer.trainer_func() 
     