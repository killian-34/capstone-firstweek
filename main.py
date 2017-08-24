import argparse
import tone_analyzer as t
from PyLyrics import PyLyrics



def print_tone_dict(tone_dict):
	for category in tone_dict["document_tone"]["tone_categories"]:
		print "Scores in " + category["category_name"] + "."
		for tone in category["tones"]:
			print tone["tone_name"] + ":", tone["score"]
		print

parser = argparse.ArgumentParser(description = "Get tone from text using IBM Watson")
parser.add_argument("-f","--songfile", type = str, help = "")
parser.add_argument("-s", "--songname", type = str, help = "")
parser.add_argument("-a", "--artist", type = str, help = "")

args = parser.parse_args()

text_we_want = ""
if (args.songname):
	lyrics = PyLyrics.getLyrics(args.artist, args.songname)
	print lyrics
	text_we_want = lyrics

else:
	textfile = open(args.songfile,'r')
	tone_text = textfile.read()
	textfile.close()
	text_we_want = tone_text

tone_dict = t.get_tone_for_text(text_we_want)

print_tone_dict(tone_dict)

emotion_dict = tone_dict["document_tone"]["tone_categories"][0]["tones"]
joy = [x for x in emotion_dict if x['tone_name'] == "Joy"][0]['score']
sadness = [x for x in emotion_dict if x['tone_name'] == "Sadness"][0]['score']

print joy
print sadness




