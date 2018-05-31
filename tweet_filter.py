from location_finder import getmap
import csv
from math import sin, cos, sqrt, atan2, radians
import unidecode
from datetime import datetime, timedelta
from itertools import groupby
from collections import OrderedDict
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import seaborn.apionly as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

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
            if keyword in row['text'].split() or '#' + keyword in row['text'].split():
                # print('HIT {}'.format(keyword))
                counted_words_df.at[index, keyword] = 1
    del counted_words_df['text']
    return counted_words_df

def match_simple(row):
    if row['barcelona'] > 5:
        row['match'] = True

def match_double(row, rival):
    if row['barcelona'] > 2 and row[rival] > 2:
        row['match'] = True


def occurrence_count(keywords):

    #Remove duplicates
    final_count_df = pd.read_csv('final_count.csv')
    final_count_df.drop_duplicates(subset=['tweetID'], keep='first')
    del final_count_df['i']
    ocurrences_df = final_count_df.copy()

    # final_count_df.to_csv('final_count2.csv', index=False)
    for index, row in ocurrences_df.iterrows():
        ocurrences_df.loc[index, "date"] = datetime.fromtimestamp(float(row['date'])/1000.0)

    del ocurrences_df['tweetID']
    del ocurrences_df['lat']
    del ocurrences_df['lon']
    del ocurrences_df['userID']
    ocurrences_df.index = pd.DatetimeIndex(ocurrences_df['date'].values)
    dfrs = ocurrences_df.resample('30min').apply(sum)
    dfrs.fillna(0, inplace=True)
    print(dfrs.head())
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # x = list(dfrs.index.values)
    # y = list(dfrs.columns.values)
    # z = dfrs.values
    weeks = [g for n, g in dfrs.groupby(pd.TimeGrouper('W'))]
    # pd.DataFrame.index.
    # plt.figure()

    # print(len(weeks))
    w = 0
    for week_data in weeks:
        # print(week_data.std())
        high_var_df = week_data.loc[:, week_data.std() > .1]
        high_var_df['match'] = 0
        # print(high_var_df.head())
        if w == 0:
            # for index, row in high_var_df.iterrows():
                # row['match'] = False
            pass
        elif w == 1:
            high_var_df[329:334]['match'] = 1
            # for index, row in high_var_df.iterrows():
            #     row['match'] = 1 if row['madrid'] > 2 and row['barcelona'] > 2 else 0
                # row['match'] = 1 if row['barcelona'] > 5 else 0
                #331->335

                # high_var_df.loc[index] = row
        elif w == 2:
            high_var_df[136:140]['match'] = 1
            # for index, row in high_var_df.iterrows():
            #     row['match'] = 1 if row['barcelona'] > 2 and row['villarreal'] > 2 else 0
            #     # row['match'] = 1 if row['barcelona'] > 5 else 0
            #     #138->141
            #     high_var_df.loc[index] = row
        high_var_df.to_csv(str(high_var_df.index[0]) + '.csv')
        plt.figure()
        for name, series in high_var_df.iteritems():
            plt.plot(series, high_var_df.index)
        plt.figure()
        ax1 = sns.heatmap(high_var_df)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=90)
        plt.tight_layout()
        plt.figure()
        ax2 = sns.heatmap(high_var_df.corr())
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)
        plt.tight_layout()
        # print(x, y, z)
        # input('ENTER')
        model_train(high_var_df, w,  'linear_regression')
        w += 1

    plt.pause(0.001)
    input('ENTER')
    plt.close()
    dfrs.to_csv('occurrences.csv',index=True)
    # high_var_df.to_csv('high_var_df.csv',index=True)


