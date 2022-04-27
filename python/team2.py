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
count = 0

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    # All calls through the internet sgould be called through a thread

    def __init__(self, url):
        pass#create these


    def run(self):
        pass#create these


     
   

    def thread_func(filename, count):
        # acquire the lock before entering the critical section
        # If another thread has the lock, this thread will wait
        # until it's released.
        global lock
        lock.acquire()
    
        # Do your stuff.  Only 1 thread is running this code
        f = open(filename, 'w')
        f.write(count)
        f.close()

        # release the lock.  If you fail to release the lock,
        # the next thread that tried to acquire the lock will
        # wait forever since the release will never happen.
        lock.release()


class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
    # TODO - add call to reshuffle
    #make a call to the website, and if the object is not empty, continue
        pass#request start and join thread


    def draw_card(self):
        # TODO add call to get a card
        #thread_func(filename, count)
        #request, then start, and join,
        #if response is not {} request remaining and return request response
        
        
        
        
        pass

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