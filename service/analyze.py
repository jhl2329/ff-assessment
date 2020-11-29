class Analyzer():

	def __init__(self):
		self.puncutation = """!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~'"""
		self.suffixes = {'L':'', 'LZ':'', 'EVM':'', 'ZQ':'', 'ZL':'A', 'PZL':'AZ', 'EZL':'R'}
		suffix_keys = list(self.suffixes.keys())
		# sort based on length of suffix in descending order
		suffix_keys.sort(key=len, reverse=True)
		self.suffix_keys = suffix_keys

	'''
	Parse an incoming file byte stream for frequency, and returns a list of tuples of frequency count
	of each word.
	'''
	def parse_file(self, file, words_to_skip=set(), core_words=False):
		counts = {}
		root_words = []
		suffix_words = []
		for word in file.split():
			word = self.process_punctuation(word)
			# regardless of case, Dog == dog == DOG
			word = word.upper()
			if core_words:
				ending_suffix = self.ends_in_suffix(word)
				if ending_suffix is not None:
					suffix_words.append((word, ending_suffix))
				else:
					root_words.append(word)
			else:
				root_words.append(word)

		self.process_suffixes(suffix_words, root_words)
		word_counts = self.get_word_counts(root_words, words_to_skip)
		return self.get_top(word_counts)

	# Go through each word in suffix_words and see if they match any valid words, appending result to total_words
	def process_suffixes(self, suffix_words, total_words):
		already_seen_words = {}
		for suffix_tuple in suffix_words:
			word = suffix_tuple[0]
			if word in already_seen_words.keys():
				total_words.append(already_seen_words[word])
			else:
				ending_suffix = suffix_tuple[1]
				possible_word = self.get_resulting_word(word, ending_suffix)
				if possible_word in total_words:
					total_words.append(possible_word)
					already_seen_words[word] = possible_word
				else:
					total_words.append(word)
					already_seen_words[word] = word

	# For a given list of words, return freq count of each word
	def get_word_counts(self, words, words_to_skip):
		counts = {}
		for word in words:
			if self.is_all_letters(word) and word not in words_to_skip and word != '':
				if word not in counts:
					counts[word] = 1
				else:
					counts[word] = counts[word] + 1
		return counts

	# Filter out non-character words
	def is_all_letters(self, word):
		for char in word:
			num_val = ord(char)
			if not ((num_val >= 65 and num_val <= 90) or (num_val >= 97 and num_val <= 122)):
				return False
		return True

	# If puncutation at end, then get rid of it, otherwise return as is
	def process_punctuation(self, word):
		last_char = word[len(word)-1]
		if last_char in self.puncutation:
			return word[:len(word)-1]
		return word

	# If word ends in any of the suffixes, return the suffix the word ends with, otherwise None
	def ends_in_suffix(self, word):
		for suffix in self.suffix_keys:
			if suffix == word[len(word)-len(suffix):]:
				return suffix
		return None

	'''
		Replace a word's suffix with the matching rule to return a new possible word.
		Pre-req is that the ending is in the possibles suffixes b/c these method would only be called if 
		'word' has a suffix that matches rule.
	'''
	def get_resulting_word(self, word, ending):
		suffix = self.suffixes[ending]
		return word[:len(word) - len(ending)] + suffix

	# Return list of 25 top counts
	def get_top(self, frequency_count):
		# Sort by count of each item
		sorted_list = sorted(frequency_count.items(), key=lambda item: item[1], reverse=True)
		# Get first 25 results
		return sorted_list[:25]