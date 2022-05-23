"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau
Purpose: Team Activity
Instructions:
- See in I-Learn
"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue


def retrieve_thread():  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        url = url_q.get()
        if url == NO_MORE_VALUES:
            break
        # TODO process the value retrieved from the queue

        # TODO make Internet call to get characters name and log it
        pass



def file_reader(log, url_q): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    with open('urls.txt') as f:
        for line in f:
            line = line.strip()
            url_q.put(line)
    # TODO Open the data file "urls.txt" and place items into a queue

    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"
    for i in range(RETRIEVE_THREADS):
        url_q.put(NO_MORE_VALUES)


def main():
    """ Main function """

    log = Log(show_terminal=True)
    url_q = queue.Queue()
    
    reader = threading.Thread(target=file_reader, args=(log, url_q))
    processes = []
    for u in range:
        processor = threading.Thread(target= retrieve_thread, args=())
        processes.append(processor)

    
    # TODO create queue
    # TODO create semaphore (if needed)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job

    log.start_timer()
    reader.start()
    for t in processes:
        t.start()


    # TODO Get them going - start the retrieve_threads first, then file_reader

    # TODO Wait for them to finish - The order doesn't matter
    for t in processes:
        t.join()
    reader.join()

    log.stop_timer('Time to process all URLS')



if __name__ == '__main__':
    main()


