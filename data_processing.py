import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

field_locations = pd.read_csv('locations.csv')
del field_locations['ID']
# print(list(field_locations.values))
df = pd.read_csv('final_results_clean.csv', )
print((df.head()))
# club_df = df[df['Text'].str.contains("club")]

a = df['Text'].tolist()
char_type = [str(type(msg)) for msg in a]

# hist, bin_edges = np.histogram(char_type, density=True)
# plt.figure()
# plt.plot(hist, bin_edges)

# print((club_df.head()))
# club_df.plot.scatter(x='Long',y='Lat',c='DarkBlue')
# for row in df:

plt.show()
