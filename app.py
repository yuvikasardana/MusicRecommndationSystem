from flask import Flask , jsonify
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
        # Upbeat, danceable happy music
        {"valence": 0.9, "energy": 0.8, "danceability": 0.9, "acousticness": 0.1, "loudness": -5.0, "tempo": 130},
        # Cheerful, relaxed happy music
        {"valence": 0.8, "energy": 0.6, "danceability": 0.7, "acousticness": 0.3, "loudness": -8.0, "tempo": 110},
    ],
    "sad": [
        # Soft, melancholic profile
        {"valence": 0.2, "energy": 0.3, "danceability": 0.4, "acousticness": 0.8, "loudness": -15.0, "tempo": 70},
        # Reflective, bittersweet profile
        {"valence": 0.3, "energy": 0.5, "danceability": 0.6, "acousticness": 0.4, "loudness": -10.0, "tempo": 90},
    ],
    "angry": [
        # Intense, high-energy angry music
        {"valence": 0.1, "energy": 0.9, "danceability": 0.6, "acousticness": 0.05, "loudness": -3.0, "tempo": 150},
        # Aggressive yet rhythmic angry music
        {"valence": 0.2, "energy": 0.8, "danceability": 0.7, "acousticness": 0.1, "loudness": -6.0, "tempo": 130},
    ],
    "relaxed": [
        # Calm, acoustic, and soft relaxed music
        {"valence": 0.8, "energy": 0.4, "danceability": 0.5, "acousticness": 0.8, "loudness": -12.0, "tempo": 80},
        # Laid-back, moderately energetic relaxing music
        {"valence": 0.7, "energy": 0.5, "danceability": 0.6, "acousticness": 0.5, "loudness": -10.0, "tempo": 90},
    ],
    "Surprise": {"valence": 0.7, "energy": 0.9, "danceability": 0.7, "tempo": 160},
    "Disgust": {"target_valence": 0.2, "target_energy": 0.4, "target_danceability": 0.4, "target_tempo": 120},
    "Anxious": {"target_valence": 0.3, "target_energy": 0.7, "target_danceability": 0.4, "target_tempo": 140}

}
def get_songs_for_emotion(emotion):
    """
    Fetch Bollywood songs based on detected emotion using Spotify's recommendations API.
    """
    profile = emotion_profiles.get(emotion, {})
    recommendations = sp.recommendations(
        seed_genres=["indian"],  # Genre seed for Bollywood/Hindi songs
        limit=10,
        **profile
    )

    # Extract track names
    return [track["name"] for track in recommendations["tracks"]]

# @app.route('/detect-emotion-and-recommend', methods=['GET'])
def recommend_songs():
    """
    Detect emotion and recommend Bollywood songs.
    """
    emotion = detect_emotion()
    if not emotion:
        return jsonify({"error": "No face detected. Please try again."}), 400

    songs = get_songs_for_emotion(emotion)
    #return jsonify({"emotion": emotion, "songs": songs})
    print(songs)

recommend_songs()

# if __name__ == '__main__':
#     app.run(debug=True)