import telebot;

import email, smtplib, ssl
import time
import datetime

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

token = 'you token'
bot = telebot.TeleBot(token);
chat_id = ##

def telegramsendEmailf():
    
    global path
    photo = open(path, 'rb')
    #photo = open('photo.jpg', 'rb')
    bot.send_photo(chat_id, photo, caption = "GOOD") #send_media_group

def telegramsendEmailn():
         
    global path
    photo = open(path, 'rb')
    #photo = open('photo.jpg', 'rb')
    bot.send_photo(chat_id, photo, caption = "WARNING!")

sender_email = "sender email"      
receiver_email = "receiver email"
password = "pass"

messagef = MIMEMultipart()  # create message with found person
messagen = MIMEMultipart()  # create message with not found person

path = ".."                #global patch
countPhotof = 0;            # photo FOUND counter (5 photo for message)
countPhoton = 0;            # photo NOT found counter (5 photo for message)
messageSend = False;        #wait N fraimes between photo
framecounter = 0;           #counter for frames
framesWaited = False;       #wait first 3 frames
facedetectcounter = 0       #wait first 3 frames

def foundsendEmail():      #function send message for Found face

    global messagef
    subject = "GOOD"
    body = "WELCOME HOME"

    # Create a multipart message and set headers
    
    messagef["From"] = sender_email
    messagef["To"] = receiver_email
    messagef["Subject"] = subject

    # Add body to email
    messagef.attach(MIMEText(body))  
    
    global path
    filephoto = path # In same directory as script
    print(filephoto)
    # Open PDF file in binary mode
    with open(filephoto, "rb") as attachment:
                       
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            "attachment; filename= " + filephoto,
        )

        # Add attachment to message and convert message to string
        
        messagef.attach(part)
        text = messagef.as_string()

        global countPhotof              #global
        countPhotof+=1                  #increment
        if(countPhotof == 5):           #if = 5 send message
            
            # Log in to server using secure context and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, text)

                    countPhotof = 0                 #obnulim 
                    global messageSend              #global
                    messageSend = True              #pause between detection
                    messagef = MIMEMultipart()
                    messagef["From"] = sender_email
                    messagef["To"] = receiver_email
                    messagef["Subject"] = subject
                    messagef.attach(MIMEText(body))


def notfoundsendEmail():          #function send message for NOT found face

    global messagen
    subject = "WARNING"
    body = "NOT FOUND FACE"

    # Create a multipart message and set headers
    
    messagen["From"] = sender_email
    messagen["To"] = receiver_email
    messagen["Subject"] = subject

    # Add body to email
    messagen.attach(MIMEText(body))   
    
    global path
    filephoto = path # In same directory as script
    print(filephoto)
    # Open PDF file in binary mode
    with open(filephoto, "rb") as attachment:
                       
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            "attachment; filename= " + filephoto,
        )

        # Add attachment to message and convert message to string
        
        messagen.attach(part)
        text = messagen.as_string()

        global countPhoton           
        countPhoton+=1
        if(countPhoton == 5):
            # Log in to server using secure context and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, text)

                    countPhoton = 0
                    global messageSend
                    messageSend = True
                    messagen = MIMEMultipart()
                    messagen["From"] = sender_email
                    messagen["To"] = receiver_email
                    messagen["Subject"] = subject
                    messagen.attach(MIMEText(body))

# Import OpenCV2 for image processing
import cv2

# Import numpy for matrices calculations
import numpy as np

import os 

# Create Local Binary Patterns Histograms for face recognization
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load the trained mode
recognizer.read('trainer/trainer.yml')

# Load prebuilt model for Frontal Face
cascadePath = "haarcascade_frontalface_default.xml"

# Create classifier from prebuilt model
faceCascade = cv2.CascadeClassifier(cascadePath);

# Set the font style
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize and start the video frame capture
cam = cv2.VideoCapture(0)

cam.set(3,640)
cam.set(4,480)

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

# Loop
while True:
    # Read the video frame
    ret, im = cam.read()

    # Convert the captured frame into grayscale
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    if not messageSend:     #pause between face detection
        
        # Get all face from the video frame
        faces = faceCascade.detectMultiScale(gray, 1.2,5,minSize=(int(minW),int(minH)))

        # For each face in faces
        for(x,y,w,h) in faces:

            # Create rectangle around the face
            cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)

            # Recognize the face belongs to which ID
            Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            
            if framesWaited:     #waiting first 3 frames
                
                # Check the ID if exist
                if(confidence < 65):    #shans oshibki, 0 = best tochnost
                    if(Id == 1):
                        Id = "first"
                        path = "found/User." + Id + datetime.datetime.today().strftime("_%Y-%m-%d_(%H:%M:%S)") + ".jpg" #patch to file
                        cv2.imwrite(path, gray[y:y+h,x:x+w])    #write image to path
                        
                        foundsendEmail()    #function for Found face
                        telegramsendEmailf()
                    
                    if(Id == 2):
                        
                        Id = "second"
                        path = "found/User." + Id + datetime.datetime.today().strftime("_%Y-%m-%d_(%H:%M:%S)") + ".jpg"
                        cv2.imwrite(path, gray[y:y+h,x:x+w]) #write image to path
                        
                        foundsendEmail()    #function for Found face
                        
                                               
                    if(Id == 3):                     
                        Id = "third"
                        path = "found/User." + Id + datetime.datetime.today().strftime("_%Y-%m-%d_(%H:%M:%S)") + ".jpg"
                        cv2.imwrite(path, gray[y:y+h,x:x+w])  #write image to path
            
                        foundsendEmail()    #function for Found face
                else:
                    Id = "Unknown {0:.2f}%".format(round(100 - confidence, 2))
                    Id = "Unknown"
                    path = "notFound/User." + Id + datetime.datetime.today().strftime("_%Y-%m-%d_(%H:%M:%S)") + ".jpg"
                    cv2.imwrite(path, gray[y:y+h,x:x+w])  #write image to path
                    notfoundsendEmail()     #function for NOT Found face
                    telegramsendEmailn()
                    framesWaited = False    #wait 3 frames


                # Put text describe who is in the picture
                cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
                cv2.putText(im, str(Id), (x,y-40), font, 1, (255,255,255), 3)
                
            else:
                if facedetectcounter == 3:     #frames counter
                    framesWaited = True
                    acedetectcounter = 0
                else:
                    facedetectcounter += 1      #increment
                            
    else:
        if framecounter==100:           #frames between face detection
            messageSend = False         # start next detection
            framecounter = 0            #obnulim
        else:
            framecounter+=1             #increment
            print(framecounter)         #print

    # Display the video frame with the bounded rectangle
    cv2.imshow('im',im) 

    # If 'q' is pressed, close program
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

#cleanup
print("\n Exiting program on user command")
    
# Stop the camera
cam.release()

# Close all windows
cv2.destroyAllWindows()
