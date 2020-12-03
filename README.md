# Intro

Project, when given a file, counts the instances of each word and returns the top 25 results. 

## Installation

Utilizes docker to run both the python app and a redis cluster. In addition, requires port 5000 to be exposed on the docker host, since that's what the flask app in the python container binds to. 

With docker-daemon running in the background

```bash
docker-compose up
```

App needs to be run through docker-compose in order to see previous analysis results. 

In order to just view only a single analysis itself, you can kick off the flask app by utilizing the entry point for the python script, assuming Python 3
```bash
pip install -r requirements.txt

python main.py
```

Then once you get the app to start running (default port 5000), navigate to `localhost:5000/upload` and upload a file from your local file system. 

## Technologies
Flask to render a basic interface and API endpoints

Docker to containerize application

Redis for basic, naive persistence

Pandas to render results in easy to read interface. 

## Usage

Navigate to `localhost:5000` to verify app is running

Then for a given .txt file,

1. Navigate to `localhost:5000/upload`
2. Select file to upload, and select checks like skipping words from pre-determined set or only utilizing "core" words
3. To see previous results, navigate to `localhost:5000/api/v1/all` and click on any of the available UUIDs to see a previous result. 

## Useful Commands
If both the python container and the redis container is up, you can view the contents of what's going on by doing as such: 

1. `docker ps`
2. Find the process id of the docker container
3. `docker exec -it ${process_id} /bin/bash`
4. Then simply type in `redis-cli` to have an interactive version of the redis instance.

## Assumptions and Thought Process for Assessment
In addition to the requirements set forth in the exercise document, I made some additional assumptions regarding the logic of some of the analysis. They are as follows:

1. A valid word is considered as such if and only if it contains characters [A-Z] and [a-z]. As such, if there is such a word like 'ABC?D', it would be considered an invalid word since the '?' interrupts the main word. Other such examples of invalid characters are numbers or accented characters.  
2. However, if a word ends in some punctuation such as "!", "?", "," and etc. once the punctuation is removed, it would be considered a valid word. For example the valid word of "ABCD?" would then be considered to be "ABCD". However, if the word in question is something like "ABCD??", the 1st question mark at index 4 would result in that word being marked as invalid and as a result, would not be counted in the frequency count. 
3. For purposes of this exercise, casing doesn't matter, such that if we have a file with "Dog", "DOG", and "dog", the resulting analysis is that there would be 3 instances of the word, "dog". 
4. In the logic of extracting the stem word from the total word itself, I made the assumption that the suffix with the longest length takes precedence of another possible suffix with the shorter length. For example, if we have suffixes of "PZL" and "L", the replacement rule to apply would be PZL, instead of L since it would have a greater "weight". 
5. For the bonus algorithm where one determines whether a resulting word is a valid extracted root word, this logic was executed: assume that for a given set of words, the calculation would end up with 2 sets of words, one that ends in desired suffixes and another that does not end in any suffixes. Then, consider all words in the set that doesn't contain suffixes to be a set of "valid" words for the whole algorithm. After, iterate through the suffix words and apply the relevant rules. If the resulting word is in the valid set of words, then it can be considered a proper transformation for that root. Otherwise, then assume it is not a valid transformation, and add it as a new valid word to the initial valid set. The end result is that you either increment a valid word in the initial generated set of valid words, or end up adding newly minted valid words to the generated set for frequency analysis. 