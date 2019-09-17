# Face Recognition

#### Face recognition consists of three parts:
- data collection;
- machine learning;
- face recognition.

## Data collection
The data collection phase is used to create a data set that is structured in parallel. Without a well-structured dataset, the quality of recognition will be worse as the machine learns from the created dataset. Thus, this step is crucial for successful work.
The script works as an automatic program for taking photos. It starts the camera, determines if a face is found in the camera stream, and, if so, saves the image to disk at the same time.
The script uses the OpenCV face detection algorithm using the default classifier, which is a given OpenCV dataset with thousands of faces. It is used to detect the face of an image, in this example it is a frame from a video stream.

When you need photos of the homeowner or proxies, a face-to-face script is executed. At run time, you need to specify the ID of the Id used to index the person from whom the images were taken. If this is the second person to be added to the system, an ID with number 2 must be provided. The results shown will start with an unconfigured system, so "1" will be entered.

<img src="https://raw.githubusercontent.com/SomethingFromNothing/face_recognition/master/images/2.png" width="550">

If Id 1 requests, the camera will start. Now you need to point the camera at the owner's face. The script will only be shot when the face is recognized. To improve the quality of machine learning and recognition, it is recommended to tilt the head in different directions so that the face shots can be taken from different angles.
As soon as 100 pictures are taken, the script will be released and the camera will be stopped. Looking at the dataSet folder on the Raspberry Pi, you can now find 100 images that were taken from the script.

<img src="https://raw.githubusercontent.com/SomethingFromNothing/face_recognition/master/images/1.png" width="550">




## Machine learning
At the machine learning stage, a training file is created that contains LBPH face information. Based on this file, the algorithm at the recognition stage will decide whether or not the person is in the video stream. The images have to be converted to uint8 and all added to a single face recognition array to create a training file, so careful pre-processing is required.

## Face recognition
Generally, the script first detects faces from the video stream just like a dataset generator script. When a face is detected, it will compare it to a trained set of data created using the previous scenario. The OpenCV algorithm will then give you a level of confidence as to how well it recognizes your face. Based on the confidence level, a rectangle with the name of the recognized face will be drawn on the frame.
The script imports the necessary libraries, this time OpenCV and OS access libraries. In the initialization phase, the first two different OpenCV objects are created. One is again a detector that uses a default cascade file to detect faces, the other is an empty LBPH face recognition object to which training data from previous ones will be submitted. 
