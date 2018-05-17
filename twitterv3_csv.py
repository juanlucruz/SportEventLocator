from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import csv
import random


consumer_key=""
consumer_secret=""

access_token=""
access_token_secret=""



Coords = dict()
XY = []


csvfile = open('geopy_results.csv','wb')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['UserID', 'Date', 'Lat', 'Long', 'Text'])

class StdOutListener(StreamListener):

                def on_status(self, status):
                                
                                text = status.text
                                
                                try:
                                    Coords.update(status.coordinates)
                                    XY = (Coords.get('coordinates'))  #Place the coordinates values into a list 'XY'

                                except:

                                    Box = status.place.bounding_box.coordinates[0]                                    
                                    XY = [(Box[0][0] + Box[2][0])/2, (Box[0][1] + Box[2][1])/2]
 
                                    pass
                                
                               
                                csvwriter.writerow([unicode(status.id_str).encode("utf-8"),unicode(status.created_at).encode("utf-8"),XY[1],XY[0],unicode(status.text).encode("utf-8")])
                      

def main():
    l = StdOutListener()    
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, timeout=30.0)

    while True:
        try:

            stream.filter(locations=[2.006981,41.308702,2.33325,41.47628], async=False)##These coordinates are approximate bounding box around BCN
            #stream.filter(track=['obama'])## This will feed the stream all mentions of 'keyword' 
            break
        except Exception as e:
             # Abnormal exit: Reconnect
             nsecs=random.randint(60,63)
             time.sleep(nsecs)            

if __name__ == '__main__':
	main()
