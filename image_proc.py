from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
from pyproj import Proj, transform

def green_detection(xy):
    img = cv2.imread('Images/image{0}{1}.png'.format(xy[0],xy[1]))
    # Green fields detection
    hsv= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Threshold for detecting green
    lower = np.array([15, 58, 15])
    upper = np.array([100,240,100])
    
    # Apply mask
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(img, img, mask = mask)

    hsv_gray= cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    green_edges=cv2.Canny(hsv_gray,100,200)

    #cv2.imwrite('green_hsv.png',hsv)
    #cv2.imwrite('green.png',output)
    cv2.imwrite('Imagesproc/image{0}{1}.png'.format(xy[0],xy[1]), green_edges)


def contour_detection(xy):
    # Get the contours
    canny_img= cv2.imread('Imagesproc/image{0}{1}.png'.format(xy[0],xy[1]),0)
    img= cv2.imread('Images/image{0}{1}.png'.format(xy[0],xy[1]),1)
    #img2= cv2.imread('example_image_mosaic.png',1)
    _, contours, hierarchy=cv2.findContours(canny_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img,contours,-1,(0,255,0))
    #cv2.imwrite('Imagesproc/image{0}{1}.png'.format(xy[0],xy[1]),img)

    #Filter the contours corresponding to football fields

    k=0
    filteredContours=[]
    fields_x_positions=[]
    fields_y_positions=[]
    thresholdarea= 800 
    while(k < len(contours)):
        epsilon = 0.1*cv2.arcLength(contours[k],True)
        contours[k] = cv2.approxPolyDP(contours[k],epsilon,True)
        area = cv2.contourArea(contours[k])
        if (thresholdarea + 250 > area > thresholdarea - 250) and len(contours[k])==4:
            filteredContours.append(contours[k])
        k+=1

    cv2.drawContours(img,filteredContours,-1,(0,255,0))
    cv2.imwrite('Imagesproc/image{0}{1}.png'.format(xy[0],xy[1]),img)   

    return filteredContours

def location_convertor(contours,xy,box,picsize):
    p1 = Proj(init='epsg:3857')
    p2 = Proj(init='epsg:4326')
    c=[]
    xm=xy[0]
    ym=xy[1]
    for i,e in enumerate(contours):

        # We calculate the center point of each contour

        #print(e.tolist())
        bounds= cv2.boundingRect(contours[i])
        x1,y1,w,h = bounds

        x=x1+w/2
        y=y1+h/2
        #print(x,y)

        # Pixel to meter conversion

        x = (xm-box) + 2*box*(x1/picsize)
        y = (ym+box) - 2*box*(y1/picsize)

        # Meter to lon,lat conversion

        lon, lat = p1(x,y,inverse=True)

        # Remove duplicates
        xl=100
        yl=0
        xl, yl = transform(p1, p2,  lon, lat)

        if len(c) > 0:
            for element in c:
                if (element[0]+xl > lon > element[0]-xl) or (element[1]+yl > lat > element[1]-yl):
                    pass 
                else:
                    c+=[[lon,lat]]              
        else:
            c+=[[lon,lat]]          
    
    return c
    
