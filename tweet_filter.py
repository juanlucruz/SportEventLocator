from location_finder import getmap
import csv
from math import sin, cos, sqrt, atan2, radians
import unidecode
from datetime import datetime, timedelta
from itertools import groupby
from collections import OrderedDict


global stopwords
stopwords=['futbol','camp nou','champions','clasico','derbi','cornella','barça','espanyol']

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

def get_key(d):
    # group by 30 minutes
    k = d + timedelta(minutes=-(d.minute % 30))
    return datetime(k.year, k.month, k.day, k.hour, k.minute, 0)

def location_filter():
    filtered=[]
    locations=[]
    #location_dict=getmap()
    file=open('locations.csv')
    entry=csv.reader(file)
    for element in entry:
        locations.append([element[2],element[1]])
    file.close()

    file=open('geopy_results_1527171096.641982.csv')
    entry=csv.reader(file)
    next(entry,None)
    for row in entry:
        for element in locations:
            try:    
                if distance_calculator(float(element[0]),float(element[1]),float(row[2]),float(row[3])) < 200:
                    filtered.append(row)
            except:
                pass
    return filtered

def keyword_filter(filtered_locations,stopwords):
    filtered=[]
    for word in stopwords:
        for row in filtered_locations:
            text= row[4].lower()
            text=unidecode.unidecode(text)
            if word in text:
                filtered.append([word, row[1]])

    return filtered

def tweet_filter(keyword_list):
    filtered_locations=location_filter()
    filtered_words=keyword_filter(filtered_locations,keyword_list)
    with open('filtered_words.csv',"w") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(filtered_words)
        f.close()
    return filtered_words

def occurrence_count(filtered_words,stopwords):
    occurrence_list=[]
    #Remove duplicates
    unique = []
    for item in filtered_words:
        if item not in unique:
            unique.append(item)
    filtered_words=unique

    for stopword in stopwords:
        occurrence_list.append([stopword,0])

    for word in filtered_words:
        #word[1]=datetime.fromtimestamp(float(word[1])/1000.0).strftime('%Y-%m-%d %H:%M:%S')
        word[1]=datetime.fromtimestamp(float(word[1])/1000.0)
        for i,stopword in enumerate(stopwords):
            if word[0] == stopword:
                occurrence_list[i][1]+=1
    
    with open('filtered_words.csv',"w") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(filtered_words)
        f.close()

    occurrence_hours=[]
    for stopword in stopwords:
        occurrence_hours.append([])

    for i,stopword in enumerate(stopwords):
        for word in filtered_words:
            if word[0] == stopword:
                occurrence_hours[i].append(word[1])

    count=0
    row=[]
    with open('occurrences.csv',"w") as f:
        writer = csv.writer(f, lineterminator='\n')
        for i,element in enumerate(occurrence_hours):
            g = groupby(sorted(element), key=get_key)
            # print data
            for key, items in g:
                #print(key)
                for item in items:
                    #print('-', item)
                    count+=1
                row=[stopwords[i],key,count]
                writer.writerow(row)
                count=0
                row=[]
        f.close()

    return occurrence_list, occurrence_hours

if __name__ == "__main__":
    filtered_words=tweet_filter(stopwords)
    occurrence_list, occurrence_hours=occurrence_count(filtered_words,stopwords)
    """
    for element in filtered_words:
            print(element)
    """
    """
    for element in occurrence_list:
        print(element)

    for element in occurrence_hours:
        print(element)
    """