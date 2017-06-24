""" 
MemeRanker using labelled scripts dataset from goodreads 
Created by Justin Yuan, June 24, 2017
Global AI Hackathon 
"""

import pickle 
import math 


class MemeRanker(object):
    """ Generate ranked memes/captions for images

    database format:
        { line: dict of attributes (sentiment scores, keywords, likes) } 
    """

    def __init__(self, file_path):
        # load in the movie/goodread lines
        self._database = None
        self.load_dataset(file_path)


    def load_dataset(self, path):
        with open('path', 'rb') as infile:
            self._database = pickle.load(infile)


    def get_sentiment_similarity(self, query, candidate_line):
        pass 

    
    def get_context_similarity(self, query, candidate_line, metric='intersection'):
        pass 


    def rank_by_upvotes(self, candidate_line):
        pass 


    def recommend_lines(self, query):
        pass 