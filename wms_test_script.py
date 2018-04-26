from owslib.wms import WebMapService
from owslib import crs
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np


c = crs.Crs('EPSG:3857')
wms = WebMapService('http://www.ign.es/wms-inspire/pnoa-ma', version='1.3.0')
"""
print('Type:',wms.identification.type)
print('Title:',wms.identification.title)
print('Contents:',list(wms.contents))
for el in wms.contents:
    print('*'*80)
    print('\tTitle({}):{}'.format(el,wms[el].title))
    print('\tQueryable:       ',wms[el].queryable)
    print('\tOpaque:          ',wms[el].opaque)
    print('\tBoundingBox:     ',wms[el].boundingBox)
    print('\tBoundingBoxWGS84:',wms[el].boundingBoxWGS84)
    print('\tcrsOptions:      ',wms[el].crsOptions)
    print('\tStyles:          ',wms[el].styles)

print('*'*80)
print('Operations:',[op.name for op in wms.operations])
print('GetMap methods:',wms.getOperationByName('GetMap').methods)
print('GetMap formats:',wms.getOperationByName('GetMap').formatOptions)
#lat = 41.390205
#lon = 2.154007
#box = 0.01
"""

box = 1000 # m?
x=234314#m?
y=5067580 #m?

picsize = 512 
#possible (boxsize/picsize) configurations to detect fields: 1000/512, 2000/512 , 1000 /256

img = wms.getmap(
    layers=['OI.OrthoimageCoverage'],
    styles=[],
    srs='EPSG:3857',
    bbox=(x - box, y - box, x + box, y + box),
    size=(picsize,picsize), #W,H px
    format='image/png',
    transparent=False
)
with open('example_image_mosaic.png','wb') as out:
    out.write(img.read())


def green_detection():
    img = cv2.imread('example_image_mosaic.png')
    # Green fields detection
    hsv= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Threshold for detecting green
    lower = np.array([33, 58, 33])
    upper = np.array([120,250,120])
    
    # Apply mask
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(img, img, mask = mask)

    hsv_gray= cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    green_edges=cv2.Canny(hsv_gray,150,200)

    cv2.imwrite('green_hsv.png',hsv)
    cv2.imwrite('green.png',output)
    cv2.imwrite('green_edges.png', green_edges)


def contour_detection():
    # Get the contours
    canny_img= cv2.imread('green_edges.png',0)
    img= cv2.imread('example_image_mosaic.png',1)
    img2= cv2.imread('example_image_mosaic.png',1)
    _, contours, hierarchy=cv2.findContours(canny_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,contours,-1,(0,255,0))
    cv2.imwrite('contours.png',img)

    #Filter the contours corresponding to football fields

    MinHeight= 20
    MaxHeight= 45
    MinWidth= 20
    MaxWidth= 45
    k=0
    filteredContours=[]
    fields_x_positions=[]
    fields_y_positions=[]
    while(k < len(contours)):
        bounds= cv2.boundingRect(contours[k])
        x,y,w,h = bounds
        if ((h > MinHeight) and (h < MaxHeight) and (w > MinWidth)):
            filteredContours.append(contours[k])

            # We save the X and Y pixel position of the fields
            fields_y_positions.append(y)
            fields_x_positions.append(x)
        k += 1

    cv2.drawContours(img2,filteredContours,-1,(0,255,0))
    cv2.imwrite('filtered_contours.png',img2)    


if __name__ == "__main__":
    green_detection()
    contour_detection()
