# General Map outputs module

from owslib.wms import WebMapService
from owslib import crs
from pyproj import Proj, transform
from location_finder import getmap
import cv2
import csv
import sys
import matplotlib as plt
import numpy as np
from skimage import io
import colorsys


def color_palette(N):
    HSV_tuples = [(x * 1.0 / N, 0.5, 0.5) for x in range(N)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    return list(RGB_tuples), HSV_tuples

def draw_fields_detected():
    c = crs.Crs('EPSG:3857')
    #wms = WebMapService('http://www.ign.es/wms-inspire/pnoa-ma', version='1.3.0')


    box = 10000 # m?
    x=238814#m?
    y=5069880 #m?
    picsize = 2048

    """
    img = wms.getmap(
        layers=['OI.OrthoimageCoverage'],
        styles=[],
        srs='EPSG:3857',
        bbox=(x - box, y - box, x + box, y + box),
        size=(picsize,picsize), #W,H px
        format='image/png',
        transparent=False
    )
    with open('fullmap.png','wb') as out:
        out.write(img.read())
    """
    img1 = cv2.imread('fullmap.png')
    circles = img1.copy()

    xydict = getmap()
    for element in xydict.values():
        for value in element:
            lon = value[0]
            lat = value[1]
            try:
                proj = Proj(init='epsg:3857')
                xm, ym = proj(lon, lat)
                p1 = picsize / (2 * box) * (xm - (x - box))
                p2 = picsize / (2 * box) * ((y + box) - ym)
                cv2.circle(img1, (int(p1), int(p2)), 5, (0, 0, 255), -1)
                plt.imshow()
            except Exception as e:
                print(e)

    cv2.imwrite('circle.png', circles)


def draw_tweets_detected(file):
    # Tweet info draw
    c = crs.Crs('EPSG:3857')
    # wms = WebMapService('http://www.ign.es/wms-inspire/pnoa-ma', version='1.3.0')


    box = 10000  # m?
    x = 238814  # m?
    y = 5069880  # m?
    picsize = 2048
    img1 = cv2.imread('fullmap.png')
    img_fields = cv2.imread('circle.png')
    overlay = img1.copy()
    tweets = img1.copy()
    final = img_fields.copy()
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file,)
        reader.__next__()
        lat = []
        lon = []
        for row in reader:
            # print(format(row).encode())
            lat.append(row[2])
            lon.append(row[3])
    print('Csv finished')
    n_tweets = len(lat)
    alpha = 2/n_tweets
    colors, _ = color_palette(n_tweets)
    for i in range(len(lat[:n_tweets])):
        try:
            print('Writing...{}'.format(i))
            proj = Proj(init='epsg:3857')
            xm, ym = proj(lon[i], lat[i])
            p1 = picsize / (2 * box) * (xm - (x - box))
            p2 = picsize / (2 * box) * ((y + box) - ym)
            # cv2.circle(overlay, (int(p1), int(p2)), 5, (int(colors[i][2] * 255), int(colors[i][1] * 255), int(colors[i][0] * 255)), -1)
            # cv2.circle(tweets, (int(p1), int(p2)), 5, (int(colors[i][2] * 255), int(colors[i][1] * 255), int(colors[i][0] * 255)), -1)
            cv2.circle(tweets, (int(p1), int(p2)), 5,
                       (0, 200, 255), -1)
            cv2.circle(final, (int(p1), int(p2)), 5,
                       (0, 200, 255), -1)

            # cv2.addWeighted(overlay, alpha,
            #                 tweets, 1 - alpha,
            #                 0, tweets)
        except Exception as e:
            print(e)

    cv2.imshow("Output", tweets)
    cv2.imwrite('tweets.png', tweets)
    cv2.imwrite('tweetsNfields.png', final)


def main(args):
    # draw_fields_detected()
    draw_tweets_detected(args[1])


if __name__ == '__main__':
    # print(sys.argv)
    main(sys.argv)
