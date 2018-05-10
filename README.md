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

## About football fields detection

Image processing for the detection of the football fields is done with the opencv library for python. The library numpy is also used to create arrays. 

The goal of the image processing is to detect several football fields from several images around the area of Barcelona. Once the football fields are detected, their longitude and latitude coordinates are calculated and stored in a dictionary, so that later, tweets can be found in these locations.

Since we have to get many images at once and process them, the image processing is parallelized using Spark. The steps are the following:

  - Get the satellite images around the area of Barcelona using owslib.
  - Apply a green colour filter to find the forms of the football field.
  - Apply a canny edge detector to get the edges of the green forms.
  - Filter the contours, by shape (number of corners should be 4) and area.
  - Get the coordinates (longitude and latitude), by doing conversions (pixels to meters, and meters to degrees). This                  is done using the pyproj library.

All the functions related to image processing are in the image_proc.py script. The parallelization of the image gathering and processing, as well as the location collection in a dictionary is done in the location_finder.py script.
