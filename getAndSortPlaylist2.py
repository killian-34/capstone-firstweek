import tone_analyzer as t
from PyLyrics import PyLyrics
import sys
import spotipy
import spotipy.util as util


scope = 'playlist-modify-private'

username = ""
playlist_id = ""

if len(sys.argv) > 1:
    uri = sys.argv[1]
    try:
    	username = uri.split(':')[2]
    	playlist_id = uri.split(':')[4]
    except:
    	username = uri.split('/')[4]
    	playlist_id = uri.split('/')[6]

else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()
print username
print playlist_id
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
else:
    print "Can't get token for", username


sad_songs = []
joy_songs = []
for item in tracks:
	track = item['track']
	print track['name'] + ' - ' + track['artists'][0]['name']
	print
	print

	track_id = track["id"]
	print
	print
	track = item['track']
	songname = track['name']
	artist = track['artists'][0]['name']
	song = {'name':songname, 'artist':artist, 'id':track_id}
	lyrics = None
	try:
		lyrics = PyLyrics.getLyrics(artist, songname)

		tone_dict = t.get_tone_for_text(lyrics)

		emotion_dict = tone_dict["document_tone"]["tone_categories"][0]["tones"]
		joy = [x for x in emotion_dict if x['tone_name'] == "Joy"][0]['score']
		sadness = [x for x in emotion_dict if x['tone_name'] == "Sadness"][0]['score']

		print joy
		print sadness

		if joy > sadness:
			joy_songs.append(song)
		else:
			sad_songs.append(song)

	except ValueError as e:
		print "Error:", e


print "Sad songs:"
for song in sad_songs:
	print song['name'] + " - " + song['artist'] 
print
print "Joy songs:"
for song in joy_songs:
	print song['name'] + " - " + song['artist'] 



happyTracks = [x['id'] for x in joy_songs]
sadTracks = [x['id'] for x in sad_songs]


pInfo = sp.user_playlist_create(username, 'happySongs', public = False)
pID = pInfo['id']
sp.user_playlist_add_tracks(username, pID, happyTracks)

pInfo = sp.user_playlist_create(username, 'sadSongs', public = False)
pID = pInfo['id']
sp.user_playlist_add_tracks(username, pID, sadTracks)
