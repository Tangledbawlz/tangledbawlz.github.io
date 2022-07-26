"""
Course: CSE 251
Lesson Week: 04
File: assignment4.py
Author: Norman Tangedal
Purpose: Assignment 04 - Factory and Dealership
Instructions:
- See I-Learn
"""

from multiprocessing import Semaphore
import queue
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50
q = queue.Queue()
sem1 = Semaphore()
sem2 = Semaphore()

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread, sem1, sem2, q):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self):
        # TODO, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        car = Car().car_models
        car = Car().car_years
        car = Car().car_makes
        car = Car().display
        

    def run(self):
        for i in range(CARS_TO_PRODUCE):
            # TODO Add you code here
            """
            create a car
            place the car on the queue
            signal the dealer that there is a car on the queue
           """
            car = Car()
            dealer = Dealer()
            q = queue.Queue()
        # for i in range(CARS_TO_PRODUCE):
        #     car.__new__()
        
        # for dealer in car.__sizeof__:
        #     sem1.acquire()
            

        # signal the dealer that there there are not more cars
        sem2.acquire()
        
        sem2.release()

class Dealer(threading.Thread, q):
    """ This is a dealer that receives cars """

    def __init__(self):
        # TODO, you need to add arguments that pass all of data that 1 Dealer needs
        # to sell a car
        t = threading.Thread(target=Factory())

    def run(self):
        while q.empty is False:
            # TODO Add your code here
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """
            factory = Factory()

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))



def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s)
    sem1 = Semaphore()
    sem2 = Semaphore()
    # TODO Create queue251 
    q = queue.Queue()
    # TODO Create lock(s) ?

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # TODO create your one factory
    factory = Factory(sem1, sem2, q)

    # TODO create your one dealership
    dealer = Dealer()

    log.start_timer()

    # TODO Start factory and dealership
    dealer.start()
    factory.start()

    # TODO Wait for factory and dealership to complete
    dealer.join()
    factory.join()

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()