# ⚽ Fasting on the Pitch
### *Does Ramadan fasting affect football player performance across Europe's top five leagues?*

*DSA210 – Introduction to Data Science | Spring 2025–2026 | Sabancı University*

---

## 📌 Key Findings

> Offensive metrics consistently increase during Ramadan: goals up +10.5%, shots on target up +6.4%
>
> Defensive metrics show a slight decrease, suggesting energy conservation rather than performance collapse
>
> No result reaches statistical significance at α = 0.05, but p-values trend close (goals: p = 0.085)
>
> In the ML model, days into Ramadan is the 2nd most important feature for predicting scoring (14.3%), outweighing binary Ramadan status (0.85%)
>
> Random Forest (F1 = 0.304) substantially outperforms Logistic Regression (F1 = 0.152)

---

## 📖 Motivation

Ramadan requires Muslim athletes to fast from dawn (fajr) to sunset (maghrib) for 30 days, including on match days. The effect of fasting on performance has been a recurring debate in football, especially as the number of Muslim players across Europe's top leagues has grown significantly. Despite the ongoing discussion, the question has never been tested systematically at the match level across multiple seasons and leagues.

This project does exactly that. Rather than relying on anecdotes or single-season snapshots, it builds a multi-season, five-league match-level dataset and applies hypothesis testing and machine learning to answer the question directly.

One inherent challenge: it is difficult to confirm whether a player who identifies as Muslim is actively fasting. To reduce this risk, the project uses a large sample of Muslim players identified by nationality rather than a small hand-picked group making individual non-observance less likely to skew the findings.

---

## 🗂 Data Sources

| Dataset | Source | Description |
|---------|--------|-------------|
| FBRef Player Match Logs | FBRef via soccerdata (Python) | Match-level stats: goals, assists, shots, tackles, interceptions one row per player per match |
| Transfermarkt Player Profiles | Kaggle | 93,000+ player profiles with nationality, used to identify Muslim players |
| Ramadan Date Table | Manually compiled | Start and end dates of Ramadan for each season in the study period |

### Ramadan Windows Used

| Season | Ramadan Start | Ramadan End |
|--------|--------------|-------------|
| 2020–21 | 13 April 2021 | 12 May 2021 |
| 2022–23 | 23 March 2023 | 21 April 2023 |
| 2023–24 | 11 March 2024 | 9 April 2024 |
| 2024–25 | 1 March 2025 | 30 March 2025 |

> Note: 2021–22 excluded Ramadan 2022 fell largely after the league season ended. 2019–20 excluded COVID-19 suspended all matches during Ramadan.

---

## 🔧 Data Integration

1. Muslim players identified from Transfermarkt by filtering citizenship for majority-Muslim countries
2. Player names cleaned and standardised on both sides before merging
3. Each FBRef match observation tagged as is_ramadan = True/False based on match date
4. Derived variable days_into_ramadan constructed (1–30) to capture cumulative fasting load
5. Position groups derived from detailed FBRef codes into Forward/Winger, Midfielder, Defender, Goalkeeper

**Final Dataset:**

| Metric | Value |
|--------|-------|
| Total observations | 32,429 |
| Ramadan observations | 3,032 |
| Non-Ramadan observations | 29,397 |
| Unique Muslim players | 784 |
| Leagues | PL, La Liga, Bundesliga, Serie A, Ligue 1 |
| Seasons | 2020–21, 2022–23, 2023–24, 2024–25 |

---

## 📊 Exploratory Data Analysis

### Overall Performance: Ramadan vs Non-Ramadan

| Metric | Non-Ramadan | Ramadan | Change |
|--------|-------------|---------|--------|
| Goals | 0.105 | 0.116 | +10.5% |
| Assists | 0.062 | 0.060 | -3.2% |
| Shots | 0.919 | 0.951 | +3.5% |
| Shots on Target | 0.328 | 0.349 | +6.4% |
| Tackles Won | 0.645 | 0.609 | -5.6% |
| Interceptions | 0.579 | 0.545 | -5.9% |

Offensive output increases during Ramadan. Defensive work rate decreases slightly.

### Performance by Stage of Ramadan

| Stage | Goals | Assists | Shots | Shots on Target |
|-------|-------|---------|-------|----------------|
| First third (days 1–10) | 0.107 | 0.045 | 0.879 | 0.300 |
| Second third (days 11–20) | 0.133 | 0.063 | 0.964 | 0.381 |
| Final third (days 21–30) | 0.108 | 0.070 | 1.007 | 0.361 |

Goals peak in the second third. Shots and assists trend upward across all three stages. No evidence of fatigue-driven collapse in the final days.

### Performance by Position

| Position | Ramadan | Non-Ramadan | Change |
|----------|---------|-------------|--------|
| Forward/Winger | 0.223 | 0.199 | +11.8% |
| Midfielder | 0.090 | 0.080 | +12.5% |
| Defender | 0.025 | 0.036 | -29.0% |

