import json
import numpy as np
import pickle
import pandas as pd

def read_dic_mappings(file_path):
    """
    This function reads the supporting dictionary files from the given file_path
    """
    with open(file_path, 'rb') as infile:
        mappings = pickle.load(infile)
    words = mappings['words'] # keywords list
    emotions = mappings['emotions'] # emotions list
    word2emotions = mappings['words2emotions'] # Read all related emotions with a given words
    return words, emotions, word2emotions

# Read the file
def read_quotes(file_path,words,emotions,word2emotions):
    '''
    Read a json file of quotes and output the 
    '''
    quotes = [] #  A list to save the text of quotes
    print("Start reading: " + file_path)
    quotes_list = json.loads(open(file_path).read())
    

    for i in range(len(quotes_list)):
        quote = quotes_list[i]['text'].replace('\n','').strip().replace('“','').replace('”','')
        if quote != '':
            quotes.append(quote)

    len_quotes_list = len(quotes)
    quotes2tags = {quotes[i]:[] for i in range(len_quotes_list)}
    quotes2like = {quotes[i]:[] for i in range(len_quotes_list)}
    quotes2emotions = {quotes[i]:[] for i in range(len_quotes_list)}

    for i in range(len_quotes_list):
        quote = quotes_list[i] # Read a quote
        tags = quote['tags'] # Read tags in the quote
        like = [int(s) for s in quote['likes'].split() if s.isdigit()][0] # get the number of likes
        # text = quote['text'].replace('\n','').strip().replace('“','').replace('”','') # Get the text, remove '\n'

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
    return quotes, quotes2tags,quotes2like,quotes2emotions

def read_quotes_file(quote_file_path,dic_file_path,output_file_path):

    words, emotions, word2emotions = read_dic_mappings(dic_file_path)

    quotes, tags,likes,emotions_in_quotes = read_quotes(quote_file_path,words,emotions,word2emotions)
    print("Finish read: " +quote_file_path)

    with open('quotes_analysis_results.p', 'wb') as outfile:
        pickle.dump({"quotes":quotes, "tags":tags,"likes":likes,"emotions_in_quotes":emotions_in_quotes}, outfile)
    
    print("All the data have been saved!")

dictionary_path ='mapping_dictionaries.p'
file1 = 'goodread_quotes_1.json' 
output_path1 = 'quotes_analysis_results.p'
read_quotes_file(file1,dictionary_path,output_path1)


file2 = 'goodread_quotes_2.json'
output_path2 = 'quotes_analysis_results2.p'
read_quotes_file(file2,dictionary_path,output_path2)