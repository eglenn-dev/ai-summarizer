import requests
from bs4 import BeautifulSoup
import json

class website_parser():

    def __init__(self, url):
        self._url = url
        def get_website(url):
            try:
                return requests.get(url)
            except: 
                raise Exception('Error while requesting the data')
        self._response = get_website(url)
        self._response_code = self._response.status_code
        self._soup = BeautifulSoup(self._response.text, 'html.parser')
        self._text_content = self._soup.get_text()
        self._summary = ''


    def get_tags(self, target='p'):
        return self._soup.find_all(target)
    
    def get_text(self):
        return self._text_content

    def set_summary(self, text_summary):
        self._summary = text_summary

    def get_summary(self):
        return self._summary