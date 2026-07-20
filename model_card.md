# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
Example: **Personal DJ**

---

## 2. Intended Use

This recommender is a class exploration project, with the mock user being someone with a distinct taste in music.
The system will read through the user profile, and recommend top [5] songs at a time that match the user.

---

## 3. How the Model Works

Scoring is based on the features in the user profile. Every song gets scored by handing out four separate "bonus points" based on how well it matches what the listener said they like, then adding those bonuses together into one total score.

- **Genre match — worth 1 point.** If the song's genre exactly matches the listener's favorite genre, it earns 1 point. There's no partial credit here — it's all-or-nothing, like a yes/no checkbox.
- **Mood match — worth 1 point.** Same idea as genre: an exact match on mood (e.g., "happy," "chill," "intense") earns 1 point, also all-or-nothing.
- **Energy closeness — worth up to 3 points.** Every song has an energy level from 0 (very mellow) to 1 (very intense), and the listener has a target energy they want. The closer the song's energy is to that target, the more points it earns, sliding down to 0 the further away it gets. Unlike genre and mood, this is a sliding scale rather than a checkbox, which is why energy ends up driving the recommendations more than anything else — it can always give partial credit, even for an imperfect match.
- **Acoustic preference — worth 0.5 points.** Songs are labeled "acoustic" or "not acoustic" based on a threshold. If that label matches what the listener said they prefer, they get half a point.

All four bonuses are simply added up into one total score (max possible: 5.5 points). Every song in the catalog gets scored this way, then the songs are sorted highest-to-lowest, and the top 5 become the recommendations shown to the listener, along with plain-English reasons pulled from whichever bonuses it earned.

There's no machine learning involved — it's a transparent point system you could hand-calculate for any song yourself. The one change made from the starter logic was rebalancing the weights: genre was originally worth 2 points and energy topped out at 1.5 points; those were flipped to genre = 1 point and energy = up to 3 points, to test how much more the recommendations lean on energy once it's weighted more heavily than genre.

---

## 4. Data

The catalog has 10 songs, straight from the starter data — nothing added or removed. Genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop (lofi and pop show up most, the rest only once each). Moods: chill, happy, intense, focused, moody, relaxed. Energy levels cluster into two groups — mellow (~0.3–0.4) and high-energy (~0.75–0.9) — with nothing in between, so "moderate energy" taste isn't really represented. The catalog is also too small and narrow to reflect real musical variety: no hip-hop, EDM, classical, or metal, and no way to have more than one genre or mood per song.

---

## 5. Strengths

It works best for listeners whose taste clearly falls into "mellow" or "high-energy" — the Upbeat Pop Fan, Lofi Chill Seeker, and High-Energy Rock Fan profiles all got top picks that genuinely matched their genre, mood, and energy. The reasons printed next to each song are accurate and easy to follow, so it's always clear _why_ a song ranked where it did. It also never breaks on weird input — genres or moods that don't exist just quietly lose their bonus instead of causing errors, which makes the system feel sturdy even when a profile is incomplete or unusual.

---

## 6. Limitations and Bias

The system systematically underserves "moderate energy" listeners while rewarding people who happen to want either chill or intense music — nothing in between.
Tie-breaking favors early rows in the CSV. The Null/Empty Profile (empty genre/mood) generates lots of ties driven only by energy+acoustic, and those ties will always resolve toward whichever song appears first in songs.csv — an accidental "seniority" bias with no relation to fit.

---

## 7. Evaluation

I ran ten different listener profiles through the recommender and read through their top-5 lists to see if the results made sense given each profile's stated taste. Four were "normal" listeners (Upbeat Pop Fan, Lofi Chill Seeker, High-Energy Rock Fan, Relaxed Ambient Listener) and six were deliberately weird or broken profiles meant to poke at the scoring logic (Contradictory Preferences, Nonexistent Mood, Nonexistent Genre, Extreme/Out-of-Range Energy, Case-Sensitivity Trap, Null/Empty Profile).

**What surprised me:** the system never crashes or returns an empty list, even when a profile asks for something that doesn't exist in the catalog (like genre "classical" or mood "sad") — it just quietly drops that bonus and ranks on whatever's left. I also didn't expect how much the energy score ends up driving almost every list once genre/mood can't be matched; energy is really the backbone of this recommender, not genre.

Below are side-by-side comparisons that show what changed between related profiles and why that change makes sense.

