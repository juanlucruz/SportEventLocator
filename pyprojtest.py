from pyproj import Proj, transform

proj_rect_meters = Proj(init='epsg:3857')
proj_wgs = Proj(init='epsg:4326')

#lat = 41.390205
#lon = 2.154007

x1 = 239706.5207023127
y1 = 5070526.70832545


lon1, lat1 = transform(proj_rect_meters, proj_wgs, x1, y1)
print(lat1, lon1)

lat2, lon2 = 40.453021, -3.688355

x2, y2 = transform(proj_wgs, proj_rect_meters, lon2, lat2)

print(x2, y2)

x3 = 241314
y3 = 5070580

for coords in [(x3-5000, y3-5000), (x3 + 5000, y3 + 5000)]:
    lon3, lat3 = transform(proj_rect_meters, proj_wgs, coords[0], coords[1])
    print(lat3, lon3)


