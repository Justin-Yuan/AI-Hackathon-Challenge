""" 
Image Analyzer using Microsoft Azure Computer Vision and Emotion API
Created by Justin Yuan, June 24, 2017
Global AI Hackathon 
"""

from __future__ import print_function
import time 
import requests
# import cv2
import operator
import numpy as np


class ImageAnalyzer(object):
    """ A analyzer for images, decodes information on emotions and context from the image 

    Usage Example:
        # initialize an empty ImageAnalyzer
        imgAnalyzer = ImageAnalyer()

        img_path = ...

        # get emotion related info
        length, top_sorted_results = imgAnalyzer.decode_emotion(img_path)

        # get context related info 
        title, description, keywords = imgAnalyzer.decode_context(img_path)
    """

    def __init__(self, url=None, key=None, max_entry=10):
        self._url = url
        self._key = key
        self._maxNumRetries = max_entry

        self.data = None 

        self._headers = dict()
        self._headers['Ocp-Apim-Subscription-Key'] = self._key
        self._headers['Content-Type'] = 'application/octet-stream'

        self._json = None
        self._params = {
            # Request parameters. All of them are optional.
            'visualFeatures': 'Categories,Description,Color',
            'language': 'en',
        }
        
    def set_url(self, emotion=True, context=False, url=None):
        if emotion:
            self._url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
        elif context:
            self._url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze'
        elif url:
            self._url = url  

    def set_key(self, emotion=True, context=False, key=None):
        if emotion:
            self._key = 'ab7ce6eb315b40a4a9fece00b4d61727'
        elif context:
            self._key = '25b9fed816544981a50c0f520214a178'
        elif url:
            self._key = key  

    def set_data(self, path):
        with open( path, 'rb' ) as f:
            self.data = f.read()

    def set_headers_key(self, other_key=None):
        self._headers['Ocp-Apim-Subscription-Key'] = self._key if not other_key else other_key
    

    def processRequest(self, json, data, headers, params, url ):
        """
        Helper function to process the request to Project Oxford

        Parameters:
        json: Used when processing images from its URL. See API Documentation
        data: Used when processing image read from disk. See API Documentation
        headers: Used to pass the key information and the data type request
        """
        retries = 0
        result = None

        while True:

            # response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )
            response = requests.request( 'post', url, json = json, data = data, headers = headers, params = params )
            if response.status_code == 429: 

                print( "Message: %s" % ( response.json()['error']['message'] ) )

                if retries <= _maxNumRetries: 
                    time.sleep(1) 
                    retries += 1
                    continue
                else: 
                    print( 'Error: failed after retrying!' )
                    break

            elif response.status_code == 200 or response.status_code == 201:

                if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                    result = None 
                elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                    if 'application/json' in response.headers['content-type'].lower(): 
                        result = response.json() if response.content else None 
                    elif 'image' in response.headers['content-type'].lower(): 
                        result = response.content
            else:
                print( "Error code: %d" % ( response.status_code ) )
                print( "Message: %s" % ( response.json()['error']['message'] ) )

            break
            
        return result


    def get_emotion(self, path):
        """ return a list of json objects for the emotions in the image 

        Arguments:
            path: image path, a string

        Returns:
            result -> [json obj1, json obj2, ...] 
                json obj -> {'scores': {'sadness': , 'fear': , ...},
                            'facecRectangle':{'top': , 'left': , 'width': , 'height': }}
        """
        self.set_data(path)

        self.set_key(emotion=True)
        self.set_url(emotion=True)
        self.set_headers_key()

        result = self.processRequest( self._json, self.data, self._headers, self._params, self._url ) 
        return result 


    def get_context(self, path):
        """ return a single json object for the image context

        Arguments:
            path: image path, a string

        Returns:
            result -> {'metadata': , 'color': , 'requestId': , 'description': , 'categories': }
                metadata -> {'height': , 'width': , 'format': }
                color -> {'dominantColors':['White', ...],
                            'accentColor': '...', 
                            'dominantColorBackground: '...'
                            'isBWImg': boolean,
                            'dominantColorForeground': '...'}
                requestedId: string 
                description: {'captions': , 'tags': }
                    captions -> [{'confidence': float, 'text': string (a complete description) }]
                    tages -> [string1, string2, ...]
                categories: [{'name': string (a short title), 'score': float}]
        """
        self.set_data(path)

        self.set_key(emotion=False, context=True)
        self.set_url(emotion=False, context=True)
        self.set_headers_key()    

        result = self.processRequest( self._json, self.data, self._headers, self._params, self._url )
        return result 


    def decode_emotion(self, path, top=7):
        """ decode the given image with emotion related information

        Arguments:
            path: image path, a string
            top: the top sentiments you want, an integer

        Returns:
            length: an integer 
            top_sorted_results: a list of emotional objects detected, each element is a list of tuples of the top sentiments
        """
        results = self.get_emotion(path)
        length = len(results)
        if length == 0:
            return length, []
        else:
            sorted_results = [sorted(result['scores'].items(), key=lambda x: x[1], reverse=True) for result in results]
            top_sorted_results = [sorted_result[:top] for sorted_result in sorted_results]
            return length, top_sorted_results


    def decode_context(self, path):
        """ decode the given image with context related information 

        Arguments:
            path: image path, a string 

        Returns:
            title: a string
            description: a string
            keywords: a list of strings
        """
        results = self.get_context(path)
        title = results['categories'][0]['name']
        description = results['description']['captions'][0]['text']
        keywords = results['description']['tags']
        return title, description, keywords



    