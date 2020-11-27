PUNCTUATION = """!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~'"""

'''
Parse an incoming file byte stream for frequency, and returns a list of tuples of frequency count
of each word.
'''
def parse_file(file):
	counts = {}
	for word in file.split():
		word = process_punctuation(word)
		if is_all_letters(word):
			if word not in counts:
				counts[word] = 1
			else:
				counts[word] = counts[word] + 1
	return get_top(counts)

# Filter out non-character words
def is_all_letters(word):
	for char in word:
		num_val = ord(char)
		if not ((num_val >= 65 and num_val <= 90) or (num_val >= 97 and num_val <= 122)):
			return False
	return True

# If puncutation at end, then get rid of it, otherwise return as is
def process_punctuation(word):
	last_char = word[len(word)-1]
	if last_char in PUNCTUATION:
		return word[:len(word)-1]
	return word

# Return list of 25 top counts
def get_top(frequency_count):
	# Sort by count of each item
	sorted_list = sorted(frequency_count.items(), key=lambda item: item[1], reverse=True)
	# Get first 25 results
	# print(sorted_list[:25])
	return sorted_list[:25]

def health_check():
	return 'Hello world'