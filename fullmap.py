from owslib.wms import WebMapService
from owslib import crs
from pyproj import Proj, transform
from location_finder import getmap
import cv2

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
cv2.imwrite('circle.png',img1)

xydict = getmap()

img1 = cv2.imread('circle.png')
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
        except Exception as e:
            print(e)

cv2.imwrite('circle.png', img1)
