# SportEventLocator
Developed by Raül Caldera, Eric Estévez and Juan Luis de la Cruz

## Presentation
- Title
- Objectives
- Group comps
- Roles of each component -> divide the work
- Calendar

## Getting locations libs

https://pypi.org/project/pyproj/ - transform coordinates

https://pypi.org/project/OWSLib/ - get images

https://pypi.org/project/opencv-python/ - compute images

## Getting twits libs

https://pypi.org/project/twython/ - twitter API wrapper

https://pandas.pydata.org/ - data analysis

## Data parallellization

https://spark.apache.org/ - image processing parallelization

## Football fields detection

Image processing for the detection of the football fields is done with the opencv library for python. The library numpy is also used to create arrays. 

The goal of the image processing is to detect several football fields from several images around the area of Barcelona. Once the football fields are detected, their longitude and latitude coordinates are calculated and stored in a dictionary as well as in a csv file, so that later, tweets can be found in these locations.

Since we have to get many images at once and process them, the image processing is parallelized using Spark. The steps are the following:

  - Get the satellite images around the area of Barcelona using owslib.
  - Apply a green colour filter to find the forms of the football field.
  - Apply a canny edge detector to get the edges of the green forms.
  - Filter the contours, by shape (number of corners should be 4) and area.
  - Get the coordinates (longitude and latitude), by doing conversions (pixels to meters, and meters to degrees). This                  is done using the pyproj library.

All the functions related to image processing are in the image_processing.py script. The parallelization of the image gathering and processing, as well as the location collection in a dictionary is done in the location_finder.py script.

The fullmap.py has functions that allow to represent the processed locations in a Barcelona map.

## Tweet collection

The twitter_scrapper.py script contains functions to collect tweets in a specific location. The search result is saved in a csv. In order to execute this script you must obtain the credentials "CONSUMER_KEY","CONSUMER_SECRET","ACCESS_TOKEN" and "ACCESS_SECRET'" on the official twitter page.


## Tweet filtering

The tweet_filter.py script contains functions that allow to filter the tweets gathered in a csv file. It filters them by location proximity to the detected football fields. Then, a key word filtering is applied to get tweets with certain words that could have valuable information regarding football events. Finally, the occurrence of each key word in a certain range of time (e.g 30 minutes) is calculated and stored as useful data to implement the football match predictive model.




