from location_finder import getmap
import csv
from math import sin, cos, sqrt, atan2, radians
import unidecode
from datetime import datetime, timedelta
from itertools import groupby
from collections import OrderedDict
import pandas as pd
import numpy as np


# global keywords
# stopwords = ['futbol','camp nou','champions','clasico','derbi','cornella','barça','espanyol']


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


def get_datetime_key(d, min_period=30):
    # group by min_period [minutes]
    k = d + timedelta(minutes=-(d.minute % min_period))
    return datetime(k.year, k.month, k.day, k.hour, k.minute, 0)


def location_filter(tweet_df, loc_longitude, loc_latitude, distance_threshold=200):
    # tweet_df = pd.read_csv('final_results_clean_short.csv')
    loc_filtered_df = pd.DataFrame(columns=['tweetID','date','lat','lon','text','userID'])
    i = 0
    for index, row in tweet_df.iterrows():
        if distance_calculator(loc_latitude, loc_longitude, float(row['lat']), float(row['lon'])) < distance_threshold:
            row['lat'] = loc_latitude
            row['lon'] = loc_longitude
            loc_filtered_df.loc[i] = row
            i += 1
    return loc_filtered_df


def keyword_filter(filtered_locations, keywords):
    filtered = []
    for word in keywords:
        for row in filtered_locations:
            text = row[4]
            text = unidecode.unidecode(text)
            if word in text:
                filtered.append([word, row[1]])

    return filtered


def tweet_filter(location_dataframe, keyword_list):
    filtered = []
    counted_words_df = location_dataframe.copy()
    sLength = len(location_dataframe['tweetID'])
    for keyword in keyword_list:  # column
        # filtered_words = keyword_filter(location_dataframe, keyword_list)
        counted_words_df[keyword] = pd.Series([0]*sLength, index=counted_words_df.index)
        for index, row in counted_words_df.iterrows():
            # print(row['text'].split())
            if keyword in row['text'].split():
                # print('HIT {}'.format(keyword))
                counted_words_df.at[index, keyword] = 1
    del counted_words_df['text']

    #         for row in :
    #             text = row[4]
    #             text = unidecode.unidecode(text)
    #             if word in text:
    #                 filtered.append([word, row[1]])
    # with open('filtered_words.csv', "w") as f:
    #     writer = csv.writer(f, lineterminator='\n')
    #     writer.writerows(filtered_words)
    #     f.close()
    return counted_words_df


def occurrence_count(filtered_words, stopwords):
    occurrence_list = []
    #Remove duplicates
    unique = []
    for item in filtered_words:
        if item not in unique:
            unique.append(item)
    filtered_words = unique

    for stopword in stopwords:
        occurrence_list.append([stopword, 0])

    for word in filtered_words:
        # word[1]=datetime.fromtimestamp(float(word[1])/1000.0).strftime('%Y-%m-%d %H:%M:%S')
        word[1] = datetime.fromtimestamp(float(word[1])/1000.0)
        for i, stopword in enumerate(stopwords):
            if word[0] == stopword:
                occurrence_list[i][1] += 1
    
    # with open('filtered_words.csv',"w") as f:
    #     writer = csv.writer(f, lineterminator='\n')
    #     writer.writerows(filtered_words)
    #     f.close()

    occurrence_hours = []
    for stopword in stopwords:
        occurrence_hours.append([])

    for i, stopword in enumerate(stopwords):
        for word in filtered_words:
            if word[0] == stopword:
                occurrence_hours[i].append(word[1])

    count = 0
    row = []
    with open('occurrences.csv',"w") as f:
        writer = csv.writer(f, lineterminator='\n')
        for i, element in enumerate(occurrence_hours):
            g = groupby(sorted(element), key=get_key)
            # print data
            for key, items in g:
                #print(key)
                for item in items:
                    #print('-', item)
                    count+=1
                row = [stopwords[i], key, count]
                writer.writerow(row)
                count = 0
                row=[]
        f.close()

    return occurrence_list, occurrence_hours


def main():
    keywords = {
        'tarragona', 'pase', 'tiro', 'español', 'espanyol', 'barsa', 'madrid', 'sevilla', 'zaragoza', 'lorca',
        'almeria', 'empieza', 'lugo', 'vigo', 'agrupacion', 'soria', 'futbol', 'jugadores', 'cadiz', 'gol', 'roja',
        'gimnastic', 'corner', 'alcorcon', 'campeones', 'balompie', 'levante', 'falta', 'partido', 'centro', 'union',
        'futbol','estadi', 'gijon', 'targeta', 'pelota', 'barça', 'deportiu', 'huesca', 'saque', 'cultural', 'yellow',
        'betis', 'rayo', 'albacete', 'alaves', 'leonesa', 'valladolid', 'liga', 'goles', 'clasico', 'estadio', 'club',
        'sociedad', 'deportivo', 'final', 'entrada', 'eibar', 'palmas', 'celta', 'vermella', 'barcelona', 'numancia',
        'cordoba', 'reus', 'valencia', 'campeon', 'coruña', 'vallecano', 'malaga', 'faltas', 'granada', 'athletic',
        'osasuna', 'amarilla', 'getafe', 'penalty', 'tenerife', 'villarreal', 'atleti', 'atletico', 'deportiva',
        'tarjeta', 'sporting', 'balompie', 'arbitro', 'leganes', 'oviedo', 'red', 'girona', 'groga', 'real'
    }
    field_id = 0
    field_locations = pd.read_csv('locations.csv')
    # print(field_locations.head())
    tweet_df = pd.read_csv('final_results_clean_short.csv', dtype=str)
    # print(tweet_df.head())
    del field_locations['ID']
    loc_full_df = None
    filtered_words_list = []
    for index, row in field_locations.iterrows():
        loc_filtered_df = location_filter(tweet_df, row['lon'], row['lat'])
        if not loc_filtered_df.empty:
            # print(loc_filtered_df.head())
            filtered_words_list.append(tweet_filter(loc_filtered_df, keywords))
            # print(filtered_words)
            print(len(filtered_words_list))
    # for el in filtered_words_list:
    #     print(el['barcelona'])
    loc_full_df = pd.concat(filtered_words_list, ignore_index=True)
            # if loc_full_df is None:
            #     loc_full_df = filtered_words.copy()
            #     print(loc_full_df.head())
            # else:
            #     print('BEFORE:{}'.format(loc_full_df.head()))
            #     print('words:{}'.format(filtered_words.head()))
            #     loc_full_df.append(filtered_words)
            #     print('AFTER:{}'.format(loc_full_df.head()))
            # input('WAIT')
    loc_full_df.sort_values(by=['date']).reset_index(drop=True).to_csv('final_count.csv')
    # occurrence_list, occurrence_hours = occurrence_count(filtered_words, keywords)

if __name__ == "__main__":
    main()
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