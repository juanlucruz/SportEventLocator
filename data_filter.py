#!/usr/bin/env python3
# Data filtering and correlation

import time
import json
# import pandas as pd
# import numpy as np
import csv

# DATA_DIR = './'
# DATA_DIR = '/home/jl/'
DATA_DIR = '/media/osonoble/Águila Alfa/BIGDATA/'


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k.
    ref -> https://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python"""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def close_brackets(my_str,i=0):
    l_b = my_str.find('{')
    r_b = my_str.find('}')
    if l_b >= 0:
        i += 1
        close_brackets(my_str[l_b+1:])
    elif r_b >= 0 and i == 0:
        return

    elif r_b == -1:
        return ''
    return my_str


def main():
    acc = ''
    p = -1
    tweet_count = 0
    json_parsed = {}
    end_flag = False
    csvfile = open('geopy_results_{}.csv'.format(time.time()), 'w')
    csvwriter = csv.writer(csvfile)
    head = ['TweetID', 'Date', 'Lat', 'Long', 'Text', 'UserID']
    csvwriter.writerow(head)
    with open(DATA_DIR + 'saved_tweets_big.json', 'r') as fp:
    # with open(DATA_DIR + 'mini_file.json', 'r') as fp:
        json_listed = [i.split('}{') for i in fp][0]
    for el in json_listed:
        if el[0] != '{' and el[-1] != '}':
            # print('{' + el + '}')
            unzip = '{' + el + '}'
            try:
                json_parsed = json.loads(unzip)
            except json.decoder.JSONDecodeError as e:
                # print('Error decoding {}'.format(unzip))
                print('Error decoding')
                sub_els = el.split('}\n{')
                try:
                    for sub_el in sub_els:
                        if sub_el[0] != '{' and sub_el[-1] != '}':
                            unzip = '{' + sub_el + '}'
                            json_parsed = json.loads(unzip)
                        elif sub_el[0] != '{' and sub_el[-1] == '}':
                            unzip = '{' + sub_el
                            json_parsed = json.loads(unzip)
                        elif sub_el[0] == '{' and sub_el[-1] != '}':
                            unzip = sub_el + '}'
                            json_parsed = json.loads(unzip)
                except json.decoder.JSONDecodeError as e:
                    # print('Error decoding {}'.format(unzip))
                    print('Error decoding')
        elif el[0] != '{' and el[-1] == '}':
            # print('{' + el )
            unzip = '{' + el
            try:
                json_parsed = json.loads(unzip)
            except json.decoder.JSONDecodeError as e:
                # print('Error decoding {}'.format(unzip))
                print('Error decoding')
                sub_els = el.split('}\n{')
                try:
                    for sub_el in sub_els:
                        if sub_el[0] != '{' and sub_el[-1] != '}':
                            unzip = '{' + sub_el + '}'
                            json_parsed = json.loads(unzip)
                        elif sub_el[0] != '{' and sub_el[-1] == '}':
                            unzip = '{' + sub_el
                            json_parsed = json.loads(unzip)
                        elif sub_el[0] == '{' and sub_el[-1] != '}':
                            unzip = sub_el + '}'
                            json_parsed = json.loads(unzip)
                except json.decoder.JSONDecodeError as e:
                    # print('Error decoding {}'.format(unzip))
                    print('Error decoding')
        elif el[0] == '{' and el[-1] != '}':
            # print(el + '}')
            unzip = el + '}'
            try:
                json_parsed = json.loads(unzip)
            except json.decoder.JSONDecodeError as e:
                # print('Error decoding {}'.format(unzip))
                print('Error decoding')
                sub_els = el.split('}\n{')
                try:
                    for sub_el in sub_els:
                        if sub_el[0] != '{' and sub_el[-1] != '}':
                            unzip = '{' + sub_el + '}'
                            json_parsed = json.loads(unzip)
                        elif sub_el[0] != '{' and sub_el[-1] == '}':
                            unzip = '{' + sub_el
                            json_parsed = json.loads(unzip)
                        elif sub_el[0] == '{' and sub_el[-1] != '}':
                            unzip = sub_el + '}'
                            json_parsed = json.loads(unzip)
                except json.decoder.JSONDecodeError as e:
                    # print('Error decoding {}'.format(unzip))
                    print('Error decoding')

        # Filtering
        user_id = json_parsed['user']['id']
        tweet_id = json_parsed['id_str']
        if json_parsed['coordinates'] is not None:
            # print(json_parsed['coordinates'])
            longitude = json_parsed['coordinates']['coordinates'][0]
            latitude = json_parsed['coordinates']['coordinates'][1]
        else:
            bbox = json_parsed['place']['bounding_box']['coordinates'][0]
            # print(bbox)
            XY = [(bbox[0][0] + bbox[2][0]) / 2, (bbox[0][1] + bbox[2][1]) / 2]
            longitude = XY[0]
            latitude = XY[1]
        timestamp = json_parsed['timestamp_ms']
        if 'extended_tweet' in json_parsed.keys():
            text = json_parsed['extended_tweet']['full_text'].lower()
        else:
            text = json_parsed['text'].lower()

            csvwriter.writerow(
                [tweet_id,
                 timestamp,
                 latitude,
                 longitude,
                 ''.join(
                     list(
                         filter(
                             lambda ch: ch not in "?.!/;:,",
                             ''.join(text.split('\n'))
                         )
                     )
                 ),
                 user_id])


    # print(unzip)
    # print(json.dumps(json_parsed[1],indent=2))
    # print(json_parsed[1]['place']['full_name'])
    # for i in range(2):
    #     if 'extended_tweet' in json_parsed[i].keys():
    #         print(json_parsed[i]['extended_tweet']['full_text'].lower().split())
    #     else:
    #         print(json_parsed[i]['text'].lower().split())
    # print(a)
    # ID, timestamp, latitud, longitud, texto, USER

if __name__ == "__main__":
    main()
