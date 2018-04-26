from pyproj import Proj

p1 = Proj(init='epsg:3857')

#lat = 41.390205
#lon = 2.154007

x=239706.5207023127
y=5070526.70832545
lon, lat = p1(x,y,inverse=True)

print(lat,lon)



