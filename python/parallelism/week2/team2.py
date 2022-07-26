"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau
Purpose: Playing Card API calls
Instructions:
- Review instructions in I-Learn.
"""

from datetime import datetime, timedelta
from itertools import count
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *
import requests

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website
lock = threading.Lock()
filename = "https://deckofcardsapi.com/"


class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    # All calls through the internet sgould be called through a thread

    #Borrowed this portion from the solution VVVVVVVVVVV
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
    # TODO - add call to reshuffle
    #make a call to the website, and if the object is not empty, continue
    #request start and join thread
        request = Request_thread(f"http://deckofcardsapi.com/api/deck/p7mrwcc6rb03/shuffle/")
        request.start()
        request.join()



    def draw_card(self):
        # TODO add call to get a card
        #request, then start, and join,
        #if response is not {} request remaining and return request.response
        request = Request_thread()
        request.start()
        request.join()

        #request.response is making a request to a URL
        if request.response != {}:
            self.remaining = request.response['remaining']
            return request.response['cards'][0]['code']
        else:
            return ' '
        
    # def new_deck(self):
    #     request = Request_thread(f"http://deckofcardsapi.com/api/p7mrwcc6rb03/new/")
    #     reshuffle = reshuffle(self)
    #     self.remaining = reshuffle

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()



if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'p7mrwcc6rb03'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(i, card, flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<