import math
from PIL import Image

from owslib.wms import WebMapService

wms = WebMapService('http://www.ign.es/wms-inspire/pnoa-ma', version='1.1.1')

print(list(wms.contents))
print("")
print(wms.getOperationByName('GetMap').formatOptions) #image/png
print("")
print(wms['OI.MosaicElement'].styles) #default
print("")
print(wms['OI.MosaicElement'].crsOptions)
print("")

img = wms.getmap(layers=['OI.MosaicElement'],
	styles=['default'],
	srs='EPSG:23031',
	bbox=(237260.53579718707,5068080.7234203275,239706.5207023127,5070526.70832545),
	size=(256, 256),
	format='image/png',
	transparent=False)

out = open('jpl_mosaic_visb.png', 'wb')
out.write(img.read())
out.close()
