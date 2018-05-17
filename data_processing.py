import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('geopy_results_1526571264.8801005.csv', )
df.head(n=20000).plot.scatter(x='Long', y='Lat', c='DarkBlue')
plt.show()
