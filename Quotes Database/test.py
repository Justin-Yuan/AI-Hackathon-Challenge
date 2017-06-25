import json
import numpy as np
import pickle
import pandas as pd

# Read dictionaries
with open('quotes_analysis_results.p', 'rb') as infile:
    data = pickle.load(infile)
quotes = data['quotes']
emotions = data['emotions_in_quotes']
likes = data['likes']
tags = data['tags']

print()
print()
print("Total number of quotes: ")
print(len(quotes))
print()
for i in range(3):
    quote = quotes[i]
    print("Sample Quotes: ")
    print(quote)
    print("Emotions in the sample quotes")
    print(emotions[quote])
    print("Likes in the sample quotes")
    print(likes[quote])
    print("Tags in the sample quotes")
    print(tags[quote])
    print()
    print()