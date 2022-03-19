import requests
import re
from bs4 import BeautifulSoup
import pprint

class Event:
    def __init__(self, title, date, time, location, image_link, identifier, artists, works) -> None:
        self.title = title
        self.date = date
        self.time = time
        self.location = location
        self.image_link = image_link
        self.identifier = identifier
        self.artists = artists
        self.works = works

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    @classmethod
    
    def fromHTML(cls, event_html):
        event_link = event_html.select("p.title a")[0].get('href')  #works
        event_title = event_html.find("a", class_ = "detail")  #works
        event_title = event_title.get_text() #works
        event_location = event_html.find("p", class_ ="location") #works
        if event_location is not None:
            event_location = event_location.get_text().strip(' \n\t')
        event_time = event_html.find("span", class_="time") #works
        if event_time is not None:
            event_time = event_time.get_text()
        event_date = event_html['data-date'] #works
        event_image = event_html.find("div", class_ = "image")['style'] #works
        event_image_url = event_image.split('(')[1].split(')')[0] #works
        event_identifier = event_html['id'].split('_')[-1]
        

        event_url = "https://www.lucernefestival.ch/" + event_link
        event_page = requests.get(event_url)
        event_soup = BeautifulSoup(event_page.content, "html.parser")
        event_artists = event_soup.find_all("div", class_ = "artist")
        event_artists_formatted = []
        for event_artist in event_artists:
            event_artist_formatted =  event_artist.strong.get_text().strip(' \n\t')
            if ":" in event_artist_formatted:
                event_artist_formatted = event_artist_formatted.split(':')[0].strip(' \n\t')
            event_artists_formatted.append(event_artist_formatted) 
    
        event_works_formatted = []
        event_works =  event_soup.find_all("div", class_ = "musical-piece")
        for event_work in event_works:
            event_work_formatted = event_work.get_text().strip(' \n\t')
            event_works_formatted.append(event_work_formatted)
    
        return cls(event_title, event_date, event_time, event_location, event_image_url, event_identifier, event_artists_formatted, event_works_formatted)
     
    