import json
import os
import site

import google.generativeai as genai
from flask import Flask, jsonify, request, send_file, send_from_directory
from website_parser import website_parser as wp

API_KEY = 'AIzaSyDwY5zfvC_zHeJ0eHNN9H7pIr-lo-BmSj4'

genai.configure(api_key=API_KEY)

app = Flask(__name__)


@app.route("/")
def index():
    return send_file('web/index.html')


@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        if API_KEY == 'TODO':
            return jsonify({ "error": '''
                To get started, get an API key at
                https://g.co/ai/idxGetGeminiKey and enter it in
                main.py
                '''.replace('\n', '') })
        try:
            req_body = request.get_json()
            model = genai.GenerativeModel(model_name=req_body.get("model"))
            website = wp(req_body.get("url"))
            response = model.generate_content(f'Summarize the following article into three key bullet points: {website.get_text()}', stream=True)
            def stream():
                for chunk in response:
                     yield 'data: %s\n\n' % json.dumps({ "text": chunk.text })

            return stream(), {'Content-Type': 'text/event-stream'}

            # website = wp(request.form['urlInput'])
            # model = genai.GenerativeModel(model_name='gemini-pro')
            # prompt = 'Summarize the following article into three to five key bullet points: ' + website.get_text()
            # result = model.generate_content(prompt, stream=True)
            # def stream():
            #     for chunk in result:
            #         yield 'data: %s\n\n' % json.dumps({ "text": chunk.text })
            # return stream(), {'Content-Type': 'text/event-stream'}           

        except Exception as e:
            return jsonify({ "error": str(e) })


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)


if __name__ == "__main__":
    app.run(port=5510, debug=True)
