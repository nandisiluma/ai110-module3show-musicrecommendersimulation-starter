# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How real world recommender systems work (e.g. Netflix)

1. Content-based Filtering: recommend items that are similar in their own attributes to things the user already likes. No other users are needed — just item features and a user profile.

2. Collaborative Filtering: recommend items based on patterns across many users' behavior, ignoring the content of the items themselves. "Users who liked what you liked also liked X."

## How The System Works

This recommender is content-based: it doesn't look at what other users liked, only at how closely each song's own attributes match a single listener's stated taste.

**What a `Song` looks like:**
Each song has a `genre`, `mood`, and four numeric traits — `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness` — all rated on their own scale (most from 0 to 1).

**What a `UserProfile` stores:**
A listener's taste is captured as a `favorite_genre`, a `favorite_mood`, a `target_energy` (how high-energy they want their music, from mellow to intense), and whether they `likes_acoustic` music.

**How a song gets scored (the Scoring Rule):**
Every song is compared to the user's profile one piece at a time, and each piece contributes points to a single score. Max possible score: **5.0**.

| Signal           | Weight         | Formula                                                                                                                                                        |
| ---------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Genre match      | **+2.0**       | Full points if `song.genre == user.favorite_genre`, else 0.                                                                                                    |
| Mood match       | **+1.0**       | Full points if `song.mood == user.favorite_mood`, else 0.                                                                                                      |
| Energy closeness | **up to +1.5** | `1.5 * (1 - abs(song.energy - user.target_energy))`, floored at 0. Linear falloff — no cliff, just diminishing credit the further the song is from the target. |
| Acoustic fit     | **+0.5**       | Full points if `user.likes_acoustic == (song.acousticness > 0.5)` — i.e. the song's acousticness lands on the side of the 0.5 threshold the user prefers.      |

Genre is weighted heaviest because with 7 distinct genres across the 10-song catalog (`data/songs.csv`), an exact match is a strong, relatively rare signal. Mood gets half that weight since moods cluster more (`chill` appears 3 times, `happy`/`intense` twice each), so a mood match alone doesn't separate songs as well. Energy is a graded comparison rather than a yes/no match, so it's scaled continuously up to 1.5 points. Acoustic fit gets the smallest weight since it's a single boolean signal rather than a nuanced comparison — the 0.5 threshold happens to split this catalog's songs evenly (5 above, 5 below).

**Potential Bias:** This makes genre dominant — a genre mismatch costs a song 40% of the max score, which could bury a song that's a near-perfect mood/energy fit.

**How recommendations are chosen (the Ranking Rule):** scoring only tells you how good _one_ song is for the user — it doesn't decide what to actually show. Once every song in the catalog has a score, the system sorts all of them from highest to lowest and returns the top `k`. This separate step is also where the system would handle ties, an empty catalog, or a catalog smaller than `k`.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
<!-- Loaded 10 songs.

Top Recommendations
========================================

1. Sunrise City  (Score: 4.97)
   - Genre matches your favorite (pop)
   - Mood matches your favorite (happy)
   - Energy (0.82) is close to your target (0.8)
   - Matches your acoustic preference

2. Gym Hero  (Score: 3.80)
   - Genre matches your favorite (pop)
   - Energy (0.93) is close to your target (0.8)
   - Matches your acoustic preference

3. Rooftop Lights  (Score: 2.94)
   - Mood matches your favorite (happy)
   - Energy (0.76) is close to your target (0.8)
   - Matches your acoustic preference

4. Night Drive Loop  (Score: 1.92)
   - Energy (0.75) is close to your target (0.8)
   - Matches your acoustic preference

5. Storm Runner  (Score: 1.83)
   - Energy (0.91) is close to your target (0.8)
   - Matches your acoustic preference -->
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