def model_train(data, w,  ml_type=None,):
    # data = data.drop('date', axis=1)
    # train_pr = ['barcelona', 'madrid', 'real', 'barça']
    # prdata = data[train_pr]
    data['is_train'] = np.random.uniform(0, 1, len(data)) <= .75
    train, test = data[data['is_train'] == True], data[data['is_train'] == False]
    # print('Number of observations in the training data:', len(train))
    # print('Number of observations in the test data:', len(test))
    # print(train.head())
    # features = data.columns.values[:-2]
    np.random.seed(0)
    if ml_type == 'linear_regression':
        # Linear Regression
        target = train.match
        train_pr = train.columns.values[:-2]

        predictor = LinearRegression(n_jobs=-1)
        predictor.fit(train[train_pr], target)

        print('features: {}'.format(train_pr))
        print('coefficients: {}'.format(predictor.coef_))
        test[train_pr].convert_objects(convert_numeric=True)
        outcome = predictor.predict(X=test[train_pr].values)

        for i in range(len(outcome)):
            if outcome[i]>0:
                print('{}.\tOUTCOME: {} -> match: {}'.format(i, outcome[i], test['match'][i]))
    elif ml_type=='random_forest':
        # train_x, test_x, train_y, test_y = train_test_split(data, 0.7)

        print(features)
        # faltan labels
    elif ml_type == 'knearest':
        indices = np.random.permutation(len(data))
    else:
        pass


def sparser(keywords):
    field_id = 0
    field_locations = pd.read_csv('locations.csv')
    # print(field_locations.head())
    # tweet_df = pd.read_csv('final_results_clean_short.csv', dtype=str)
    tweet_df = pd.read_csv('final_results_clean.csv', dtype=str)
    # print(tweet_df.head())
    del field_locations['ID']
    # del field_locations[0]
    filtered_words_list = []
    for index, row in field_locations.iterrows():
        loc_filtered_df = location_filter(tweet_df, row['lon'], row['lat'])
        if not loc_filtered_df.empty:
            # print(loc_filtered_df.head())
            filtered_words_list.append(tweet_filter(loc_filtered_df, keywords))
            # print(filtered_words)
        print('{}/{}'.format(index+1,len(field_locations.index)))
    loc_full_df = pd.concat(filtered_words_list, ignore_index=True)
    loc_full_df.sort_values(by=['date']).reset_index(drop=True).to_csv('final_count.csv')
    # occurrence_list, occurrence_hours = occurrence_count(filtered_words, keywords)


if __name__ == "__main__":
    # keywords = {
    #     'tarragona', 'pase', 'tiro', 'español', 'espanyol', 'barsa', 'madrid', 'sevilla', 'zaragoza', 'lorca',
    #     'almeria', 'empieza', 'lugo', 'vigo', 'agrupacion', 'soria', 'futbol', 'jugadores', 'cadiz', 'gol', 'roja',
    #     'gimnastic', 'corner', 'alcorcon', 'campeones', 'balompie', 'levante', 'falta', 'partido', 'centro', 'union',
    #     'futbol', 'estadi', 'gijon', 'targeta', 'pelota', 'barça', 'deportiu', 'huesca', 'saque', 'cultural', 'yellow',
    #     'betis', 'rayo', 'albacete', 'alaves', 'leonesa', 'valladolid', 'liga', 'goles', 'clasico', 'estadio', 'club',
    #     'sociedad', 'deportivo', 'final', 'entrada', 'eibar', 'palmas', 'celta', 'vermella', 'barcelona', 'numancia',
    #     'cordoba', 'reus', 'valencia', 'campeon', 'coruña', 'vallecano', 'malaga', 'faltas', 'granada', 'athletic',
    #     'osasuna', 'amarilla', 'getafe', 'penalty', 'tenerife', 'villarreal', 'atleti', 'atletico', 'deportiva',
    #     'tarjeta', 'sporting', 'balompie', 'arbitro', 'leganes', 'oviedo', 'red', 'girona', 'groga', 'real'
    # }
    keywords = {'espanyol', 'liga', 'campeones', 'rcde', 'español', 'camp', 'nou', 'barcelona', 'estadi', 'estadio',
                'club', 'futbol', 'partido', 'madrid', 'liga', 'clasico', 'goles', 'gol', 'barça', 'final',
                'real', 'villarreal', 'targeta', 'campeon'}
    # sparser(keywords)
    occurrence_count(keywords)
