import json
import os
import google.generativeai as genai
from flask import Flask, jsonify, request, send_file, send_from_directory
from website_parser import website_parser as wp
from PyPDF2 import PdfFileReader as pfr
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("API_KEY")

if API_KEY is None:
    print("API_KEY not found in environment variables. Please set it and try again.")
    exit()
genai.configure(api_key=API_KEY)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return send_file('web/site.html')

@app.route('/site')
def site():
    return send_file('web/site.html')

@app.route('/doc')
def doc():
    return send_file('web/doc.html')

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
                     yield 'data: %s\n\n' % json.dumps({ "text": chunk.text, "faviconURL": website.get_favicon()})

            return stream(), {'Content-Type': 'text/event-stream'}     

        except Exception as e:
            return jsonify({ "error": str(e) })

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'
        


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)


if __name__ == "__main__":
    app.run(port=5510, debug=True)
