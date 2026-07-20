"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.")

    # Example user profiles, each favoring a different corner of the catalog
    profiles = [
        (
            "Upbeat Pop Fan",
            {
                "favorite_genre": "pop",
                "favorite_mood": "happy",
                "target_energy": 0.8,
                "likes_acoustic": False,
            },
        ),
        (
            "Lofi Chill Seeker",
            {
                "favorite_genre": "lofi",
                "favorite_mood": "chill",
                "target_energy": 0.3,
                "likes_acoustic": True,
            },
        ),
        (
            "High-Energy Rock Fan",
            {
                "favorite_genre": "rock",
                "favorite_mood": "intense",
                "target_energy": 0.9,
                "likes_acoustic": False,
            },
        ),
        (
            "Relaxed Ambient Listener",
            {
                "favorite_genre": "ambient",
                "favorite_mood": "relaxed",
                "target_energy": 0.3,
                "likes_acoustic": True,
            },
        ),
        # Adversarial / edge case profiles: designed to probe scoring logic
        # rather than represent a typical listener.
        (
            "Contradictory Preferences",
            {
                "favorite_genre": "rock",
                "favorite_mood": "chill",
                "target_energy": 0.9,
                "likes_acoustic": True,
            },
        ),
        (
            "Nonexistent Mood",
            {
                "favorite_genre": "pop",
                "favorite_mood": "sad",
                "target_energy": 0.8,
                "likes_acoustic": False,
            },
        ),
        (
            "Nonexistent Genre",
            {
                "favorite_genre": "classical",
                "favorite_mood": "relaxed",
                "target_energy": 0.3,
                "likes_acoustic": True,
            },
        ),
        (
            "Extreme/Out-of-Range Energy",
            {
                "favorite_genre": "rock",
                "favorite_mood": "intense",
                "target_energy": 1.5,
                "likes_acoustic": False,
            },
        ),
        (
            "Case-Sensitivity Trap",
            {
                "favorite_genre": "Pop",
                "favorite_mood": "Happy",
                "target_energy": 0.8,
                "likes_acoustic": False,
            },
        ),
        (
            "Null/Empty Profile",
            {
                "favorite_genre": "",
                "favorite_mood": "",
                "target_energy": 0.5,
                "likes_acoustic": False,
            },
        ),
    ]

    for name, user_prefs in profiles:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\nTop Recommendations for {name}")
        print("=" * 40)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n{rank}. {song['title']}  (Score: {score:.2f})")
            for reason in explanation.split("; "):
                print(f"   - {reason}")
        print()


if __name__ == "__main__":
    main()
