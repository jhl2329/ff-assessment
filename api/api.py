from service import processor
from datetime import datetime
import uuid
import flask
from flask import request, render_template
import pandas as pd

app = flask.Flask(__name__, template_folder='template')
app.config["DEBUG"] = True

# Health check
@app.route('/', methods=['GET'])
def home():
	return 'Hello'

# Basic upload 
@app.route('/upload')
def upload_file():
	return render_template('upload.html')

# Get file from upload and do analysis on it. 
@app.route('/api/v1/analyze', methods=['POST'])
def analyze_file():
	# generate uuid to act as request marker
	request_id = str(uuid.uuid4())
	skip_words = 'stop' in request.form
	core_words = 'stem' in request.form
	# FileStorage object
	file = request.files['file']
	# Decode incoming file with utf-8
	decoded_file = file.read().decode('utf-8', 'ignore')
	# Throw to service code to do analysis, returns df of results
	service_processor.process(request_id, decoded_file, skip_words, core_words, file.filename, True)
	json = service_processor.get(request_id)
	if json is not None:
		df = pd.read_json(json['data'])
		return render('results.html', df, request_id, json['skip_words'], json['core_words'], json['file_name'])

@app.route('/api/v1', methods=['GET'])
def get():
	request_id = request.args.get('id', type = str)
	json = service_processor.get(request_id)
	if json is not None:
		df = pd.read_json(json['data'])
		return render('results.html', df, request_id, json['skip_words'], json['core_words'], json['file_name'])
	return 'Not Found'

@app.route('/api/v1/all')
def get_all():
	keys = service_processor.get_all()
	return render_template('get_all.html', keys=keys)

def render(template_name, tables, request_id, skip_words, core_words, file_name):
	return render_template(template_name,
		tables=[tables.to_html()] if not tables.empty else [],
		timestamp=datetime.now(),
		request_id=request_id,
		file_name=file_name,
		skip_words=skip_words,
		core_words=core_words
	)

service_processor = processor.Processor()
app.run(host='0.0.0.0')
