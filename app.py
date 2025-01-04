from flask import Flask , jsonify, request, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
from emotion_detector import detect_emotion
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
    
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

emotion_dict = {0: "Angry", 1: "Disgust", 2: "Anxious", 3: "Happy", 4: "Sad", 5: "Surprise", 6: "Relaxed"}
emotion_profiles = {
    "happy": [
        # Upbeat and energetic
        {"valence": 0.9, "energy": 0.9, "danceability": 0.8, "acousticness": 0.2, "loudness": -5.0, "tempo": 140},
        # Cheerful and relaxed
        {"valence": 0.8, "energy": 0.7, "danceability": 0.7, "acousticness": 0.4, "loudness": -8.0, "tempo": 120},
    ],
    "sad": [
        # Slow and reflective
        {"valence": 0.2, "energy": 0.2, },
        # # Melancholic yet dynamic
        # {"valence": 0.3, "energy": 0.4, "danceability": 0.1, "acousticness": 0.5, "loudness": -15.0, "tempo": 90},
    ],
    "angry": [
        # High intensity and aggressive
        {"valence": 0.1, "energy": 0.95, "danceability": 0.6, "acousticness": 0.05, "loudness": -3.0, "tempo": 150},
        # Rhythmic but intense
        {"valence": 0.2, "energy": 0.85, "danceability": 0.7, "acousticness": 0.1, "loudness": -6.0, "tempo": 130},
    ],
    "relaxed": [
        # Calm and soothing
        {"valence": 0.8, "energy": 0.3, "danceability": 0.4, "acousticness": 0.9, "loudness": -20.0, "tempo": 70},
        # Easy-going and chill
        {"valence": 0.7, "energy": 0.4, "danceability": 0.5, "acousticness": 0.7, "loudness": -15.0, "tempo": 90},
    ],
    "surprise": [
        # High tempo, dynamic surprises
        {"valence": 0.7, "energy": 0.9, "danceability": 0.8, "acousticness": 0.3, "loudness": -8.0, "tempo": 160},
    ],
    "disgust": [
        # Dark and unsettling
        {"valence": 0.2, "energy": 0.4, "danceability": 0.3, "acousticness": 0.6, "loudness": -15.0, "tempo": 80},
    ],
    "anxious": [
        # Fast and erratic
        {"valence": 0.3, "energy": 0.8, "danceability": 0.5, "acousticness": 0.2, "loudness": -10.0, "tempo": 140},
    ],
}
# seed_genres = {
#     "happy": ["indian", "dance", "pop"],       # Joyful Indian songs
#     "sad":   [ "sad","indian"],     # Emotional and melancholic tracks
#     "angry": ["indian", "rock", "metal"],         # Intense Indian tracks
#     "relaxed": ["indian", "chill", "ambient"],    # Soothing Indian music
#     "surprise": ["indian", "edm", "dance"],       # Upbeat Indian tracks
#     "disgust": ["indian", "lofi", "indie"],       # Reflective or moody Indian songs
#     "anxious": ["indian", "cinematic", "trance"]  # Dramatic Indian soundtracks
# }

def get_songs_for_emotion(emotion):
    """
    Fetch Bollywood songs based on detected emotion using Spotify's recommendations API.
    """
    profile = emotion_profiles.get(emotion, {})
    recommendations = sp.recommendations(
        country="IN",
        seed_genres =  ["indian"],  # Genre seed for Bollywood/Hindi songs
        limit=10,
        **profile
    )

    # Extract track names
    return [[track["name"],track["external_urls"]['spotify']]for track in recommendations["tracks"]]

# @app.route('/detect-emotion-and-recommend', methods=['GET'])
@app.route('/detect-emotion-and-recommend', methods=['GET','POST'])
def recommend_songs():
    """
    Detect emotion and recommend Bollywood songs.
    """
    if request.method == 'POST':
        emotion = emotion_dict[detect_emotion()]
        if not emotion:
            return jsonify({"error": "No face detected. Please try again."}), 400

        songs = get_songs_for_emotion(emotion)
        #return jsonify({"emotion": emotion, "songs": songs})
        print(songs)
        return jsonify({"emotion": emotion, "songs": songs})
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)