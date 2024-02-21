import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
    
    def get_favicon(self):
        try:
            # Find the favicon link tag
            favicon_link = self._soup.find('link', rel='icon') or self._soup.find('link', rel='shortcut icon')
            
            # Extract favicon URL
            if favicon_link:
                favicon_url = favicon_link.get('href')
                # If the URL is relative, convert it to absolute URL
                favicon_url = urljoin(self._url, favicon_url)
                return favicon_url
            else:
                return None
        except Exception as e:
            print("Error:", e)
            return None