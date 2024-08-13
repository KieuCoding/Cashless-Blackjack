"""
name: Peter Kieu, Email: pckieu@cougarnet.uh.edu, PSID: 1916075
"""
import requests, json
from bs4 import BeautifulSoup
from flask import Flask, Response

URL = "https://www.msn.com/en-us/weather/forecast/in-Houston,TX?loc=eyJsIjoiSG91c3RvbiIsInIiOiJUWCIsInIyIjoiSGFycmlzIENvLiIsImMiOiJVbml0ZWQgU3RhdGVzIiwiaSI6IlVTIiwiZyI6ImVuLXVzIiwieCI6Ii05NS42MzA5OTY3MDQxMDE1NiIsInkiOiIyOS44NjgwMDAwMzA1MTc1NzgifQ%3D%3D&weadegreetype=F"

"""
Webscrapper class obtains the weather sites URL, and performs functions to retrieve certain
weather data live time.
"""
class Webscrapper:
    # this function/ class method converts the website data into html text
    @classmethod
    def get_soup(cls, URL):
        data = requests.get(URL)
        soup = BeautifulSoup(data.text, "html.parser")
        return soup
    
    # this function obtains the temperature data from the website via respective headers
    @classmethod
    def get_temp(cls, URL):
        data = {}
        soup = Webscrapper.get_soup(URL)
        element = soup.find_all('a', {"class": "summaryTemperatureCompact-E1_1 summaryTemperatureHover-E1_1"})
        data["current"] = element[0].contents[0]
        element = soup.find_all('a', {"class":"summaryFeelLikeContainerCompact-E1_1 detailItemGroupHover-E1_1"})
        """
        print(element[0].contents)
        print(element[0].contents[1])
        print(len(element[0].contents[1]))
        word = str(element[0].contents[1])
        word_len = len(word)
        extraction = word[14:16]
        type(word)
        print(word)
        print(word_len)
        print(extraction)
        data["feel like"] = extraction
        """
        data["feels like"] = element[0].text[11:13]
        return data
    
    # this function obtains the air quality data from the website via respective headers
    @classmethod
    def get_airq(cls, URL):
        data = {}
        soup = Webscrapper.get_soup(URL)
        element = soup.find_all('a', {"class": "aqiDetailItemGroupCompact-E1_1 aqiDetailItemGroupHoverCompact-E1_1"})
        data["air quailty"] = element[0].text[74:76]
        return data
    
    # this function obtains the wind data from the website via respective headers
    @classmethod
    def get_wind(cls, URL):
        data = {}
        soup = Webscrapper.get_soup(URL)
        element = soup.find_all('a', {"class": "detailItemGroup-E1_1 detailItemGroupHover-E1_1"})
        data["wind"] = element[0].text[86:91] 
        return data
    
    # this function obtains the humidity data from the website via respective headers
    @classmethod
    def get_humidity(cls, URL):
        data = {}
        soup = Webscrapper.get_soup(URL)
        element = soup.find_all('a', {"class": "detailItemGroup-E1_1 detailItemGroupHover-E1_1"})
        data["humidity"] = element[1].text[136:138] # element[1] because humidity data in second element
        return data

"""
Proxy class will create URL(Proxy) and create headers for each of the
local host URL, that will have the weather data within each of their
respective URL Proxy.
"""  
class Proxy:
    app = None
    def __init__(self, name):
        self.app = Flask(name)
        self.app.add_url_rule("/temp", "temp", self.dispatch_temp_request)
        self.app.add_url_rule("/airq", "airq", self.dispatch_airq_request)
        self.app.add_url_rule("/wind", "wind", self.dispatch_wind_request)
        self.app.add_url_rule("/humidity", "humidity", self.dispatch_humidity_request)
        
    # Local URL Proxy for temperature data 
    def dispatch_temp_request(self):
        print("handle the /temp request")
        data = Webscrapper.get_temp(URL)
        return Response(json.dumps(data), status=200, headers={})
    
    # Local URL Proxy for air quality data 
    def dispatch_airq_request(self):
        print("handle the /airq request")
        data = Webscrapper.get_airq(URL)
        return Response(json.dumps(data), status=200, headers={})
    
    # Local URL Proxy for wind data 
    def dispatch_wind_request(self):
        print("handle the /wind request")
        data = Webscrapper.get_wind(URL)
        return Response(json.dumps(data), status=200, headers={})
    
    # Local URL Proxy for humidity data 
    def dispatch_humidity_request(self):
        print("handle the /humidity request")
        data = Webscrapper.get_humidity(URL)
        return Response(json.dumps(data), status=200, headers={})
    
    # function to run the application without the "/'weather data'"
    # add /temp or /airq or /wind or /humidity to end of http://localhost:5000
    def run(self):
        self.app.run()
        
p = Proxy(__name__) # enter a name
p.run()