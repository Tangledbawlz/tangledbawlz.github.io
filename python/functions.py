"""
Course: CSE 251, week 14
File: common.py
Author: Norman Tangedal
Instructions:
Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU
Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04
Requesting a family from the server:
family = Request_thread(f'{TOP_API_URL}/family/{id}')
Requesting an individual from the server:
person = Request_thread(f'{TOP_API_URL}/person/{id}')
You will lose 10% if you don't detail your part 1 
and part 2 code below
Describe how to speed up part 1

I tried to speed up the tree with threads and ran into a few race condition problems, and although I was able to speed it up exponentially with threads,
I began to lose data more and more and have left it at no threads for now. To speed this up, I was assisted by creating another method for requesting 
a person, in order to thread the threads. We hoped that this would speed up the processes, and limit the race conditions. After a few attempts, we
were able to get the thread time down to 3 seconds and grabbing half the information, but it became unstable and we attacked it with a different idea.

Describe how to speed up part 2

In order to speed up number 2, I would use an idea similar to what we did for the maze, and have threads created at every parent. That way, for each
parent, there would be 2^n threads, and it would speed this up much quicker.

10% Bonus to speed up part 3
<Add your comments here>

http://127.0.0.1:8123/person/5018280996


http://127.0.0.1:8123/person/start_id : "OK"

"""
from concurrent.futures import thread
from common import *
import threading

plock = threading.Lock()


def requestPerson(id, my_fam_persons):
    global plock
    req_person = Request_thread(f'{TOP_API_URL}/person/{id}')
    req_person.start()
    req_person.join()
    plock.acquire()
    p = Person(req_person.response)
    plock.release()

    plock.acquire()
    my_fam_persons.append(p)
    plock.release()
    
def member_in_family(family, tree):
    global plock
    my_fam_ids = []
    my_fam_persons = []
    threads = []
    #grab families ids and place them into my_fam_ids
    my_fam_ids.append(family.husband)
    my_fam_ids.append(family.wife)

    for child in family.children: 
        my_fam_ids.append(child)

    #iterate through the fam ids to get people info
    for item in my_fam_ids:
        #for each person's id create a Person and append it to my_fam_persons
        if not tree.does_person_exist(item):
            # Attempt at making a threaded call
            # thread = threading.Thread(target=requestPerson, args=(item, my_fam_persons))
            # threads.append(thread)
            # thread.start()
            requestPerson(item, my_fam_persons)
        else:
            # Append to persons list
            my_fam_persons.append(tree.get_person(item))
    #join the threads to finish getting responses
    # for i in threads:
    #     i.join()

    #return persons list
    return my_fam_persons

    
count = 0
# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    # TODO - implement Depth first retrieval
    # Tree might have the starting family id already set
    global count
    threads = []
    count += 1
    print(family_id)
    if tree.does_family_exist(family_id):
        return

    
    # Family_id at first is the starting family
    req_fam = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    req_fam.start()
    req_fam.join()
    # Must have family created properly, with the family id, and the request information
    family = Family(family_id, req_fam.response)
    family_members = member_in_family(family, tree) #Person list
    
    
    #add family to tree
    tree.add_family(family)

    #add the people in the family to the tree
    for item in family_members:
        tree.add_person(item)

    # #recursive 
    # recurse upwards for parents
    for parent in family_members[:2]: # Skip the children
        if parent.parents != None and tree.does_person_exist(parent.parents): # Check to see if parent parent exists and the parent parent is not in tree
            # thread = threading.Thread(target=depth_fs_pedigree, args=(parent.parents, tree))# for each child, add their families as well
            # threads.append(thread)
            # thread.start()
            depth_fs_pedigree(parent.parents, tree)  # Add each parent

    # recurse downwards for children
    for children in family_members[2:]: #skip the parents
        if children.family != None and not tree.does_family_exist(children.family): # if the child has a family, and the family exists, we recurse into that family
            # thread = threading.Thread(target=depth_fs_pedigree, args=(children.family, tree))# for each child, add their families as well
            # threads.append(thread)
            # thread.start()
            depth_fs_pedigree(children.family, tree) 
        
   

    for t in threads:
        t.join()


    

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(start_id, tree):
    # TODO - implement breadth first retrieval

    # print('WARNING: BFS function not written')

    pass


# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5

    threads = []
    print(family_id)
    if tree.does_family_exist(family_id):
        return
    
    # Family_id at first is the starting family
    req_fam = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    req_fam.start()
    req_fam.join()

    # Must have family created properly, with the family id, and the request information
    family = Family(family_id, req_fam.response)
    family_members = member_in_family(family, tree) #Person list
    
    #add family to tree
    tree.add_family(family)

    #add the people in the family to the tree
    for item in family_members:
        plock.acquire()
        tree.add_person(item)
        plock.release()

    # #recursive 
    # recurse upwards for parents
    for parent in family_members[:2]: # Skip the children
        if parent.parents != None and tree.does_person_exist(parent.parents): # Check to see if parent parent exists and the parent parent is not in tree
            with plock:
                thread = threading.Thread(target=breadth_fs_pedigree_limit5, args=(parent.parents, tree))# for each child, add their families as well
                threads.append(thread)
                thread.start()

    # recurse downwards for children
    for children in family_members[2:]: #skip the parents
        if children.family != None and tree.does_family_exist(children.family): # if the child has a family, and the family exists, we recurse into that family
            with plock:
                thread = threading.Thread(target=breadth_fs_pedigree_limit5, args=(children.family, tree))# for each child, add their families as well
                threads.append(thread)
                thread.start()

    for t in threads:
            t.join()
