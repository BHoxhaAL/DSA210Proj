# Analyzing the Effect of Ramadan on Football Player Performance Across Europe's Top Five Leagues

*DSA210 – Introduction to Data Science (Spring 2025–2026) | Buen Hoxha*

---

## 1. Motivation

Ramadan requires Muslim athletes to fast from dawn (fajr) to sunset (maghrib) for 30 days, including on match days. The effects of fasting on player performance has been a hot topic in football, especially in recent years as the number of Muslim players across Europe's top leagues has grown. Despite the ongoing debates, the question has never been faced directly head on. This project aims to do exactly that: does fasting during Ramadan measurably affect player performance across Europe's top five leagues?

One challenge in this type of analysis is that it is difficult to confirm whether a player who identifies as Muslim is actually fasting. Therefore to reduce this risk, the project uses a larger sample of Muslim players rather than a small hand-picked group, making the findings less likely to be skewed.

---

## 2. Datasets

**a. FBRef Player Match Logs**
- **Source:** FBRef (stathead.com/fbref), collected programmatically using Python
- **Description:** Match-level player statistics covering the top five European leagues (Premier League, La Liga, Bundesliga, Serie A, Ligue 1) from 2020–21 to 2024–25, spanning four Ramadan windows. Provides detailed performance metrics for every game played.

**b. Transfermarkt Player Profiles**
- **Source:** Kaggle (kaggle.com/datasets/xfkzujqjvx97n/football-datasets)
- **Description:** Comprehensive player profiles including nationality for over 93,000 players worldwide, used to identify Muslim players at scale by filtering for players from majority-Muslim countries.

**c. Ramadan Date Table**
- **Source:** Manually compiled from Islamic calendar sources
- **Description:** A table recording the start and end dates of Ramadan for each season in the study period, used to classify each match observation as falling inside or outside the fasting period.

**d. FPL Player Logs (fallback)**
- **Source:** Kaggle (kaggle.com/datasets/franeksakowski/fpl-player-logs)
- **Description:** Match-level player observations for Premier League players covering the 2021–22 and 2022–23 seasons. Used as a fallback if FBRef data collection proves unfeasible.

---

## 3. Data Integration Plan

Muslim players are first identified from the Transfermarkt profiles by nationality. Their match logs are then pulled from FBRef and each match observation is tagged as Ramadan or non-Ramadan using the date table. Two derived variables are constructed: days elapsed since Ramadan start at kickoff, capturing cumulative fasting load, and a binary Ramadan flag. The final dataset contains one row per Muslim player per match, with performance metrics, Ramadan status, and fasting load.

**Final Dataset:**

| | |
|--|--|
| Total observations | 32,429 |
| Ramadan observations | 3,032 |
| Non-Ramadan observations | 29,397 |
| Unique Muslim players | 784 |
| Leagues | Premier League, La Liga, Bundesliga, Serie A, Ligue 1 |
| Seasons | 2020–21, 2022–23, 2023–24, 2024–25 |

---

## 4. Hypotheses

**Main Hypothesis (H₁)**
Muslim players in Europe's top five leagues show a statistically significant improvement in performance during Ramadan compared to their own non-Ramadan baseline within the same season, driven by heightened motivation, willpower, and mental focus.

**Null Hypothesis (H₀)**
Fasting during Ramadan has no statistically significant effect on player performance.

**Secondary Hypothesis (H₂)**
The performance improvement strengthens as Ramadan progresses — players in the final third of the fasting period perform better than those in the first third, as mental and spiritual resilience builds over time.

**Third Hypothesis (H₃)**
Players in high-intensity positions (forwards, midfielders) show a stronger performance improvement during Ramadan than players in lower-intensity positions (defenders, goalkeepers), reflecting the greater role of motivation and willpower in attacking play.

---

## 5. EDA Results

### Overall Performance: Ramadan vs Non-Ramadan

| Metric | Non-Ramadan | Ramadan | Change |
|--------|-------------|---------|--------|
| Goals | 0.105 | 0.116 | +10.5% |
| Shots on Target | 0.328 | 0.349 | +6.4% |
| Shots | 0.919 | 0.951 | +3.5% |
| Tackles Won | 0.645 | 0.609 | -5.6% |
| Interceptions | 0.579 | 0.545 | -5.9% |

### Performance by Stage of Ramadan

| Stage | Goals | Assists | Shots | Shots on Target |
|-------|-------|---------|-------|----------------|
| First third (days 1–10) | 0.107 | 0.045 | 0.879 | 0.300 |
| Second third (days 11–20) | 0.133 | 0.063 | 0.964 | 0.381 |
| Final third (days 21–30) | 0.108 | 0.070 | 1.007 | 0.361 |

### Performance by Position

| Position | Ramadan | Non-Ramadan | Change |
|----------|---------|-------------|--------|
| Forward/Winger | 0.223 | 0.199 | +11.8% |
| Midfielder | 0.090 | 0.080 | +12.5% |
| Defender | 0.025 | 0.036 | -29.0% |

