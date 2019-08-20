import cv2
import time
import pygame
import RPi.GPIO as GPIO
import time

class CameraInst():
        # Constructor...
        def __init__(self):
                fps        = 20.0               # Frames per second...
                resolution = (640, 480)         # Frame size/resolution...
                w = 640
                h = 480
 
                self.cap = cv2.VideoCapture(0)  # Capture Video...
                print("Camera warming up ...")
                time.sleep(1)
 
                # Define the codec and create VideoWriter object
                fourcc = cv2.VideoWriter_fourcc(*"H264")     # You also can use (*'XVID')
                self.out = cv2.VideoWriter('output.avi',fourcc, fps, (w, h))
 
        def captureVideo(self):
                # Capture
                self.ret, self.frame = self.cap.read()
                # Image manipulations come here...
                self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                #cv2.imshow('frame',self.gray)
                return self.frame
 
        def saveVideo(self):
                # Write the frame
                self.out.write(self.frame)
 
        def __del__(self):
                self.cap.release()
                cv2.destroyAllWindows()
                print("Camera disabled and all output windows closed...")
 
def detect():
        font = cv2.FONT_HERSHEY_SIMPLEX
        cam1 = CameraInst()
        stair =cv2.CascadeClassifier("/home/pi/resources/stair.xml")
        car = cv2.CascadeClassifier("/home/pi/resources/sideview_cascade_classifier.xml")
        face_casecade = cv2.CascadeClassifier('/home/pi/resources/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('/home/pi/resources/haarcascade_eye.xml')
        #cap = cv2.VideoCapture("/home/pi/resources/cars2.mp4")
        while(True):
                frame = cam1.captureVideo()    # Live stream of video on screen...
                #ret,frame = cap.read()
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                stairs = stair.detectMultiScale(gray,1.3,5)
                cars = car.detectMultiScale(gray,1.3,5)
                faces = face_casecade.detectMultiScale(gray,1.3,5)
                for (x,y,w,h) in cars:
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                        cv2.putText(frame,'car_detected',(x,y),font,1,(0,255,130),2,cv2.LINE_AA)
                for (x,y,w,h) in stairs:
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                        cv2.putText(frame,'stair_detected',(x,y),font,1,(0,255,130),2,cv2.LINE_AA)

                cv2.imshow('cap',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        cap.release()
        cv2.destroyAllWindows()
        cleanUp()
if __name__ == '__main__':
        detect()