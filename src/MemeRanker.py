""" 
MemeRanker using labelled scripts dataset from goodreads 
Created by Justin Yuan, June 24, 2017
Global AI Hackathon 
"""

import pickle 
import math 
import numpy as np 


class MemeRanker(object):
    """ Generate ranked memes/captions for images

    Formats:
        database: { line: dict of attributes (sentiment scores, keywords, likes) } 
        query: a dictionary of input attributes { length, top_sorted_results, title, description, keywords } 
    
    """

    def __init__(self, file_path, cut_off_length=50):
        # load in the movie/goodread lines
        self._database = None
        self.load_dataset(file_path) # Load the quotes file

        self.cut_off_length = 25 # Over 50 char is not desired
        self.length_weight = 5
        self.sentiment_weight = 50 
        
        self.context_weight = 10
        self.like_weight = 0.05

        self.sentiment_list = []

        self.emotions_in_quotes = {}
        self.tally_dataset_sentiments()

        self.likes = {}
        self.normalize_likes()

    def load_dataset(self, path):
        with open(path, 'rb') as infile:
            self._database = pickle.load(infile)

    def tally_dataset_sentiments(self):
        """ load the "emotions in quotes" into format {quote:{sentiment:score, ...}, ...}
        """
        temp_dict = {}
        for key in self._database['emotions_in_quotes']: # Each key is a quote
            temp_dict[key] = {'sadness':0, 'contempt':0, 'neutral':0, 'happiness':0, 'surprise':0, 'fear':0, 'disgust':0, 'anger':0}
            each_key_count = 0
            for sent in self._database['emotions_in_quotes'][key][0]:
                if sent[-1] == " ":
                    temp_sent = sent[:-1]
                    temp_dict[key][temp_sent] += 1
                else:
                    temp_dict[key][sent] += 1
                each_key_count += 1
            for sent in temp_dict[key]:
                # there are items with no sentiment? 
                temp_dict[key][sent] = temp_dict[key][sent] / (each_key_count if each_key_count!=0 else 1)
            # print("one pass succeeded")
        self.emotions_in_quotes = temp_dict
            
    def set_sentiment_weight(self, new_sentiment_weight):
        self.sentiment_weight = new_sentiment_weight

    def set_context_weight(self, new_context_weight):
        self.context_weight = new_context_weight
    
    def set_like_weight(self, new_like_weight):
        self.like_weight = new_like_weight

    def set_length_weight(self, new_length_weight):
        self.length_weight = new_length_weight 

    def cut_off_regularizer(self, length):
        """
        To be checked: 
        """
        return 1 if length < self.cut_off_length else 0

    def length_regularizer(self, length):
        """
        """
        return self.length_weight * length if length < self.cut_off_length else 0 

    def set_sentiment_list(self, query):
        self.sentiment_list = query['top_sorted_results']

    def rescale_sentiment(self, sentiment):
        """ rescale sentiment values to a range 0~1, cut off values that are too small
        """
        value_list = [item[1] if item[1] > 0.0005 else 0 for item in sentiment]
        value_sum = sum(value_list)
        value_list = [value/value_sum for value in value_list]
        return [(sentiment[i][0], value_list[i]) for i in range(len(value_list))]
    
    def rescale_sentiment_list(self):
        self.sentiment_list = [self.rescale_sentiment(sentiment) for sentiment in self.sentiment_list]

    def merge_sentiment_list(self):
        # squared_sentiment_list = [[(item[0], (item[1]*10)**2) for item in sentiment] for sentiment in self.sentiment_list]
        squared_sentiment_list = [(item[0], (item[1]*10)**2) for sentiment in self.sentiment_list for item in sentiment]
        temp_normalized_sentiment_dict = {}
        for item in squared_sentiment_list:
            if item[0] not in temp_normalized_sentiment_dict:
                temp_normalized_sentiment_dict[item[0]] = item[1]
            else:
                temp_normalized_sentiment_dict[item[0]] += item[1]
        squared_value_sum = sum([temp_normalized_sentiment_dict[key] for key in temp_normalized_sentiment_dict])
        normalized_sentiment_list = [(key, temp_normalized_sentiment_dict[key]/squared_value_sum) for key in temp_normalized_sentiment_dict]
        self.sentiment_list  = normalized_sentiment_list

    def normalize_likes(self):
        likes_dict = {}
        total = 0
        for line in self._database['quotes']:
            likes_dict[line] = self._database['likes'][line][0]
            total += self._database['likes'][line][0]
        for line in self._database['quotes']:
            likes_dict[line] = likes_dict[line] / total 
        self.likes = likes_dict

    def get_sentiment_similarity(self, query_sentiments, candidate_line, metric="euclidean"):
        """
        """
        score = 0
        # print(query_sentiments)
        # print(candidate_line)
        if metric == "euclidean":
            score += sum([math.pow(item[1]-self.emotions_in_quotes[candidate_line][item[0]], 2.0) for item in query_sentiments])     
            # score += sum([math.pow(item[1]-self._database[candidate_line]['sentiments'][item[0]], 2.0) for item in query_sentiments.items()])     
        elif metric == "weighted":
            score += sum([item[1] * math.pow(item[1]-self.emotions_in_quotes[candidate_line][item[0]], 2.0) for item in query_sentiments]) 
            # score += sum([item[1]*math.pow(item[1]-self._database[candidate_line]['sentiments'][item[0]], 2.0) for item in query_sentiments.items()])     
        return score 
    

    def get_context_similarity(self, query, candidate_line, metric='content'):
        """
        """
        score = 0
        if metric == 'content':
            temp = candidate_line.split(' ')
            score +=  len(set(query['keywords']) & set(temp)) / len(temp) * self.cut_off_regularizer(len(temp)) - self.length_regularizer(len(temp))
        elif metric == 'semantic':
            pass  # thinking of using word2vec here 
        return score 

     
    def get_rank_score(self, query, candidate_line):
        """
        """
        rank_score = 0
        rank_score += self.sentiment_weight * self.get_sentiment_similarity(self.sentiment_list, candidate_line, metric="weighted")
        rank_score += self.context_weight * self.get_context_similarity(query, candidate_line)
        rank_score += self.like_weight * self.likes[candidate_line]
        return rank_score


    def recommend_lines(self, query, top=3):
        """
        """
        self.set_sentiment_list(query)
        self.rescale_sentiment_list()
        self.merge_sentiment_list()

        ranks = []
        count = 0
        total = 0

        for line in self._database['quotes']:
            score = self.get_rank_score(query, line)
            if count < top:
                count += 1
                ranks.append((line, score))
                ranks.sort(key=lambda x: x[1], reverse=False)
            else:
                for pair in ranks:
                    # print("next")
                    if pair[1] < score:
                        ranks[0] = (line, score)
                        ranks.sort(key=lambda x: x[1], reverse=False)
                        break 
            # print("finding next line ")
            # print(ranks)
            total += 1
        
        return ranks 

            


        