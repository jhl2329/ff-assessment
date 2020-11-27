from service import analyze, processor
from datetime import datetime
import flask
from flask import request, render_template

app = flask.Flask(__name__, template_folder='template')
app.config["DEBUG"] = True

# Health check
@app.route('/', methods=['GET'])
def home():
	return render_template('base.html')

# Basic upload 
@app.route('/upload')
def upload_file():
	return render_template('upload.html')

# Get file from upload and do analysis on it. 
@app.route('/api/v1/analyze', methods=['POST'])
def analyze_file():
	skip_words = request.args.get('skip', default=0, type=int)
	core = request.args.get('core', default=0, type=int)

	# FileStorage object
	file = request.files['file']
	# Decode incoming file with utf-8
	decoded_file = file.read().decode('utf-8', 'ignore')
	# Throw to service code to do analysis, returns df of results
	service_response = processor.process(decoded_file)
	return render_template('results.html', 
		tables=[service_response.to_html()] if not service_response.empty else [],
		timestamp=datetime.now(),
		filename=file.filename
	)


app.run()
