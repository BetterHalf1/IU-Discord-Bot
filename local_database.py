import random

#stores functions that returns items in a list

def getFlipCoinResponse():
  lst = ["it's a no kids zone!", "born to be a gambler!", "can't die I'm all in."
  , "worth more than jewels."]
  return random.choice(lst)