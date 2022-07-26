"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau
Purpose: Check for prime values
Instructions:
- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it
"""
from ast import While, arg
from concurrent.futures import process
import time
import threading
import multiprocessing as mp
import random

#Include cse 251 common Python files
from cse251 import *
from numpy import full

PRIME_PROCESS_COUNT = 1

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function
def read_file(filename, shared_q):
    with open(filename) as f:
        for line in f:
            value = int(line)
            shared_q.put(value)

# TODO create prime_process function
def process_prime(shared_q, results, count):
    while True:
        size = shared_q.size


def create_data_txt(filename):
    with open(filename, 'w') as f:
        for _ in range(1000):
            f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'

    # Once the data file is created, you can comment out this line
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    shared_q = mp.Manager().Queue()
    primes = mp.Manager()
    count = mp.Manager.list([0] * PRIME_PROCESS_COUNT)

    empty_sem = mp.Semaphore(10)
    full_sem = mp.Semaphore(0)

    # TODO create reading thread
    reader = threading.Thread(target=read_file, args=(filename, shared_q, empty_sem, full_sem))

    # TODO create prime processes
    processes = []
    for i in range(PRIME_PROCESS_COUNT):
        p = mp.Process(target=process_prime, args=(shared_q, primes, count, empty_sem, full_sem))
        processes.append(p)

    # TODO Start them all
    for _ in processes:
        p.start()
    reader.start()
    # TODO wait for them to complete

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()