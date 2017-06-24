import json
import numpy as np
import pickle
import pandas as pd

# Read dictionaries
with open('mapping_dictionaries.p', 'rb') as infile:
    mappings = pickle.load(infile)
words = mappings['words'] # keywords list
emotions = mappings['emotions'] # emotions list
word2emotions = mappings['words2emotions'] # Read all related emotions with a given words

# Read the file
file_path = 'goodread_quotes_1.json' 
quotes_list = json.loads(open(file_path).read())
len_quotes_list = len(quotes_list)


quotes = []
for i in range(len_quotes_list):
    quotes.append(quotes_list[i]['text'].replace('\n',''))

quotes2tags = {quotes[i]:[] for i in range(len_quotes_list)}
quotes2like = {quotes[i]:[] for i in range(len_quotes_list)}
quotes2emotions = {quotes[i]:[] for i in range(len_quotes_list)}

for i in range(len_quotes_list):
    quote = quotes_list[i] # Read a quote
    tags = quote['tags'] # Read tags in the quote
    like = [int(s) for s in quote['likes'].split() if s.isdigit()][0] # get the number of likes
    # text = quote['text'].replace('\n','') # Get the text, remove '\n'

    # Analyze tags: if a tag is a keyword, find its corresponding emotion, and
    emotions_in_quote = [] # initialize a list
    for tag in tags:
        if tag in words:
            emotions_in_word = word2emotions[tag] # find all corresponding emotions
            for emotion_in_word in emotions_in_word:
                emotions_in_quote.append(emotion_in_word)
    # Save all variables

    quotes2tags[quotes[i]].append(tags)
    quotes2like[quotes[i]].append(like)
    quotes2emotions[quotes[i]].append(emotions_in_quote)


with open('quotes_analysis_results.p', 'wb') as outfile:
   pickle.dump({"quotes":quotes, "tags":quotes2tags,"likes":quotes2like,"emotions_in_quotes":quotes2emotions}, outfile)