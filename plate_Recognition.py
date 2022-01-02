import cv2
import datetime
import mysql.connector
from mysql.connector import errorcode
datetime.datetime.now()
datetime.datetime(2009, 1, 6, 15, 8, 24, 78915)
nPlateCascade = cv2.CascadeClassifier("G:\python\Haarcascade.txt")
minArea = 500
cap=cv2.VideoCapture(0)
count = 0

while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = nPlateCascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in numberPlates:
        area = w*h
        if area >minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img,"Number Plate",(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),2)
            imgRoi = img[y:y+h,x:x+w]
            cv2.imshow("ROI", imgRoi)
            
    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('s'):     #pressing s will save the detected number plate
        arriveTime=datetime.datetime.now()
        print(arriveTime)
        dataBase = mysql.connector.connect(
                              host ="localhost",
                              user ="odile",
                              passwd ="password",
                              database="fees_collection"
                                       )
        
   
        mycursor = dataBase.cursor()
        val = arriveTime
        sql = f"INSERT INTO carInfo (arrival_time) VALUES ('{val}')"
        print(sql)
  
        mycursor.execute(sql)
        dataBase.commit()
  
        print(mycursor.rowcount, "details inserted")
        dataBase.close() 

        cv2.imwrite("G:\python\Z Number Plate"+str(count)+".jpg",imgRoi)   #here we have defined where our image will be saved
        cv2.rectangle(img,(0,200),(640,300),(255,0,0),cv2.FILLED)
        cv2.putText(img,"SCAN SAVED",(5,100),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,255),2) #after pressing s this will display SCAN SAVED on screen
        cv2.imshow("FINAL OUTPUT",img)
        cv2.waitKey(30)
        count=count+1

         

                
