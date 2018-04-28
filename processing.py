from owslib.wms import WebMapService
from owslib import crs
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
from pyspark import SparkContext
from pyproj import Proj

c = crs.Crs('EPSG:3857')
wms = WebMapService('http://www.ign.es/wms-inspire/pnoa-ma', version='1.3.0')


box = 1000 # m?
x=236814#m?
y=5068880 #m?
picsize = 512

img = wms.getmap(
    layers=['OI.OrthoimageCoverage'],
    styles=[],
    srs='EPSG:3857',
    bbox=(x - box, y - box, x + box, y + box),
    size=(picsize,picsize), #W,H px
    format='image/png',
    transparent=False
)
with open('image.png','wb') as out:
    out.write(img.read())
    
def green_detection():
    img = cv2.imread('image.png')
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

    cv2.imwrite('green_hsv.png',hsv)
    cv2.imwrite('green.png',output)
    cv2.imwrite('green_edges.png', green_edges)


def contour_detection():
    # Get the contours
    canny_img= cv2.imread('green_edges.png',0)
    img= cv2.imread('image.png',1)
    img2= cv2.imread('image.png',1)
    _, contours, hierarchy=cv2.findContours(canny_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,contours,-1,(0,255,0))
    cv2.imwrite('image_contours.png',img)

    #Filter the contours corresponding to football fields comparing the areas of the contours

    k=0
    filteredContours=[]
    fields_x_positions=[]
    fields_y_positions=[]
    thresholdarea= 800 
    while(k < len(contours)):
        epsilon = 0.1*cv2.arcLength(contours[k],True)
        contours[k] = cv2.approxPolyDP(contours[k],epsilon,True)
        area = cv2.contourArea(contours[k])
        print("Area; ",area)
        if thresholdarea + 200 > area > thresholdarea - 200:
            filteredContours.append(contours[k])
        k+=1

    cv2.drawContours(img2,filteredContours,-1,(0,255,0))
    cv2.imwrite('image_contours_filtered.png',img2)   
  
    return filteredContours

def location_convertor(contours,xm,ym,box,picsize):
	p1 = Proj(init='epsg:3857')
	c=[]
	for i,e in enumerate(contours):

		# We calculate the center point of each contour

		print(e.tolist())
		bounds= cv2.boundingRect(contours[i])
		x1,y1,w,h = bounds

		x=x1+w/2
		y=y1+h/2
		print(x,y)
		# Pixel to meter conversion


		x = (xm-box) + 2*box*(x1/picsize)
		y = (ym+box) - 2*box*(y1/picsize)

		# Meter to lon,lat conversion

		lon, lat = p1(x,y,inverse=True)

		c+=[[lon,lat]]
	
	return c





if __name__ == "__main__":
    green_detection()
    c=contour_detection()
    centers=location_convertor(c,x,y,box,picsize)
    print(centers)