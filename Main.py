#Fix up the color and use better lighting. 

import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow("TrackBar")
cv2.createTrackbar("LowerHue","TrackBar",52, 180, nothing)
cv2.createTrackbar("LowerSaturation","TrackBar",142, 255, nothing)
cv2.createTrackbar("LowerValue","TrackBar",156, 255, nothing)
cv2.createTrackbar("UpperHue","TrackBar", 180 , 180, nothing)
cv2.createTrackbar("UpperSaturation","TrackBar",255 , 255 , nothing)
cv2.createTrackbar("UpperValue","TrackBar",255 , 255, nothing)

font = cv2.FONT_HERSHEY_COMPLEX


while True: 
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lh = cv2.getTrackbarPos("LowerHue","TrackBar")
    ls = cv2.getTrackbarPos("LowerSaturation","TrackBar")
    lv = cv2.getTrackbarPos("LowerValue","TrackBar")
    uh = cv2.getTrackbarPos("UpperHue","TrackBar")
    us = cv2.getTrackbarPos("UpperSaturation","TrackBar")
    uv= cv2.getTrackbarPos("UpperValue","TrackBar")
    

    lower_red = np.array([lh,ls,lv]) #Hue,Saturation,Value
    upper_red = np.array([uh,us,uv])
    mask = cv2.inRange(hsv,lower_red,upper_red)
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode(mask, kernel)


    countours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in countours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt,True),True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if area > 400:
            cv2.drawContours(frame, [approx], 0,(0,0,0),5)

            if len(approx) ==3:
                cv2.putText(frame, "Triangle", (x,y), font, 1, (0,0,0))
            elif len(approx) == 4:
                cv2.putText(frame, "Rectangle", (x,y), font, 1, (0,0,0))
            elif 10 < len(approx) < 20:
                cv2.putText(frame, "Circle", (x,y), font, 1, (0,0,) )         


       



    cv2.imshow("Frame",frame)
    cv2.imshow("Mask",mask)

    key = cv2.waitKey(1)
    if key == 's': #change 
        break 


cap.release() 
cv2.destroyAllWindows()