```
Tried a few different user profiles and got the following results:

Top Recommendations for Upbeat Pop Fan
========================================

1. Sunrise City  (Score: 4.97)
   - Genre matches your favorite (pop)
   - Mood matches your favorite (happy)
   - Energy (0.82) is close to your target (0.8)
   - Matches your acoustic preference

2. Gym Hero  (Score: 3.80)
   - Genre matches your favorite (pop)
   - Energy (0.93) is close to your target (0.8)
   - Matches your acoustic preference

3. Rooftop Lights  (Score: 2.94)
   - Mood matches your favorite (happy)
   - Energy (0.76) is close to your target (0.8)
   - Matches your acoustic preference

4. Night Drive Loop  (Score: 1.92)
   - Energy (0.75) is close to your target (0.8)
   - Matches your acoustic preference

5. Storm Runner  (Score: 1.83)
   - Energy (0.91) is close to your target (0.8)
   - Matches your acoustic preference


Top Recommendations for Lofi Chill Seeker
========================================

1. Library Rain  (Score: 4.92)
   - Genre matches your favorite (lofi)
   - Mood matches your favorite (chill)
   - Energy (0.35) is close to your target (0.3)
   - Matches your acoustic preference

2. Midnight Coding  (Score: 4.82)
   - Genre matches your favorite (lofi)
   - Mood matches your favorite (chill)
   - Energy (0.42) is close to your target (0.3)
   - Matches your acoustic preference

3. Focus Flow  (Score: 3.85)
   - Genre matches your favorite (lofi)
   - Energy (0.4) is close to your target (0.3)
   - Matches your acoustic preference

4. Spacewalk Thoughts  (Score: 2.97)
   - Mood matches your favorite (chill)
   - Energy (0.28) is close to your target (0.3)
   - Matches your acoustic preference

5. Coffee Shop Stories  (Score: 1.90)
   - Energy (0.37) is close to your target (0.3)
   - Matches your acoustic preference


Top Recommendations for High-Energy Rock Fan
========================================

1. Storm Runner  (Score: 4.98)
   - Genre matches your favorite (rock)
   - Mood matches your favorite (intense)
   - Energy (0.91) is close to your target (0.9)
   - Matches your acoustic preference

2. Gym Hero  (Score: 2.96)
   - Mood matches your favorite (intense)
   - Energy (0.93) is close to your target (0.9)
   - Matches your acoustic preference

3. Sunrise City  (Score: 1.88)
   - Energy (0.82) is close to your target (0.9)
   - Matches your acoustic preference

4. Rooftop Lights  (Score: 1.79)
   - Energy (0.76) is close to your target (0.9)
   - Matches your acoustic preference

5. Night Drive Loop  (Score: 1.77)
   - Energy (0.75) is close to your target (0.9)
   - Matches your acoustic preference


Top Recommendations for Relaxed Ambient Listener
========================================

1. Spacewalk Thoughts  (Score: 3.97)
   - Genre matches your favorite (ambient)
   - Energy (0.28) is close to your target (0.3)
   - Matches your acoustic preference

2. Coffee Shop Stories  (Score: 2.90)
   - Mood matches your favorite (relaxed)
   - Energy (0.37) is close to your target (0.3)
   - Matches your acoustic preference

3. Library Rain  (Score: 1.92)
   - Energy (0.35) is close to your target (0.3)
   - Matches your acoustic preference

4. Focus Flow  (Score: 1.85)
   - Energy (0.4) is close to your target (0.3)
   - Matches your acoustic preference

5. Midnight Coding  (Score: 1.82)
   - Energy (0.42) is close to your target (0.3)
   - Matches your acoustic preference


Top Recommendations for Contradictory Preferences
========================================

1. Storm Runner  (Score: 3.48)
   - Genre matches your favorite (rock)
   - Energy (0.91) is close to your target (0.9)

2. Midnight Coding  (Score: 2.28)
   - Mood matches your favorite (chill)
   - Energy (0.42) is close to your target (0.9)
   - Matches your acoustic preference

3. Library Rain  (Score: 2.17)
   - Mood matches your favorite (chill)
   - Energy (0.35) is close to your target (0.9)
   - Matches your acoustic preference

4. Spacewalk Thoughts  (Score: 2.07)
   - Mood matches your favorite (chill)
   - Energy (0.28) is close to your target (0.9)
   - Matches your acoustic preference

5. Gym Hero  (Score: 1.46)
   - Energy (0.93) is close to your target (0.9)


Top Recommendations for Nonexistent Mood
========================================

1. Sunrise City  (Score: 3.97)
   - Genre matches your favorite (pop)
   - Energy (0.82) is close to your target (0.8)
   - Matches your acoustic preference

2. Gym Hero  (Score: 3.80)
   - Genre matches your favorite (pop)
   - Energy (0.93) is close to your target (0.8)
   - Matches your acoustic preference

3. Rooftop Lights  (Score: 1.94)
   - Energy (0.76) is close to your target (0.8)
   - Matches your acoustic preference

4. Night Drive Loop  (Score: 1.92)
   - Energy (0.75) is close to your target (0.8)
   - Matches your acoustic preference

5. Storm Runner  (Score: 1.83)
   - Energy (0.91) is close to your target (0.8)
   - Matches your acoustic preference


Top Recommendations for Nonexistent Genre
========================================

1. Coffee Shop Stories  (Score: 2.90)
   - Mood matches your favorite (relaxed)
   - Energy (0.37) is close to your target (0.3)
   - Matches your acoustic preference

2. Spacewalk Thoughts  (Score: 1.97)
   - Energy (0.28) is close to your target (0.3)
   - Matches your acoustic preference

3. Library Rain  (Score: 1.92)
   - Energy (0.35) is close to your target (0.3)
   - Matches your acoustic preference

4. Focus Flow  (Score: 1.85)
   - Energy (0.4) is close to your target (0.3)
   - Matches your acoustic preference

5. Midnight Coding  (Score: 1.82)
   - Energy (0.42) is close to your target (0.3)
   - Matches your acoustic preference


Top Recommendations for Extreme/Out-of-Range Energy
========================================

1. Storm Runner  (Score: 4.12)
   - Genre matches your favorite (rock)
   - Mood matches your favorite (intense)
   - Energy (0.91) is close to your target (1.5)
   - Matches your acoustic preference

2. Gym Hero  (Score: 2.15)
   - Mood matches your favorite (intense)
   - Energy (0.93) is close to your target (1.5)
   - Matches your acoustic preference

3. Sunrise City  (Score: 0.98)
   - Energy (0.82) is close to your target (1.5)
   - Matches your acoustic preference

4. Rooftop Lights  (Score: 0.89)
   - Energy (0.76) is close to your target (1.5)
   - Matches your acoustic preference

5. Night Drive Loop  (Score: 0.88)
   - Energy (0.75) is close to your target (1.5)
   - Matches your acoustic preference


Top Recommendations for Case-Sensitivity Trap
========================================

1. Sunrise City  (Score: 1.97)
   - Energy (0.82) is close to your target (0.8)
   - Matches your acoustic preference

2. Rooftop Lights  (Score: 1.94)
   - Energy (0.76) is close to your target (0.8)
   - Matches your acoustic preference

3. Night Drive Loop  (Score: 1.92)
   - Energy (0.75) is close to your target (0.8)
   - Matches your acoustic preference

4. Storm Runner  (Score: 1.83)
   - Energy (0.91) is close to your target (0.8)
   - Matches your acoustic preference

5. Gym Hero  (Score: 1.80)
   - Energy (0.93) is close to your target (0.8)
   - Matches your acoustic preference


Top Recommendations for Null/Empty Profile
========================================

1. Night Drive Loop  (Score: 1.62)
   - Energy (0.75) is close to your target (0.5)
   - Matches your acoustic preference

2. Rooftop Lights  (Score: 1.61)
   - Energy (0.76) is close to your target (0.5)
   - Matches your acoustic preference

3. Sunrise City  (Score: 1.52)
   - Energy (0.82) is close to your target (0.5)
   - Matches your acoustic preference

4. Storm Runner  (Score: 1.39)
   - Energy (0.91) is close to your target (0.5)
   - Matches your acoustic preference

5. Midnight Coding  (Score: 1.38)
   - Energy (0.42) is close to your target (0.5)

```

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
