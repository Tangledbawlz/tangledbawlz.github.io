"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau
Purpose: Retrieve Star Wars details from a server
Instructions:
- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.
The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.
{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
from matplotlib.pyplot import title
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
    
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)


# TODO Add any functions you need here
    def grabFilms(self, url):
        films = Request_thread(url)
        films.start()
        films.join()
        if films.response != {}:
            self.remaining = films.response['remaining']
            return films.response[title][0]['opening_crawl']
        else:
            return ' '

    def grabPeople(self, url):
        people = Request_thread(url)
        people.start()
        people.join()

    def grabPlanets(self, url):
        planets = Request_thread(url)
        planets.start()
        planets.join()

    def grabSpecies(self, url):
        species = Request_thread(url)
        species.start()
        species.join()

    def grabVehicles(self, url):
        vehicles = Request_thread(url)
        vehicles.start()
        vehicles.join()

    def grabStarships(self, url):
        starships = Request_thread(url)
        starships.start()
        starships.join()



def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls
    response = requests.get(TOP_API_URL)

    # TODO Retrieve Details on film 6
    films = Request_thread.grabFilms(rf"http://127.0.0.1:8790/films/")
    people = Request_thread.grabPeople(rf"http://127.0.0.1:8790/people/")
    planets = Request_thread.grabPlanets(rf"http://127.0.0.1:8790/planets/")
    species = Request_thread.grabSpecies(rf"http://127.0.0.1:8790/species/")
    vehicles = Request_thread.grabVehicles(rf"http://127.0.0.1:8790/vehicles/")
    starships = Request_thread.grabStarships(rf"http://127.0.0.1:8790/starships/")
    
    # TODO Display results
    print(films, people, planets, species, vehicles, starships)


    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()