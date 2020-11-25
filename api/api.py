from service import analyze
import flask
from flask import request, jsonify, render_template

app = flask.Flask(__name__, template_folder='template')
app.config["DEBUG"] = True

# Health check
@app.route('/', methods=['GET'])
def home():
	return 'Hello!'

# Basic upload 
@app.route('/upload')
def upload_file():
	return render_template('upload.html')

# Get file from upload and do analysis on it. 
@app.route('/api/v1/analyze', methods=['POST'])
def analyze_file():
	skip_words = request.args.get('skip', default=0, type=int)
	core = request.args.get('core', default=0, type=int)

	file = request.files['file']
	analyze.parse_file(file)
	return 'Processing'

app.run()
