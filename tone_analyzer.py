from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonException
import json
import argparse



def get_tone_for_text(tone_text):

	with open('../creds.json') as data_file:
	    data = json.load(data_file)


	username = data['username']
	password =  data['password']
	version = data['version']

	tone_analyzer = ToneAnalyzerV3(
	  version=version,
	  username=username,
	  password=password
	)

	tone_dict = None
	try:
		tone_dict = tone_analyzer.tone(tone_text, content_type='text/plain', sentences=False)
	except WatsonException as e:
		print "Something went wrong with your request. Here is what they said:"
		print e

	return tone_dict



parser = argparse.ArgumentParser(description = "Get tone from text using IBM Watson")
parser.add_argument("textfile", type = str, help = "")
args = parser.parse_args()

textfile = open(args.textfile,'r')
tone_text = textfile.read()
textfile.close()
tone_dict = get_tone_for_text(tone_text)

for category in tone_dict["document_tone"]["tone_categories"]:
	print "Scores in " + category["category_name"] + "."
	for tone in category["tones"]:
		print tone["tone_name"] + ":", tone["score"]
	print





#print json.dumps(tone_dict, indent=2)

