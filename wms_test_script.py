from owslib.wms import WebMapService
from owslib import crs

c = crs.Crs('EPSG:3857')
wms = WebMapService('http://www.ign.es/wms-inspire/pnoa-ma', version='1.3.0')
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
x=234314 #m?
y=5067580 #m?
box = 2000 # m?
img = wms.getmap(
    layers=['OI.OrthoimageCoverage'],
    styles=[],
    srs='EPSG:3857',
    bbox=(x - box, y - box, x + box, y + box),
    size=(256,256), #W,H px
    format='image/png',
    transparent=False
)
with open('example_image_mosaic.png','wb') as out:
    out.write(img.read())

