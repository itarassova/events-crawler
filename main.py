import requests
import re
from bs4 import BeautifulSoup
from database import EventPSQL
from event import Event
import pprint
import os
import logging

if __name__ == '__main__':
    host = os.getenv('HOST', default = 'localhost')
    database = os.getenv('DATABASE', default = 'postgres')
    user = os.getenv('USER', default = 'postgres')
    password = os.getenv('PASSWORD', default = 'mysecretpassword')

    event_psql = EventPSQL(host, database, user, password)
    

    URL = "https://www.lucernefestival.ch/en/program/summer-festival-22"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    events_html = soup.find_all(id=re.compile("event_id_"))
    for event_html in events_html:
        try:
            event = Event.fromHTML(event_html) 
            event_insert = event_psql.insert_event_details(event)
            logging.info("Processed: %s", event)
        except Exception as e:
            logging.error(e, exc_info=True)
    
    

   



