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
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
else:
    print "Can't get token for", username

for item in tracks:
    track = item['track']
    print track['name'] + ' - ' + track['artists'][0]['name']