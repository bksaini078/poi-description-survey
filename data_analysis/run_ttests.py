import pandas as pd
import scipy.stats as stats
import numpy as np

# Load data as done in notebook cell
from utils import load_survey_responses
import config

print("Loading survey responses...")
survey_df = load_survey_responses('../survey_results/survey_response/', config.SURVEY_RESPONSES_PATTERN)
survey_df_unique = survey_df.drop_duplicates(subset=['user_id'], keep='last')

# Prepare data: filter for German and Indian
df_demog = survey_df_unique[survey_df_unique['nationality'].isin(['German', 'Indian'])].copy()

# Likert Ratings across Demographics (Independent t-test)
metric_categories = {
    "significance": ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
    "trust": ["Not at all", "Slightly", "Moderately", "Very", "Extremely"],
    "clarity": ["Very Unclear", "Unclear", "Neutral", "Clear", "Very Clear"]
}

# Create a mapping to convert Likert strings to numeric
likert_mapping = {}
for metric, categories in metric_categories.items():
    likert_mapping[metric] = {cat: i+1 for i, cat in enumerate(categories)}

print("\\n=== Rating Differences: German vs Indian (Independent t-test) ===")
for metric, categories in metric_categories.items():
    for version in ['manual', 'ai']:
        col = f"{version}_{metric}"
        df_demog[f"{col}_num"] = df_demog[col].map(likert_mapping[metric])
        
        german_vals = df_demog[df_demog['nationality'] == 'German'][f"{col}_num"].dropna()
        indian_vals = df_demog[df_demog['nationality'] == 'Indian'][f"{col}_num"].dropna()
        
        if len(german_vals) > 1 and len(indian_vals) > 1:
            stat, p = stats.ttest_ind(german_vals, indian_vals, equal_var=False) # Welch's t-test
            sig = "*" if p < 0.05 else ""
            print(f"{col}: p-value = {p:.4f} {sig} | German mean={german_vals.mean():.2f}, Indian mean={indian_vals.mean():.2f}")

print("\\n=== Rating Differences: Across PoIs (One-way ANOVA) ===")
df_poi = survey_df_unique.copy()
for metric, categories in metric_categories.items():
    for version in ['manual', 'ai']:
        col = f"{version}_{metric}"
        df_poi[f"{col}_num"] = df_poi[col].map(likert_mapping[metric])
        
        groups = []
        for poi in df_poi['poi_title'].unique():
            vals = df_poi[df_poi['poi_title'] == poi][f"{col}_num"].dropna()
            if len(vals) > 1: # Need >1 for variance
                groups.append(vals)
        
        if len(groups) > 1:
            stat, p = stats.f_oneway(*groups)
            sig = "*" if p < 0.05 else ""
            print(f"{col}: p-value = {p:.4f} {sig}")
