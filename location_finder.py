from owslib.wms import WebMapService
from owslib import crs
from pyspark import SparkContext
from image_processing import *
import csv


c = crs.Crs('EPSG:3857')
wms = WebMapService('http://www.ign.es/wms-inspire/pnoa-ma', version='1.3.0')


def parallel_processing(xy, box, picsize):
    img = wms.getmap(
        layers=['OI.OrthoimageCoverage'],
        styles=[],
        srs='EPSG:3857',
        bbox=(xy[0] - box, xy[1] - box, xy[0] + box, xy[1] + box),
        size=(picsize,picsize), #W,H px
        format='image/png',
        transparent=False
    )
    with open('Images/image{0}{1}.png'.format(xy[0],xy[1]),'wb') as out:
        out.write(img.read())
    
    green_detection(xy)
    c=contour_detection(xy)
    locations=location_convertor(c,xy,box,picsize)
    return locations


def getmap():
    sc = SparkContext()
    box = 1000  # m?
    x=241314  # m?
    y=5066180  # m?
    picsize = 512
    xylist=[]
    d=[]
    xydict={}
    location_list=[]
    for i in range(-12,12):
        for j in range(-12,12):
            xylist.append([x+(i*(box-100)),y+(j*(box-100))])
    
    xylist = sc.parallelize(xylist)\
        .map(lambda x: [x,parallel_processing(x, box, picsize)])\
        .collect()
    sc.stop()
    
    # remove localization exact duplicates
    [d.append(item) for item in xylist if item not in d]

    for element in d:
        if element[1] != []:
            xydict[str(element[0][0])+str(element[0][1])] = element[1]
    return xydict

if __name__ == "__main__":
    xydict = getmap()
    with open(r'saved_tweets_big.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        for element in xydict.items():
            writer.writerow(element)
