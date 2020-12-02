# Intro

Project, when given a file, counts the instances of each word and returns the top 25 results. 

## Installation

Utilizes docker to run both the python app and a redis cluster. In addition, requires port 5000 to be exposed on the docker host, since that's what the flask app in the python container binds to. 

With docker-daemon running in the background

```bash
docker-compose up
```

## Usage

Navigate to `localhost:5000` to verify app is running

Then for a given .txt file,

1. Navigate to `localhost:5000/upload`
2. Select file to upload, and select checks like skipping words from pre-determined set or only utilizing "core" words
3. To see previous results, navigate to `localhost:5000/api/v1/all` and click on any of the available UUIDs to see a previous result. 