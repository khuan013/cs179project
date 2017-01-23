#! twitter/bin/python3

import tweepy
import time, sys, json

# constants
TIME_LIMIT = 2

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

# modified version of the basic StreamListener from Tweepy
class JSONStream(tweepy.StreamListener):
    def __init__(self):
        self.timeStart = time.time()
        self.timeLimit = 60 * TIME_LIMIT
        super(JSONStream, self).__init__()

    def on_status(self, status):
        if (time.time() - self.timeStart) < self.timeLimit:
            print(json.dumps(status._json))
        else:
            return False

if __name__ == "__main__":

    # authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # gather current trends in the US
    rawTrends = api.trends_place(id=2442047)
    trends = list()
    sys.stderr.write("Currently trending topics:\n")
    for trend in rawTrends[0]["trends"]:
        trends.append(trend["name"])
        sys.stderr.write("\t> " + trend["name"] + "\n")

    # gather tweets until time runs out
    jsonstream = JSONStream()
    stream = tweepy.Stream(auth=api.auth, listener=jsonstream)
    sys.stderr.write("\nCollecting tweets for " + str(TIME_LIMIT) + " minutes... ")
    stream.filter(track=trends)
    sys.stderr.write("Done!\n")
