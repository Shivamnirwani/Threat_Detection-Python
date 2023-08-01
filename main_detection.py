import cv2
from djitellopy import tello
import cvzone
import numpy as np
import winsound
thres = 0.6
nmsthre = 0.2
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
classNames = []
classfiles = 'detect.names'
with open(classfiles, 'rt') as f:
    classNames = f.read().split('\n')
#print(classNames)
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
while True:
    success, img = cap.read()
    ok, frame = cap.read()
    frame = cv2.resize(frame, (1000, 600))
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nmsthre)
    blur = cv2.GaussianBlur(frame, (15, 15), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype='uint8')
    upper = np.array(upper, dtype='uint8')
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(frame, hsv, mask=mask)
    number_of_total = cv2.countNonZero(mask)

    try:
        for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
            if classNames[classId - 1] == 'lion':
                cvzone.cornerRect(img, box, rt=0)
                cv2.putText(img, f'{classNames[classId - 1].upper()}{round(conf * 100, 2)}',
                            (box[0], box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
                winsound.Beep(2500, 1000)
                print(classNames[classId-1])
            elif int(number_of_total) > 15000:
                print("fire detected")
                cvzone.cornerRect(img, box, rt=0)
                winsound.Beep(2500, 1000)

            else:
                cvzone.cornerRect(img, box, rt=0)
                cv2.putText(img, f'{classNames[classId - 1].upper()}{round(conf * 100, 2)}',
                            (box[0], box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
    except:
        pass
    cv2.imshow("image", img)
    cv2.waitKey(1)
cv2.destroyAllWindows()
video.release()