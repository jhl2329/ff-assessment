from service import analyze
import pandas as pd
# take file that's already decoded and in bytes, and do analysis, returning pandas df of results
def process(file):
	analysis = analyze.parse_file(file) # list of tuples
	if (len(analysis) == 0): # analysis turned up empty for words
		return pd.DataFrame()
	df = pd.DataFrame(analysis)
	df.columns = ['Word', 'Count']
	return df