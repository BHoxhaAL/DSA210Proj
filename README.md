# DSA210Proj
Project Proposal
DSA210 – Introduction to Data Science (Spring 2025–2026)

1. Motivation

Ramadan requires Muslim athletes to fast from dawn (fajr) to sunset (maghrib) for 30 days, including on match days. The effects of fasting on player performance has been a hot topic in football, especially in recent years as the number of Muslim players across Europe's top leagues has grown. Despite the ongoing debates, the question has never been faced directly head on. This project aims to do exactly that: does fasting during Ramadan measurably affect player performance across Europe's top five leagues? One challenge in this type of analysis is that it is difficult to confirm whether a player who identifies as Muslim is actually fasting. Therefore to reduce this risk, the project uses a larger sample of Muslim players rather than a small hand-picked group, making the findings less likely to be skewed.


2. Datasets
   
a. FBRef Player Match Logs
Source: FBRef (stathead.com/fbref)
Description: Match-level player statistics covering the top five European leagues (Premier League, La Liga, Bundesliga, Serie A, Ligue 1) from 2020-21 to 2025-26, spanning six Ramadan windows. It provides detailed performance metrics for every game played, collected programmatically using Python.
b. Transfermarkt Player Profiles
Source: Kaggle (kaggle.com/datasets/xfkzujqjvx97n/football-datasets)
Description: Comprehensive player profiles including nationality for over 93,000 players worldwide, used to identify Muslim players at scale by filtering for players from majority-Muslim countries.
c. Ramadan Date Table
Source: Manually compiled using Islamic calendar sources (e.g. Prayer Times Calendar, London UK)
Description: A table recording the start and end dates of Ramadan from 2021 to 2026, used to classify each match observation as falling inside or outside the fasting period.
d. FPL Player Logs (Fallback)
Source: Kaggle (kaggle.com/datasets/franeksakowski/fpl-player-logs)
Description: Match-level player observations for Premier League players covering the 2021-22 and 2022-23 seasons. Used as a fallback if FBRef data collection proves unfeasible.

3. Data Integration Plan

Muslim players are first identified from the Transfermarkt profiles by nationality. Their match logs are then pulled from FBRef and each match observation is tagged as Ramadan or non-Ramadan using the date table. Two derived variables are constructed: days elapsed since Ramadan start at kickoff, capturing cumulative fasting load, and a binary Ramadan flag. The final dataset contains one row per Muslim player per match, with performance metrics, Ramadan status, and fasting load.

4. Hypotheses

Main Hypothesis (H₁)
Muslim players in Europe's top five leagues show a statistically significant improvement in performance during Ramadan compared to their own non-Ramadan baseline within the same season, driven by heightened motivation, willpower, and mental focus.
Null Hypothesis (H₀)
Fasting during Ramadan has no statistically significant effect on player performance.
Secondary Hypothesis (H₂)
The performance improvement strengthens as Ramadan progresses — players in the final third of the fasting period perform better than those in the first third, as mental and spiritual resilience builds over time.
Third Hypothesis (H₃)
Players in high-intensity positions (forwards, midfielders) show a stronger performance improvement during Ramadan than players in lower-intensity positions (defenders, goalkeepers), reflecting the greater role of motivation and willpower in attacking play.

5. Expected Outcomes

A match-level dataset linking player performance metrics to Ramadan fasting periods across six seasons and five leagues. Identification of whether fasting produces a statistically significant and consistent effect on key performance indicators. Quantification of how fasting load accumulates over the month and whether position moderates the effect. A machine learning model predicting player performance outcomes using Ramadan status, fasting load, position, and opponent strength as features.