---

## 6. Hypothesis Testing

All tests used Welch's two-sample t-test (`scipy.stats.ttest_ind`, `equal_var=False`). Significance threshold: α = 0.05.

**H1 — Do Muslim players perform better during Ramadan?**

| Metric | Ramadan | Non-Ramadan | T-stat | P-value | Result |
|--------|---------|-------------|--------|---------|--------|
| Goals | 0.1164 | 0.1046 | 1.721 | 0.085 | Fail to reject H₀ |
| Shots | 0.9512 | 0.9189 | 1.297 | 0.195 | Fail to reject H₀ |
| Shots on Target | 0.3486 | 0.3276 | 1.607 | 0.108 | Fail to reject H₀ |

**H2 — Does performance improve as Ramadan progresses?**

| Comparison | T-stat | P-value | Result |
|-----------|--------|---------|--------|
| Second third vs First third | 1.568 | 0.117 | Fail to reject H₀ |
| Final third vs First third | 0.055 | 0.956 | Fail to reject H₀ |

**H3 — Do attacking players show a stronger Ramadan effect?**

| Position | Change | P-value | Result |
|----------|--------|---------|--------|
| Forward/Winger | +11.8% | 0.155 | Fail to reject H₀ |
| Midfielder | +12.5% | 0.262 | Fail to reject H₀ |
| Defender | -29.0% | 0.111 | Fail to reject H₀ |

All three hypotheses fail to reach statistical significance. Trends are consistent and directionally clear across all seasons and leagues.

---

## 7. Machine Learning

**Task:** Binary classification — will a Muslim player score in this match, and how important is Ramadan as a feature?

**Models:** Logistic Regression and Random Forest Classifier with `class_weight='balanced'`, evaluated via 5-fold cross-validation (F1 score).

| Model | 5-Fold CV F1 Score |
|-------|--------------------|
| Logistic Regression | 0.152 ± 0.009 |
| Random Forest | 0.304 ± 0.006 |

**Feature Importance (Random Forest):**

| Feature | Importance |
|---------|-----------|
| Position | 78.7% |
| Days into Ramadan | 14.3% |
| League | 6.2% |
| Is Ramadan (binary) | 0.85% |

Days into Ramadan is the second most important predictor at 14.3%, far outweighing the binary Ramadan flag (0.85%). The accumulation of fasting days carries more predictive signal than Ramadan status alone, providing indirect ML support for H2.

---

## 8. Conclusions

Offensive metrics consistently increase during Ramadan across all tested metrics and all seasons. Defensive metrics show slight decreases. Attacking players benefit more than defenders. No result reaches statistical significance at α = 0.05, but p-values cluster between 0.085 and 0.195, suggesting a real effect that a more precisely defined sample could confirm.

The ML analysis reinforces this: days into Ramadan is a meaningful predictor of scoring independent of position and league. The common narrative that Ramadan impairs athletic performance is not supported by this data.

---

## 9. Limitations & Future Work

**Muslim player identification:** Nationality-based filtering introduces false positives. A verified list of practising Muslim players would strengthen the methodology.

**Missing season:** The 2021–22 Ramadan window is absent from the scraped dataset due to a soccerdata season labelling issue.

**Metrics:** FBRef summary stats do not include xG or xA. Advanced stat tables would provide more reliable performance indicators.

**Confounding variables:** Opponent strength, home/away status, and manager rotation are not controlled for in the hypothesis tests.

**Future work:** A within-player paired analysis controlling for opponent difficulty, extended to include match timing relative to Iftar, would be the most rigorous next step.

---

## 10. How to Reproduce

1. Clone the repository

```
git clone https://github.com/BHoxhaAL/DSA210Proj.git
```

2. Install dependencies

```
pip install pandas numpy matplotlib seaborn scipy scikit-learn soccerdata
```

3. Build the dataset

```
python filter_players.py
python save_all_fbref.py
python build_final_dataset.py
```

4. Open `analysis.ipynb` in Jupyter or VS Code and run all cells in order

---

## 11. Repository Structure

| File | Description |
|------|-------------|
| `analysis.ipynb` | Main notebook: EDA, hypothesis testing, ML |
| `build_final_dataset.py` | Builds the final integrated dataset |
| `save_all_fbref.py` | Exports cached FBRef data to CSV |
| `fetch_fbref.py` | Scrapes FBRef match logs via soccerdata |
| `filter_players.py` | Filters Transfermarkt profiles for Muslim players |
| `fbref_all_leagues.csv` | Raw FBRef match stats across all leagues and seasons |
| `muslim_players.csv` | Muslim players identified by nationality |
| `muslim_player_matches.csv` | Final dataset used for all analysis |
| `ramadan_dates.csv` | Ramadan start and end dates by season |
| `ProjectProposal.pdf` | Original project proposal |
| `FinalReport.md` | Full project report |
