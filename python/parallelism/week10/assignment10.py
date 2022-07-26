"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Norman Tangedal
Purpose: assignment for week 10 - reader writer problem
Instructions:
- Review TODO comments
- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)
- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  
  
- Display the numbers received by the reader printing them to the console.
- Create WRITERS writer processes
- Create READERS reader processes


- You can use sleep() statements for any process.
- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.
- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment
- Not allowed to use Queue(), Pipe(), List() or any other data structure.
- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.
Add any comments for me:
"""
from ast import arg
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp
import time
from xml.dom.minidom import Element

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2
HEAD = 0
TAIL = -1
COUNT = 0

def main():

    # This is the number of values that the writer will send to the reader
    items_list = []
    for i in range(20, 30):
      items_to_send = random.randint(1000, 10000)
      items_list.append(items_to_send)
    print(items_list)
    items_to_send = random.randint(1000, 10000)
    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    sm = smm.SharedMemory(items_list)
    
  
    def writeElements(sm, element):
      index = (TAIL + 1) % BUFFER_SIZE
      COUNT = COUNT + 1
      if(index == BUFFER_SIZE):
        index = 0
      items_list[index] = element
      TAIL = TAIL + 1
      
      
    def readElements(sm):
      if(BUFFER_SIZE == 0):
        print("The Buffer is Empty ")
      index = HEAD % BUFFER_SIZE
      element = items_list[index]
      HEAD = HEAD + 1
      COUNT = COUNT - 1
      return element
   
    def check_for_empty():
      index = HEAD % BUFFER_SIZE
      element = items_list[index]
      return element

    # def is_empty():
    #   return BUFFER_SIZE == 0

    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    # Locks for the writers
    writelock1 = mp.Lock()
    writelock2 = mp.Lock()
    # Locks for the readers
    readlock1 = mp.Lock()
    readlock2 = mp.Lock()
    # Semaphore for when needed
    sem = mp.Semaphore()

    
    # Delete an element, or remove element
    # items_list.pop()
  

    # TODO - create reader and writer processes
    read = mp.Process(target=readElements, args=(sm,))
    write = mp.Process(target=writeElements, args=(sm, items_list))
    
    # TODO - Start the processes and wait for them to finish
    read.start()
    write.start()
    read.join()
    write.join()
    

    print(f'{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    print(f'{COUNT} values received')

    smm.shutdown()


if __name__ == '__main__':
    main()