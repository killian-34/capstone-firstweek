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


print "Sad songs:"
for song in sad_songs:
	print song
print
print "Joy songs:"
for song in joy_songs:
	print song