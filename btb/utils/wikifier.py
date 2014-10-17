'''
Created on Oct 6, 2014

@author: carlosm
'''
import pycurl
import json
from StringIO import StringIO
from urllib import urlencode

def wikify(chunk, prob=0.5):
    '''
    Use the wikipedia-miner web service to convert a given chunk of text into 
    a set of topics. Each topic is associated with a probability of the word being 
    a link to Wikipedia. Only topics with probability greater than a given 
    probability threshold are returned.
    
    Topics and their probabilities are returned in a { topic: probability } dictionary.
    
    Parameters:
       chunk     The chunk of text to be converted.
       prob      The minimum probability threshould.
    
    Returns:
       A dictionary of topics with their associated probabilities of being a link.
    '''
    wikifyURL = 'http://wikipedia-miner.cms.waikato.ac.nz/services/wikify'

    c = pycurl.Curl()
    c.setopt(c.URL, wikifyURL)
    buff = StringIO()

    post_data = {'responseFormat': 'json',
                 'minProbability': prob,
                 'source': chunk}

    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEFUNCTION, buff.write)
    c.perform()
    c.close()

    body = buff.getvalue()
    response = json.loads(body)
    return { topic['title']: topic['weight'] for topic in response['detectedTopics'] }
