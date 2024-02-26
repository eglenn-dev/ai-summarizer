import json
import os
import google.generativeai as genai
from flask import Flask, jsonify, request, send_file, send_from_directory, redirect
from website_parser import website_parser as wp
from PyPDF2 import PdfReader  as pfr
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import math

# Importing the API key into the environment
load_dotenv()
API_KEY = os.environ.get('API_KEY')

# Checking if the API key is present
if API_KEY is None:
    # If not, print an error message and exit
    print('API_KEY not found in environment variables. Please set it and try again.')
    exit()

# Configuring the API key and the gemini api object
genai.configure(api_key=API_KEY)
file_name = ''

# Creating the Flask app and setting the upload folder and allowed file extensions
app = Flask(__name__, static_url_path='/web', static_folder='web')
current_dir = os.path.abspath(os.path.dirname(__file__))
upload_folder = os.path.join(current_dir, 'static/uploads')
app.config['UPLOAD_FOLDER'] = upload_folder
ALLOWED_EXTENSIONS = {'pdf'}
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Default root
@app.route('/')
def index():
    return send_file('web/pages/index.html')

@app.route('/site')
def site():
    return send_file('web/pages/site.html')

@app.route('/doc')
def doc():
    return send_file('web/pages/doc.html')

@app.route('/api/site', methods=['GET', 'POST'])
def generate_api():
    if request.method == 'POST':
        try:
            req_body = request.get_json()
            model = genai.GenerativeModel(model_name=req_body.get('model'))
            website = wp(req_body.get('url'))
            response = model.generate_content(f'Summarize the following article into four key bullet points: {website.get_text()}', stream=True)
            def stream():
                for chunk in response:
                     yield 'data: %s\n\n' % json.dumps({ 'text': chunk.text, 'faviconURL': website.get_favicon()})

            return stream(), {'Content-Type': 'text/event-stream'}     

        except Exception as e:
            return jsonify({ 'error': str(e) })
    elif request.method == 'GET':
        return redirect('/')

@app.route('/api/doc', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']

        if file.filename == '':
            return 'No selected file', 400
        
        if file and allowed_file(file.filename):
            # Preparing the file
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            global file_name
            file_name = filename

            try:
                model = genai.GenerativeModel(model_name='gemini-pro')
                with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), 'rb') as f:
                    pdf = pfr(f)
                    text = ''
                    for i in range(len(pdf.pages)):
                        text += pdf.pages[i].extract_text()
                    text.replace('\n', ' ')
                    bullet_points = calculate_bullet_points(count_pages(pdf), 300)
                    response = model.generate_content(f'Summarize the following document into {bullet_points} key bullet that are categorized into sections, also preforms a sentiment analysis at the bottom, and generate three questions to gauge the readers understanding of the document: {text}', stream=True)
                    def stream():
                        for chunk in response:
                            yield 'data: %s\n\n' % json.dumps({ 'text': chunk.text})

                    return stream(), {'Content-Type': 'text/event-stream'}    

            except Exception as e:
                return jsonify({ 'error': str(e) })
    elif request.method == 'GET':
        return redirect('/')


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

def calculate_bullet_points(document_length, max_summary_length, k=0.001, m=2500):
    return math.ceil((max_summary_length / (1 + math.exp(-k * (document_length - m)))) / 20)

def count_pages(document):
    word_count = 0
    num_pages = len(document.pages)
    for page_num in range(num_pages):
            page = document.pages[page_num]
            text = page.extract_text()
            words = text.split()
            word_count += len(words)
    return word_count

if __name__ == '__main__':
    app.run(port=5510, debug=True) # For debugging
    # app.run(port=5000, host='0.0.0.0') # For deployment
