"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Norman Tangedal

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

What I tried doing was to use the global variable "Stop" to make all the strings stop the moment one of them reached the end. I had a lot of trouble getting the 
threads to work, instead the program hits every possible path on the maze and then returns to the starting position. I could change the program in the future to be able
to use each thread to find the ends. I can also use the thread count to return how many threads were created, and hopefully end the program after finding the end.


Why would it work?

It could work because the threading class uses global variables to communicate between the threads. It would also return the number of threads used in the first place,
and by using the "Stop," we would be able to stop the program.

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 common Python files - Dont change
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them

    # create a variable for the path
    path = []
    threads = []
    
    # check to see if the spots are available and open 
    # Find start position
    position = maze.get_start_pos() 
    # label x and y coordinates
    x, y = position
    # create x and y variables for the position
    path.append(position)
    
    # if space is free, move here
    if maze.can_move_here(x, y) and maze.get_possible_moves(x, y):
        #move to next value in index 
        maze.move(x, y, COLOR)
        #recursive call to go through maze
    def move_through():
        nonlocal path
        nonlocal maze
        global stop
        # t = threading.Thread(target=move_through(), args=())
        # threads.append(t)
        # for i in range(threads):
        #     i.start()
        
        x, y = path[-1]
        if maze.at_end(x,y):
            return 
        next_move = maze.get_possible_moves(x, y)
        for possible in next_move:
            new_color = get_color()
            row, col = possible
            if maze.can_move_here(row, col):
                path.append(possible)
                maze.move(row, col, new_color)
                move_through()
            if maze.at_end(row, col):
                return maze.get_possible_moves(row, col)
            if maze.get_possible_moves(row, col):
                maze.can_move_here(row, col)
                path.append(possible)
                maze.move(row, col, new_color)
                move_through()
            if not maze.get_possible_moves(row, col):
                maze.restore(row, col)
            else:
                return
        
    move_through()   
    # for i in range(threads):
    #         i.join()  
    return path
    


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()