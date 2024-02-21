import requests
from bs4 import BeautifulSoup
import json

class Site():

    def __init__(self, url):
        self._url = url
        self._response = get_website()
        self._response_code = self._response.status_code
        self._soup = BeautifulSoup(response.text, 'html.parser')
        self._text_content = _soup.get_text()
        self._summary = ''

    def get_website(self):
        # Get website data
        try:
            return requests.get(self._url)
        except: 
            raise Exception('Error while requesting the data')

    def get_tags(target='p'):
        return _soup.find_all(target)
    
    def get_text():
        return self._text_content

    def set_summary(text_summary):
        self._summary = text_summary

    def get_summary():
        return self._summary