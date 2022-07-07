"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""
import os
import threading
import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 15

# Run program for this number of seconds
TIME = 5

STARTING_PARTY_MESSAGE =  '\nTurning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^\n'

STARTING_CLEANING_MESSAGE =  '\nStarting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'

CLEAN_LOCK = threading.Lock() # Lock for cleaners to prevent guests entry
GUEST_LOCK = threading.Lock() # Light switch


cleaned_count = 0
party_count = 0

'''
cg
claim definition:
00 --> cleaner can enter or guest can enter 
10 --> neither can enter
01 --> on First guest, light on. Guests can enter or leave
11 --> not possible/error

release definition:
00 --> neither can 
01 --> Guests can leave turn lights off
10 --> cleaner can leave
11 --> not possible

'''


def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))

def cleaner():
    """
    do the following for TIME seconds
    cleaner will wait to try to clean the room (cleaner_waiting())
    get access to the room
    display message STARTING_CLEANING_MESSAGE
    Take some time cleaning (cleaner_cleaning())
    display message STOPPING_CLEANING_MESSAGE
    """
   
    while True:
        cleaner_waiting()
        # check if cleaner can enter room if yes, claim room
        if(not GUEST_LOCK.locked() and not CLEAN_LOCK.locked()):
            # Lock room to cleaner
            CLEAN_LOCK.acquire()
            # Print message
            print(STARTING_CLEANING_MESSAGE)
            # Returns cleaner PID
            cleaner_cleaning(os.getpid())
            # Stop message
            print(STOPPING_CLEANING_MESSAGE)
            # Release lock
            CLEAN_LOCK.release()
            
 


def guest():
    global party_count
    """
    do the following for TIME seconds
    guest will wait to try to get access to the room (guest_waiting())
    get access to the room
    display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
    Take some time partying (guest_partying())
    display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """ 
    while True:
        guest_waiting()
        # if the room is not being cleaned
        if(not CLEAN_LOCK.locked()):
            # lock the Cleaners from entering
            GUEST_LOCK.acquire()
            # Guests turn the light on
            print(STARTING_PARTY_MESSAGE)
            # Get the ID of the guests entering
            while(GUEST_LOCK.locked() and not CLEAN_LOCK.locked()):
                guest_partying(os.getpid())
                # Increment the global variable for party count
                party_count += 1
            # Closing party and turn off lights
            print(STOPPING_PARTY_MESSAGE)
            # unlock room
            GUEST_LOCK.release()
            
    

def main():
    cleaner_list = [] 
    guest_list = []
    global party_count
    global cleaned_count
    
    # TODO - add any variables, data structures, processes you need
    
    for i in range(CLEANING_STAFF):
        cleaning_process = mp.Process(target=cleaner)
        cleaning_process.start()
        cleaner_list.append(cleaning_process)
        
    time.sleep(TIME)

    for cleaning_process in cleaner_list:
        cleaning_process.terminate()
    

    for i in range(HOTEL_GUESTS):
        guest_process = mp.Process(target=guest)
        guest_process.start()
        guest_list.append(guest_process)

    time.sleep(TIME)

    for guest_process in guest_list:
        guest_process.terminate()

    # Results
    print(f'Room was cleaned {cleaned_count} times, there were {party_count} parties')


if __name__ == '__main__':
    main()