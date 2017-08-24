import sys
import spotipy
import spotipy.util as util

scope = 'playlist-modify-private'

if len(sys.argv) > 1:
    uri = sys.argv[1]
    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
<<<<<<< HEAD
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
=======
    results = sp.current_user_saved_tracks()

    for item in results['items']:
        track = item['track']
        print track['name'] + ' - ' + track['artists'][0]['name']
>>>>>>> 203337b507ede6320b59d9f7a21c5f05fd0692e9
else:
    print "Can't get token for", username

for item in tracks:
    track = item['track']
    print track['name'] + ' - ' + track['artists'][0]['name']