import requests
import json
import random
import os
# set the apikey and limit
def getGif(arg):
  lmt = 8

  # our test search
  search_term = str(arg)

  # get random results using default locale of EN_US
  r = requests.get(
      "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, os.environ['apikey'], lmt))

  if r.status_code == 200:
      # load the GIFs using the urls for the smaller GIF sizes
      data = json.loads(r.content)
      gif = random.choice(data["results"])
      return gif['media'][0]['gif']['url']
  else:
      return