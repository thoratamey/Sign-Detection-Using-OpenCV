# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 11:36:37 2020

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 11:35:17 2020

@author: User
"""
import cv2
import numpy as np
import math
import pyttsx3


engine = pyttsx3.init()

cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(0)
while 1:
    # read image
    ret, img = cap.read()
    
    val=(300,300)
    val1=(100,100)

    # get hand data from the rectangle sub window on the screen
    cv2.rectangle(img, val, val1, (0,255,0),0)
    crop_img = img[100:300, 100:300]
     
    cv2.rectangle(img, (500,300), (300,100), (0,255,0),0)
    crop_img1 = img[100:300, 300:500]

    # convert to grayscale
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    grey1= cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)

    # applying gaussian blur
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)
    blurred1 = cv2.GaussianBlur(grey1, value, 0)
    
    # thresholdin: Otsu's Binarization method
    ret, thresh1 = cv2.threshold(blurred, 127, 255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    ret1, thresh2 = cv2.threshold(blurred1, 127, 255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # show thresholded image
    cv2.imshow('Thresholded', thresh1)
    cv2.imshow('Thresholded2',thresh2)

    # check OpenCV version to avoid unpacking error
    contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    max_area = -1
    for i in range(len(contours)):
       cnt=contours[i]
       area = cv2.contourArea(cnt)
       if(area>max_area):
            max_area=area
            cl=i
            
    contours1, hierarchy1 = cv2.findContours(thresh2.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    max_area1 = -1
    for l in range(len(contours1)):
        cnt1=contours1[l]
        area1 = cv2.contourArea(cnt1)
        if(area1>max_area1):
            max_area1=area1
            cl1=l       
        

    # find contour with max area
    cnt = contours[cl]
    cnt1 = contours1[cl1]
    
    # create bounding rectangle around the contour (can skip below two lines)
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0, 255), 0)
    cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0, 255), 0)
    
    x1, y1, w1, h1 = cv2.boundingRect(cnt1)
    cv2.rectangle(crop_img1, (x1, y1), (x1+w1, y1+h1), (0, 0, 255), 0)
    cv2.rectangle(crop_img1, (x1, y1), (x1+w1, y1+h1), (0, 0, 255), 0)
    
    # finding convex hull
    hull = cv2.convexHull(cnt)
    hull1 = cv2.convexHull(cnt1)
    
    # drawing contours
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing, [hull], 0,(0, 0, 255), 0)
    
    drawing1 = np.zeros(crop_img1.shape,np.uint8)
    cv2.drawContours(drawing1, [cnt1], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing1, [hull1], 0,(0, 0, 255), 0)

     #finding convex hull
    hull = cv2.convexHull(cnt, returnPoints=False)
    hull1 = cv2.convexHull(cnt1, returnPoints=False)

    # finding convexity defects
    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

    defects1 = cv2.convexityDefects(cnt1, hull1)
    count_defects1 = 0
    cv2.drawContours(thresh2, contours1, -1, (0, 255, 0), 3)
    
    # applying Cosine Rule to find angle for all defects (between fingers)
    # with angle > 90 degrees and ignore defects
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]

        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        
        # find length of all sides of triangle
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        
        # apply cosine rule here
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        
          #ignore angles > 90 and highlight rest with red dots
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img, far, 1, [0,0,255], -1)
        #dist = cv2.pointPolygonTest(cnt,far,True)

        # draw a line from start to end i.e. the convex points (finger tips)
        # (can skip this part)
        cv2.line(crop_img,start, end, [0,255,0], 2)
        cv2.circle(crop_img,far,5,[0,0,255],-1)
        

    for l in range(defects1.shape[0]):
        s1,e1,f1,d1 = defects1[l,0]

        start1 = tuple(cnt1[s1][0])
        end1 = tuple(cnt1[e1][0])
        far1 = tuple(cnt1[f1][0])
        
        # find length of all sides of triangle
        a1 = math.sqrt((end1[0] - start1[0])**2 + (end1[1] - start1[1])**2)
        b1 = math.sqrt((far1[0] - start1[0])**2 + (far1[1] - start1[1])**2)
        c1 = math.sqrt((end1[0] - far1[0])**2 + (end1[1] - far1[1])**2)

        # apply cosine rule here
        angle1 = math.acos((b1**2 + c1**2 - a1**2)/(2*b1*c1)) * 57

        # ignore angles > 90 and highlight rest with red dots
        if angle1 <= 90:
            count_defects1 += 1
            cv2.circle(crop_img1, far1, 1, [0,0,255], -1)
        #dist = cv2.pointPolygonTest(cnt,far,True)

        # draw a line from start to end i.e. the convex points (finger tips)
        # (can skip this part)
        cv2.line(crop_img1,start1, end1, [0,255,0], 2)
        cv2.circle(crop_img,far,5,[0,0,255],-1)
        
    if cv2.waitKey(1)== ord('n'):
        if (count_defects1 == 0):
            cv2.putText(img,"1", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
            engine.say("one")
            engine.runAndWait()
        elif (count_defects1 == 1):
            cv2.putText(img,"2", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2) 
        elif (count_defects1 == 2):
            cv2.putText(img,"3", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2) 
        elif (count_defects1 == 3):
            cv2.putText(img,"4", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        elif (count_defects1 == 4):
            cv2.putText(img,"5", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        if (count_defects == 0 and count_defects1 == 4):
            cv2.putText(img,"6", (500, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2) 
        elif (count_defects == 1 and count_defects1 == 4):
            cv2.putText(img,"7", (500, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2) 
        elif (count_defects == 2 and count_defects1 == 4):
            cv2.putText(img,"8", (500, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        elif (count_defects == 3 and count_defects1 == 4):
            cv2.putText(img,"9", (500, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        elif (count_defects == 4 and count_defects1 == 4):
            cv2.putText(img,"10", (500, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2) 

        
    if cv2.waitKey(1) == ord('w'):
        if (count_defects == 1 and count_defects1 == 1):
            cv2.putText(img,"Peace", (200, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2) 
        elif (count_defects == 0 and count_defects1 == 0):
            cv2.putText(img,"Best of luck", (200, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        elif (count_defects == 1):
            cv2.putText(img,"Smile", (200, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        elif (count_defects == 2):
            cv2.putText(img,"Nice", (200, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        elif (count_defects ==3 and count_defects1 == 3):
            cv2.putText(img,"Thank you", (200, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
    
    if cv2.waitKey(1) == ord('a'):
        if (count_defects1 == 0 or count_defects == -1):
            cv2.putText(img,"A", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        elif (count_defects1 == 1):
            cv2.putText(img,"B", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2) 
        elif (count_defects1 == 2):
            cv2.putText(img,"C", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2) 
        elif (count_defects1 == 3):
            cv2.putText(img,"D", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        elif (count_defects1 == 4):
            cv2.putText(img,"E", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        if (count_defects == 0 and count_defects1 == 4):
            cv2.putText(img,"F", (500, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2) 
        elif (count_defects == 1 and count_defects1 == 4):
            cv2.putText(img,"G", (500, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2) 
        elif (count_defects == 2 and count_defects1 == 4):
            cv2.putText(img,"H", (500, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        elif (count_defects == 3 and count_defects1 == 4):
            cv2.putText(img,"I", (500, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        elif (count_defects == 4 and count_defects1 == 4):
            cv2.putText(img,"J", (500, 50), cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        
        

        

    
    
         
        



    # show appropriate images in windows
    cv2.imshow('Gesture', img)
    all_img = np.hstack((drawing, crop_img))
    cv2.imshow('Contours', all_img)
    cv2.imshow('Gesture', img)
    all_img1 = np.hstack((drawing1, crop_img1))
    cv2.imshow('Contours1', all_img1)

    if cv2.waitKey(1)== ord('q'):
        break

cap.release()
cap1.release()
cv2.destroyAllWindows()
