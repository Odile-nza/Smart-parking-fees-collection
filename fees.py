from PIL.Image import ImageTransformHandler
import cv2
import numpy as np
import pytesseract
import datetime
import time
from datetime import  timedelta
import mysql.connector

dep=int(datetime.datetime.utcnow().timestamp())


datetime.datetime.now()
datetime.datetime(2009, 1, 6, 15, 8, 24, 78915)

pytesseract.pytesseract.tesseract_cmd="C:/Program Files/Tesseract-OCR/tesseract.exe"

cascade= cv2.CascadeClassifier("haarcascade.xml")
def extract_num(img_filename):
    img=cv2.imread(img_filename)
    #Img To Gray
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    nplate=cascade.detectMultiScale(gray,1.1,4)
    #crop portion
    for (x,y,w,h) in nplate:
        wT,hT,cT=img.shape
        a,b=(int(0.02*wT),int(0.02*hT))
        plate=img[y+a:y+h-a,x+b:x+w-b,:]
        #make the img more darker to identify LPR
        kernel=np.ones((1,1),np.uint8)
        plate=cv2.dilate(plate,kernel,iterations=1)
        plate=cv2.erode(plate,kernel,iterations=1)
        plate_gray=cv2.cvtColor(plate,cv2.COLOR_BGR2GRAY)
        (thresh,plate)=cv2.threshold(plate_gray,130,255,cv2.THRESH_BINARY)
        #read the text on the plate
        read=pytesseract.image_to_string(plate,config='--psm 11')
        print(read)
        departureTime=datetime.datetime.now()
        print(departureTime)
        
        dataBase = mysql.connector.connect(
                              host ="localhost",
                              user ="odile",
                              passwd ="password",
                              database="fees_collection"
                                       )
        
        val1 = departureTime
        val3=read
        sql_Query = "select arrive_time from carInfo where  plate_number=%s"
        plate_number = (val3,)
        cursor = dataBase.cursor()
        cursor.execute(sql_Query, plate_number)
        record = cursor.fetchone()
        time=record[0]
        print(record)
        minutes_diff = (departureTime - time).total_seconds() / 60.0
        print(minutes_diff)
        price=minutes_diff*(16.6)
        val2=price
        print(price)
        cursor.execute("UPDATE carInfo SET departure_time=%s,parking_fees=%s WHERE plate_number=%s",(val1,val2,val3))
        dataBase.commit()
  
        #print(mycursor.fetchone(), "details inserted")
        dataBase.close() 


        read=''.join(e for e in read if e.isalnum())
        stat=read[0:2]
        print(stat)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.rectangle(img,(x-10,y-50),(x+w+1,y),(255,0,0),-1)
        cv2.putText(img,"Number Plate",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2)
        
        cv2.imshow("plate",plate)
        
    cv2.imwrite("Result.png",img)
    cv2.imshow("Result",img)
    if cv2.waitKey(0)==113:
        exit()
    cv2.destroyAllWindows()

extract_num("car9.jpg")
