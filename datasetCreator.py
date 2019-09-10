# Import OpenCV2 for image processing
import cv2
import numpy as np
# Start capturing video
cam = cv2.VideoCapture(0)
# Detect object in video stream using Haarcascade Frontal Face
detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# For each person, one face id
faceId=input('enter your id')
# Initialize sample face image
sampleNum=0
# Start looping
while(True):
    # Capture video frame
    _, img = cam.read()
    # Convert frame to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect frames of different sizes, list of faces rectangles
    faces = detector.detectMultiScale(gray, 1.3, 5)
    # Loops for each faces
    for (x,y,w,h) in faces:        
        #incrementing sample number 
        sampleNum=sampleNum+1        
        #saving the captured face in the dataset folder
        cv2.imwrite("dataSet/User."+faceId +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
        # Crop the image frame into rectangle
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        # Display the video frame, with bounded rectangle on the person's face
        cv2.imshow('frame',img)       
    # To stop taking video, press 'q' for at least 100ms
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break   
    # If image taken reach 100, stop taking video
    elif sampleNum>200:
        break
print("\n successfull generation, exiting.")
# Stop video
cam.release()
# Close all started windows
cv2.destroyAllWindows()
