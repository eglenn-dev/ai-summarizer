import json
import os
from website_parser import website_parser as wp

import google.generativeai as genai

API_KEY = 'AIzaSyDwY5zfvC_zHeJ0eHNN9H7pIr-lo-BmSj4'

genai.configure(api_key=API_KEY)

website = wp('https://news-gh.churchofjesuschrist.org/article/apostles-join-the-africa-west-area-presidency-in-visit-to-lagos-and-abuja--nigeria')

model = genai.GenerativeModel(model_name='gemini-pro')
prompt = 'Summarize the following article into three key bullet points, ensuring no bias in the summarization: ' + website.get_text()
result = model.generate_content(prompt, stream=False)
website.set_summary(result.text)
print(website.get_summary())