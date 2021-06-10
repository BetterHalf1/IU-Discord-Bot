# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 11:08:16 2021

@author: kenne
"""
import requests
import json
import random
# set the apikey and limit
apikey = "AYSR5937VAN9"  # test value
lmt = 15

# our test search
search_term = "iu"

# get random results using default locale of EN_US
r = requests.get(
    "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
    data = json.loads(r.content)
    gif = random.choice(data["results"])
    print(gif)
    print(gif['media'][0]['gif']['url'])
else:
    top_8gifs = None


# continue a similar pattern until the user makes a selection or starts a new search.
