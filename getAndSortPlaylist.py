import tone_analyzer as t
from PyLyrics import PyLyrics
import sys
import spotipy
import spotipy.util as util

def print_tone_dict(tone_dict):
	for category in tone_dict["document_tone"]["tone_categories"]:
		print "Scores in " + category["category_name"] + "."
		for tone in category["tones"]:
			print tone["tone_name"] + ":", tone["score"]
		print

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope)

sad_songs = []
joy_songs = []
if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
		track = item['track']
		songname = track['name']
		artist = track['artists'][0]['name']
		lyrics = None
		try:
			lyrics = PyLyrics.getLyrics(artist, songname)

			tone_dict = t.get_tone_for_text(lyrics)
			print_tone_dict(tone_dict)

			emotion_dict = tone_dict["document_tone"]["tone_categories"][0]["tones"]
			joy = [x for x in emotion_dict if x['tone_name'] == "Joy"][0]['score']
			sadness = [x for x in emotion_dict if x['tone_name'] == "Sadness"][0]['score']

			print joy
			print sadness

			song = {'name':songname, 'artist':artist}
			if joy > sadness:
				joy_songs.append(song)
			else:
				sad_songs.append(song)

		except ValueError as e:
			print "Error:", e


else:
    print "Can't get token for", username

print "Sad songs:"
for song in sad_songs:
	print song
print
print "Joy songs:"
for song in joy_songs:
	print song


