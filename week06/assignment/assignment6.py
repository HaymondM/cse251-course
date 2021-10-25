"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Marshall Haymond
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

from math import trunc
import random
import multiprocessing as mp
import os.path
import time

# Include cse 251 common Python files - Don't change
import os, sys
sys.path.append('../../code')   # Do not change the path.
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change for the 93% """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change for the 93% """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self,conn_par,marble_c,creator_dly):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.conn_par = conn_par
        self.marble_c = marble_c
        self.creator_dly = creator_dly
    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        print("In the Marble_Creator")
        for _ in range(self.marble_c):
            random_marble = random.choice(self.colors)
            #print(random_marble)
            self.conn_par.send(random_marble)
            time.sleep(self.creator_dly)
        print("here")
        self.conn_par.send("DONE")
        self.conn_par.close()    
        



class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self,child_conn,conn_par,bag_c,bagger_d):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.child_conn = child_conn
        self.conn_par = conn_par
        self.bag_c = bag_c
        self.bagger_d = bagger_d
        #Make the bag here

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        while True:
            if self.child_conn.recv() == "DONE": #make this a var
                print('Haymond')
                break
            marbles = []
            for _ in range(self.bag_c):
                #print(self.child_conn.recv())
                marbles.append( self.child_conn.recv())
            #print(marbles)
            self.conn_par.send(marbles)
            time.sleep(self.bagger_d)
        print("here2")
        self.conn_par.send("DONE")
        self.conn_par.close()


            


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self,child_conn,conn_par,assem_d,num_gifts):
       # TODO Add any arguments and variables here
        mp.Process.__init__(self)
        self.child_conn = child_conn
        self.conn_par = conn_par
        self.assem_d = assem_d
        self.num_gifts = num_gifts
    
    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            if self.child_conn.recv() == "DONE": #Change here
                print('Marshall')
                break
            
            random_large_marble = random.choice(self.marble_names)
            marbles = self.child_conn.recv()
            large_marble = random_large_marble

            g = Gift(large_marble,marbles)
            self.conn_par.send(g)
            self.num_gifts.value += 1
            time.sleep(self.assem_d)
        self.conn_par.send("DONE")
        self.conn_par.close()


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self,child_conn,wrapper_d):
        # TODO Add any arguments and variables here
        mp.Process.__init__(self)
        self.child_conn = child_conn
        self.wrapper_d = wrapper_d

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount

            with BOXES_FILENAME as 'a':
        '''
        print("!!!!!!!")
        with open(BOXES_FILENAME, 'w') as f:
            while True:
                giftt = self.child_conn.recv()
                #print(giftt)
                if giftt == "DONE":
                    print('DONEEEEEEEE')
                    break
                print('############!')
                print(giftt)
                f.write(str(giftt))
                time.sleep(self.wrapper_d)
                


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count                = {settings[MARBLE_COUNT]}')
    log.write(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    log.write(f'settings["bag-count"]       = {settings[BAG_COUNT]}') 
    log.write(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    log.write(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    log.write(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    parent_conn_creator, child_conn__creator = mp.Pipe()
    parent_conn_bagger, child_conn__bagger = mp.Pipe()
    parent_conn_assembler, child_conn__assembler = mp.Pipe()
    # TODO create variable to be used to count the number of gifts
    num_gifts = mp.Value('i', 0)


    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    mc = Marble_Creator(parent_conn_creator,settings[MARBLE_COUNT],settings[CREATOR_DELAY]) 
    bg = Bagger(child_conn__creator,parent_conn_bagger,settings[BAG_COUNT],settings[BAGGER_DELAY])
    ab = Assembler(child_conn__bagger,parent_conn_assembler,settings[ASSEMBLER_DELAY],num_gifts)
    wr = Wrapper(child_conn__assembler,settings[WRAPPER_DELAY])  

    log.write('Starting the processes')
    # TODO add code here
    mc.start()
    bg.start()
    ab.start()
    wr.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    mc.join()
    bg.join()
    ab.join()
    wr.join()


    display_final_boxes(BOXES_FILENAME, log)

    # TODO Log the number of gifts created.
    log.write(f'Number of Gifts: {num_gifts.value}')



if __name__ == '__main__':
    main()