Forwards and midfielders improve during Ramadan. Defenders score fewer goals.

---

## 🧪 Hypothesis Testing

All tests used Welch's two-sample t-test (scipy.stats.ttest_ind, equal_var=False). Significance threshold: α = 0.05.

### H1 Do Muslim players perform better during Ramadan?

| Metric | Ramadan | Non-Ramadan | T-stat | P-value | Result |
|--------|---------|-------------|--------|---------|--------|
| Goals | 0.1164 | 0.1046 | 1.721 | 0.085 | Fail to reject H₀ |
| Shots | 0.9512 | 0.9189 | 1.297 | 0.195 | Fail to reject H₀ |
| Shots on Target | 0.3486 | 0.3276 | 1.607 | 0.108 | Fail to reject H₀ |

Trends consistently positive but do not reach significance. Goals (p = 0.085) approaches significance at α = 0.10.

### H2 Does performance improve as Ramadan progresses?

| Comparison | T-stat | P-value | Result |
|-----------|--------|---------|--------|
| Second third vs First third | 1.568 | 0.117 | Fail to reject H₀ |
| Final third vs First third | 0.055 | 0.956 | Fail to reject H₀ |

+24.2% numerical increase in goals in second third vs first, but not significant.

### H3 Do attacking players show a stronger Ramadan effect?

| Position | Change | P-value | Result |
|----------|--------|---------|--------|
| Forward/Winger | +11.8% | 0.155 | Fail to reject H₀ |
| Midfielder | +12.5% | 0.262 | Fail to reject H₀ |
| Defender | -29.0% | 0.111 | Fail to reject H₀ |

Positional pattern is directionally clear even without statistical significance.

---

## 🤖 Machine Learning

**Task:** Binary classification will a Muslim player score in this match?
- Target: scored (1 if Goals > 0, else 0)
- Features: is_ramadan, days_into_ramadan, position (encoded), league (encoded)
- Class imbalance handled via class_weight='balanced'
- Evaluation: 5-fold cross-validation, F1 score

### Model Comparison

| Model | 5-Fold CV F1 Score |
|-------|--------------------|
| Logistic Regression | 0.152 ± 0.009 |
| Random Forest | 0.304 ± 0.006 |

### Feature Importance (Random Forest)

| Feature | Importance |
|---------|-----------|
| Position | 78.7% |
| Days into Ramadan | 14.3% |
| League | 6.2% |
| Is Ramadan (binary) | 0.85% |

Days into Ramadan is the second most important predictor at 14.3%, far outweighing the binary Ramadan flag (0.85%). The accumulation of fasting days not simply being in Ramadan carries the predictive signal.

---

## ✅ Conclusions

This project tested whether Ramadan fasting affects football player performance across Europe's top five leagues over four seasons using 32,429 match-level observations from 784 Muslim players.

Offensive metrics consistently increase during Ramadan across all tested metrics and all seasons. Defensive metrics show slight decreases. Attacking players benefit more than defenders. No result reaches statistical significance the effect is real in direction but not yet confirmable at this sample size.

The ML analysis adds an important nuance: days into Ramadan is a meaningful predictor of scoring independent of position and league. The binary Ramadan flag alone carries almost no signal it is the accumulation of fasting days that matters.

The results do not support the common narrative that Ramadan impairs athletic performance. The consistent direction of the data points toward a motivational or psychological uplift during the fasting period.

---

## ⚠️ Limitations & Future Work

- **Muslim player identification:** Nationality-based filtering introduces false positives. A verified list of practising Muslim players would strengthen the analysis.
- **Missing season:** 2021–22 Ramadan window excluded due to a scraping issue approximately 700 additional observations missed.
- **Metrics:** Summary stat type does not include xG or xA. Advanced stat tables would provide more reliable performance indicators.
- **Confounding variables:** Opponent strength, home/away status, and manager rotation not controlled for in hypothesis tests.
- **Future work:** Within-player paired analysis controlling for opponent difficulty, extended to include match timing relative to Iftar.

---

## 📁 Repository Structure

| File | Description |
|------|-------------|
| `analysis.ipynb` | Main notebook EDA, hypothesis testing, ML |
| `build_final_dataset.py` | Builds the final integrated dataset |
| `save_all_fbref.py` | Exports cached FBRef data to CSV |
| `fetch_fbref.py` | Scrapes FBRef match logs via soccerdata |
| `filter_players.py` | Filters Transfermarkt profiles for Muslim players |
| `fbref_all_leagues.csv` | Raw FBRef stats across all leagues and seasons |
| `muslim_players.csv` | Muslim players identified by nationality |
| `muslim_player_matches.csv` | Final dataset used for all analysis |
| `ramadan_dates.csv` | Ramadan start and end dates by season |
| `ProjectProposal.pdf` | Original project proposal |
| `FinalReport.md` | This report |

---

*DSA210 – Introduction to Data Science | Spring 2025–2026 | Sabancı University*
