from service import processor
from datetime import datetime
import flask
from flask import request, render_template

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
	skip_words = 'stop' in request.form
	core_words = 'stem' in request.form
	# FileStorage object
	file = request.files['file']
	# Decode incoming file with utf-8
	decoded_file = file.read().decode('utf-8', 'ignore')
	# Throw to service code to do analysis, returns df of results
	service_response = service_processor.process(decoded_file, skip_words, core_words)
	return render_template('results.html', 
		tables=[service_response.to_html()] if not service_response.empty else [],
		timestamp=datetime.now(),
		filename=file.filename,
		skip_words=skip_words,
		core_words=core_words
	)

service_processor = processor.Processor()
app.run()
