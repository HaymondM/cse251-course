"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
Marshall Haymond
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 5

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

# -----------------------------------------------------------------------------
def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

# -----------------------------------------------------------------------------
def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))

# -----------------------------------------------------------------------------
def guest_waiting():
    time.sleep(random.uniform(0, 2))

# -----------------------------------------------------------------------------
def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))

# -----------------------------------------------------------------------------
def cleaner(id, start_time, sl, lock_c):
    """
    do the following for TIME seconds
    cleaner will wait to try to clean the room (cleaner_waiting())
    get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    
    while True:
        totaltime = round((time.time() - start_time), 2)
        if totaltime >= TIME:
            print(f"Party done for the cleaner {id}")
            break

        if sl[0] == 0:
            print(STARTING_CLEANING_MESSAGE)
            lock_c.acquire()
            cleaner_cleaning(id)
            sl[2] += 1
            lock_c.release()
            print(STOPPING_CLEANING_MESSAGE)


# -----------------------------------------------------------------------------
def guest(id, start_time, sl, lock_g):
    """
    do the following for TIME seconds
    guest will wait to try to get access to the room (guest_waiting())
    get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    while True:
        totaltime = round((time.time() - start_time), 2)
        if totaltime >= TIME:
            print(f'Party done for the guest {id}')
            break

        print(STARTING_PARTY_MESSAGE)
        lock_g.acquire()
        sl[0] += 1
        guest_partying(id)
        sl[1] += 1
        lock_g.release()
        sl[0] -= 1
        print(STOPPING_PARTY_MESSAGE)



# -----------------------------------------------------------------------------
def main():

    # Start time of the running of the program. 
    start_time = time.time()
    #print(start_time)

    # TODO - add any variables, data structures, processes you need
    # TODO - add any arguments to cleaner() and geust() that you need
    g_count = 0
    clean_total = 0
    party_total = 0



    sl= mp.Manager().list()
    sl.append(g_count)
    sl.append(party_total)
    sl.append(clean_total)

    lock_c = mp.Lock()
    lock_g = mp.Lock()

    processes_c = [mp.Process(target=cleaner, args=(i,start_time, sl, lock_c)) for i in range(CLEANING_STAFF)]
    processes_g = [mp.Process(target=guest, args=(i,start_time, sl, lock_g)) for i in range(HOTEL_GUESTS)]

    #start
    for i in range(CLEANING_STAFF):
        processes_c[i].start()
    
    for i in range(HOTEL_GUESTS):
        processes_g[i].start()

    #join
    for i in range(CLEANING_STAFF):
        processes_c[i].join()
    
    for i in range(HOTEL_GUESTS):
        processes_g[i].join()

    # Results
    print(f'Room was cleaned {sl[2]} times, there were {sl[1]} parties')


if __name__ == '__main__':
    main()

