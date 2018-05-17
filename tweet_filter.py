from location_finder import getmap
import csv
from math import sin, cos, sqrt, atan2, radians
import unidecode

def distance_calculator(lat1,lon1,lat2,lon2):
    # approximate radius of earth in km
    R = 6373000

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    #print("Result:", distance)
    return distance


def location_filter():
    filtered=[]
    location_dict=getmap()
    file=open('geopy_results_1526569414.4222775.csv')
    entry=csv.reader(file)
    next(entry,None)
    for row in entry:
        for element in location_dict.values():
                for coordinate in element:
                    try:    
                        if distance_calculator(coordinate[1],coordinate[0],float(row[2]),float(row[3])) < 200:
                            filtered.append(row)
                    except:
                        pass
    return filtered


def keyword_filter(filtered_locations,keywords):
    filtered = []
    for word in keywords:
        for row in filtered_locations:
            text= row[4].lower()
            text=unidecode.unidecode(text)
            if word in text:
                filtered.append([word, row[1]])
    return filtered


def tweet_filter(keyword_list):
    filtered_locations=location_filter()
    filtered_words=keyword_filter(filtered_locations,keyword_list)
    return filtered_words

if __name__ == "__main__":
    filtered_words = tweet_filter(['futbol','camp nou','champions'])
    for element in filtered_words:
            print(element)