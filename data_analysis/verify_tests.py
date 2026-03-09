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

# 1. Preferences across Demographics (Chi-Square)
preference_cols = ['engaging_preference', 'relevant_preference', 'eager_preference', 'title_preference', 'description_preference']

print("=== Preference Differences: German vs Indian (Chi-Square Test) ===")
for col in preference_cols:
    contingency = pd.crosstab(df_demog['nationality'], df_demog[col])
    contingency = contingency.loc[:, (contingency != 0).any(axis=0)]
    
    if contingency.size > 0 and contingency.shape[0] > 1 and contingency.shape[1] > 1:
        chi2, p, dof, expected = stats.chi2_contingency(contingency.values)
        sig = "*" if p < 0.05 else ""
        print(f"{col}: p-value = {p:.4f} {sig}")
    else:
        print(f"{col}: Not enough variation for Chi-Square")
print("\\n* p < 0.05 indicates a significant difference in preference distribution.\\n")

# 2. Likert Ratings across Demographics (Mann-Whitney U test)
metric_categories = {
    "significance": ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
    "trust": ["Not at all", "Slightly", "Moderately", "Very", "Extremely"],
    "clarity": ["Very Unclear", "Unclear", "Neutral", "Clear", "Very Clear"]
}

# Create a mapping to convert Likert strings to numeric
likert_mapping = {}
for metric, categories in metric_categories.items():
    likert_mapping[metric] = {cat: i+1 for i, cat in enumerate(categories)}

print("=== Rating Differences: German vs Indian (Mann-Whitney U Test) ===")
for metric, categories in metric_categories.items():
    for version in ['manual', 'ai']:
        col = f"{version}_{metric}"
        # Map values to numeric
        numeric_series = df_demog[col].map(likert_mapping[metric])
        df_demog[f"{col}_num"] = numeric_series
        
        # Split into groups
        german_vals = df_demog[df_demog['nationality'] == 'German'][f"{col}_num"].dropna()
        indian_vals = df_demog[df_demog['nationality'] == 'Indian'][f"{col}_num"].dropna()
        
        if len(german_vals) > 0 and len(indian_vals) > 0:
            stat, p = stats.mannwhitneyu(german_vals, indian_vals, alternative='two-sided')
            sig = "*" if p < 0.05 else ""
            print(f"{col}: p-value = {p:.4f} {sig} (German median={german_vals.median()}, Indian median={indian_vals.median()})")
        else:
            print(f"{col}: Not enough data")
print("\\n* p < 0.05 indicates a significant difference in ordinal rankings.\\n")

print("=== Preference Differences: Across PoIs (Chi-Square Test) ===")
# We use the full unique dataset for this
df_poi = survey_df_unique.copy()

for col in preference_cols:
    contingency = pd.crosstab(df_poi['poi_title'], df_poi[col])
    contingency = contingency.loc[:, (contingency != 0).any(axis=0)]
    
    if contingency.size > 0 and contingency.shape[0] > 1 and contingency.shape[1] > 1:
        chi2, p, dof, expected = stats.chi2_contingency(contingency.values)
        sig = "*" if p < 0.05 else ""
        print(f"{col}: p-value = {p:.4f} {sig}")
    else:
        print(f"{col}: Not enough variation for Chi-Square")
print("\\n* p < 0.05 indicates the preference distribution significantly depends on the PoI.\\n")

print("=== Rating Differences: Across PoIs (Kruskal-Wallis H Test) ===")
for metric, categories in metric_categories.items():
    for version in ['manual', 'ai']:
        col = f"{version}_{metric}"
        df_poi[f"{col}_num"] = df_poi[col].map(likert_mapping[metric])
        
        # Collect groups
        groups = []
        for poi in df_poi['poi_title'].unique():
            vals = df_poi[df_poi['poi_title'] == poi][f"{col}_num"].dropna()
            if len(vals) > 0:
                groups.append(vals)
        
        if len(groups) > 1:
            stat, p = stats.kruskal(*groups)
            sig = "*" if p < 0.05 else ""
            print(f"{col}: p-value = {p:.4f} {sig}")
        else:
            print(f"{col}: Not enough groups")
print("\\n* p < 0.05 indicates median ranks differ significantly across PoIs.\\n")
