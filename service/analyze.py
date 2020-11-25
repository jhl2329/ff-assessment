# Parse an incoming file for frequency
def parse_file(file):
	for line in file.read():
		print(chr(line))
		print('stop')

# Filter out non-character words
def filter_nonchar():
	return None