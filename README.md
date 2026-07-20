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
