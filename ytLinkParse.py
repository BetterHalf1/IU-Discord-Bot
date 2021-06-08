# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 16:02:17 2021

@author: kenne
"""

import urllib.request
import re

user_input = input("What song?")
search_keyword = user_input.replace(" ", "+")
html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
print("https://www.youtube.com/watch?v=" + video_ids[0])

pattern = 'abc'
string = 'abcdefabcab'
result = re.findall(pattern, string)
print(result)
#print("http://www.youtube.com/watch?v=" + video_ids[0])