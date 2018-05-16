#!/usr/bin/env python3
# Data filtering and correlation

import datetime
import json
# import pandas as pd
import numpy as np

DATA_DIR = './'
DATA_DIR = '/home/jl/'


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
    chunk_count = 0
    tweet_count = 0
    indent = 0
    json_parsed = []
    end_flag = False
    with open(DATA_DIR + 'saved_tweets_big.json', 'r') as fp:
    # with open(DATA_DIR + 'mini_file.json', 'r') as fp:
        json_listed = [i.split('}{') for i in fp][0]
    for el in json_listed:
        if el[0] != '{' and el[-1] != '}':
            # print('{' + el + '}')
            unzip = '{' + el + '}'
            try:
                json_parsed.append(json.loads(unzip))
            except json.decoder.JSONDecodeError as e:
                print('Error decoding {}'.format(unzip))
        elif el[0] != '{' and el[-1] == '}':
            # print('{' + el )
            unzip = '{' + el
            try:
                json_parsed.append(json.loads(unzip))
            except json.decoder.JSONDecodeError as e:
                print('Error decoding {}'.format(unzip))
        elif el[0] == '{' and el[-1] != '}':
            # print(el + '}')
            unzip = el + '}'
            try:
                json_parsed.append(json.loads(unzip))
            except json.decoder.JSONDecodeError as e:
                print('Error decoding {}'.format(unzip))
        # a = json.load(fp)
        # for chunk in read_in_chunks(fp, 1024):
        #     # print(chunk)
        #     l_brackets = chunk.count('{')
        #     r_brackets = chunk.count('}')
        #     print('CHUNK',chunk_count)
        #
        #     # Parse chunk
        #     for i in range(l_brackets+r_brackets):
        #         print('BRACKETS',i)
        #         if l_brackets > 0 and r_brackets > 0:
        #             l_bracket_i = chunk[p+1:].find('{')
        #             r_bracket_i = chunk[p+1:].find('}')
        #             if l_bracket_i > r_bracket_i:
        #                 p += l_bracket_i
        #                 indent += 1
        #                 l_brackets -= 1
        #             else:
        #                 p += r_bracket_i
        #                 indent -= 1
        #                 r_brackets -= 1
        #                 if indent == 0:
        #                     json_parsed = acc + chunk[:p]
        #                     break
        #         elif l_brackets > 0 and r_brackets == 0:
        #             l_bracket_i = chunk[p + 1:].find('{')
        #             p += l_bracket_i
        #             indent += 1
        #             l_brackets -= 1
        #         elif l_brackets == 0 and r_brackets > 0:
        #             r_bracket_i = chunk[p + 1:].find('}')
        #             p += r_bracket_i
        #             indent -= 1
        #             r_brackets -= 1
        #             if indent == 0:
        #                 json_parsed = acc + chunk[:p]
        #                 break
        #
        #     if json_parsed != '' and indent == 0:
        #         break
        #     acc += chunk
        #     chunk_count += 1
            #  END READING FOR
    print(len(json_parsed))
    print(json.dumps(json_parsed[0],indent=2))
    # print(a)

if __name__ == "__main__":
    main()