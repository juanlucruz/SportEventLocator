import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

field_locations = pd.read_csv('locations.csv')
del field_locations['ID']
# print(list(field_locations.values))
df = pd.read_csv('geopy_results_1527171096.641982.csv', )
# df = pd.read_csv('occurrences.csv', )
# print(df.head())
# keywords = {
#     'tarragona', 'pase', 'tiro', 'español', 'espanyol', 'barsa', 'madrid', 'sevilla', 'zaragoza', 'lorca', 'almeria',
#     'empieza', 'lugo', 'vigo', 'agrupacion', 'soria', 'futbol', 'jugadores', 'cadiz', 'gol', 'roja', 'gimnastic',
#     'corner', 'alcorcon', 'campeones', 'balompie', 'levante', 'falta', 'partido', 'centro', 'union', 'futbol',
#     'estadi', 'gijon', 'targeta', 'pelota', 'barça', 'deportiu', 'huesca', 'saque', 'cultural', 'yellow', 'betis',
#     'rayo', 'albacete', 'alaves', 'leonesa', 'valladolid', 'liga', 'goles', 'clasico', 'estadio', 'club', 'sociedad',
#     'deportivo', 'final', 'entrada', 'eibar', 'palmas', 'celta', 'vermella', 'barcelona', 'numancia', 'cordoba',
#     'reus', 'valencia', 'campeon', 'coruña', 'vallecano', 'malaga', 'faltas', 'granada', 'athletic', 'osasuna',
#     'amarilla', 'getafe', 'penalty', 'tenerife', 'villarreal', 'atleti', 'atletico', 'deportiva', 'tarjeta',
#     'sporting', 'balompie', 'arbitro', 'leganes', 'oviedo', 'red', 'girona', 'groga', 'real'
# }
# df_dict = dict()
# df_reshaped = pd.DataFrame()
# for keyword in keywords:
#     df_dict[keyword] = df[df['word'].str.contains(keyword)]
# club_df = df[df['Text'].str.contains("club")]

# a = df['Text'].tolist()
# char_type = [str(type(msg)) for msg in a]

# hist, bin_edges = np.histogram(char_type, density=True)
# plt.figure()
# plt.plot(hist, bin_edges)

# print((club_df.head()))
# club_df.plot.scatter(x='Long',y='Lat',c='DarkBlue')
plt.figure()
df.plot.scatter(x='Long', y='Lat', c='DarkBlue')
# for row in df:

plt.show()