- **Upbeat Pop Fan vs. Lofi Chill Seeker** — Opposite energy targets (0.8 vs. 0.3) produce completely non-overlapping top-5 lists. Makes sense: energy is weighted the heaviest, so once the target is on opposite ends of the scale, nothing from one list can score well in the other.

- **Lofi Chill Seeker vs. Relaxed Ambient Listener** — Both want low energy (0.3), just different genre/mood. Their lists share three of the same songs (Library Rain, Coffee Shop Stories, Midnight Coding) because they're pulling from the same "quiet" pool, but the _order_ differs based on which genre/mood actually lines up. This shows genre/mood act as tie-breakers on top of an energy-driven base, not the other way around.

- **High-Energy Rock Fan vs. Contradictory Preferences** — Same genre (rock) and same energy target (0.9), but Contradictory Preferences also asks for mood "chill" and likes_acoustic=True, which no high-energy rock song has. The top pick is still Storm Runner in both cases, but its score drops from 5.47 to 3.97. This is exactly what should happen: the system doesn't get "confused" by the contradiction, it just can't collect bonuses that don't apply, so the score honestly reflects the mismatch.

- **High-Energy Rock Fan vs. Extreme/Out-of-Range Energy** — Same genre/mood, but target_energy jumps from 0.9 to an impossible 1.5. The ranking order barely changes (Storm Runner still wins), but every score drops because no song can get closer than "somewhat far" from 1.5. This confirmed the scoring math doesn't break or go negative on out-of-range inputs — it just treats 1.5 as "further away than anything the catalog can offer."

- **Upbeat Pop Fan vs. Case-Sensitivity Trap** — Identical preferences, just capitalized ("Pop"/"Happy" instead of "pop"/"happy"). The top song stays the same (Sunrise City), but its score falls from 5.44 to 3.44 because the genre and mood bonuses silently fail to trigger on a case mismatch. This was the clearest sign of an actual bug rather than a modeling tradeoff — a real user who types "Pop" instead of "pop" gets a worse experience for no good reason.

- **Upbeat Pop Fan vs. Nonexistent Mood** — Same profile, but "happy" is swapped for "sad" (a mood that doesn't exist in the catalog). The top song is unchanged, and the score drops by exactly 1.0 — precisely the size of the mood bonus. This is a good sanity check: it shows the mood term is cleanly isolated from the rest of the score instead of leaking into other bonuses.

- **Relaxed Ambient Listener vs. Nonexistent Genre** — Same mood/energy/acoustic preferences, but the genre "ambient" is swapped for "classical" (not in the catalog). Both profiles land on the same low-energy songs, just with slightly lower scores for whichever song would have had the genre bonus. Confirms an unmatched genre degrades the score instead of breaking the recommender.

- **Null/Empty Profile vs. Lofi Chill Seeker** — This was the most revealing comparison. The empty profile (target*energy 0.5, no genre/mood) surfaces songs like Midnight Coding, Night Drive Loop, and Rooftop Lights that don't appear in \_any* other profile's top 5. That's because 0.5 sits in a gap between the catalog's "chill" cluster (~0.3–0.4) and "high-energy" cluster (~0.75–0.9) — nothing is close, so the best available songs are middling, unenthusiastic matches. This exposed the "moderate energy" blind spot described in the Limitations section rather than a bug in the code itself.

No numeric metrics beyond the raw scores were used — comparisons were done by reading the printed output for each profile and reasoning about whether the ranking matched what that profile should want.

---

## 8. Future Work

Add a few mid-energy songs to close the gap between "mellow" and "high-energy," and give genre some partial credit for close matches (e.g., "indie pop" should count for something toward "pop") instead of strict exact-match. Make genre and mood matching case-insensitive so typos like "Pop" don't silently lose points. Break ties on something more meaningful than CSV row order — maybe a secondary trait like valence or danceability. Longer term, let listeners list more than one favorite genre or mood, since real taste is rarely just one thing.

---

## 9. Personal Reflection

Building this showed me that recommender systems don't need machine learning — simple, transparent math can work fine. I was also surprised that I didn't need every feature in the dataset to build reasonable scoring logic; as noted in the Limitations section, a more diverse dataset with a wider range of genres would have put that unused headroom to better use.

Returning the top-k songs, rather than a single "best" one, also stood out to me as a simple but effective design choice — it gives the user a range of good options instead of forcing one determinate answer.

AI was a great collaborator throughout this project. Prompting it in plain English and reviewing the generated code saved me time and surfaced solutions I wouldn't have thought of. I also used it to explain unfamiliar concepts so I understood exactly what the code was doing and why, and to revise my README and model card responses.
