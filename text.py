import json
import os
import site

import google.generativeai as genai
from flask import Flask, jsonify, request, send_file, send_from_directory

API_KEY = 'AIzaSyDwY5zfvC_zHeJ0eHNN9H7pIr-lo-BmSj4'

website = Site('https://www.cnn.com/2024/02/20/politics/joe-biden-donald-trump-wild-comments/index.html')

model = genai.GenerativeModel(model_name=req_body.get("model"))
prompt = 'Summarize the following article into three bullet points: ' + website.get_text()
summary = model.generate_content(prompt, stream=False)
print(summary)