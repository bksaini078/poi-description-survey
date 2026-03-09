import pandas as pd
import numpy as np
import math

from utils import load_survey_responses
import config

print("Loading survey responses...")
survey_df = load_survey_responses('../survey_results/survey_response/', config.SURVEY_RESPONSES_PATTERN)
survey_df_unique = survey_df.drop_duplicates(subset=['user_id'], keep='last')

df_demog = survey_df_unique[survey_df_unique['nationality'].isin(['German', 'Indian'])].copy()

metric_categories = {
    "significance": ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
    "trust": ["Not at all", "Slightly", "Moderately", "Very", "Extremely"],
    "clarity": ["Very Unclear", "Unclear", "Neutral", "Clear", "Very Clear"]
}

likert_mapping = {}
for metric, categories in metric_categories.items():
    likert_mapping[metric] = {cat: i+1 for i, cat in enumerate(categories)}

print("\\n=== T-test Results: German vs Indian ===")
for metric, categories in metric_categories.items():
    for version in ['manual', 'ai']:
        col = f"{version}_{metric}"
        df_demog[f"{col}_num"] = df_demog[col].map(likert_mapping[metric])
        
        g_vals = df_demog[df_demog['nationality'] == 'German'][f"{col}_num"].dropna().values
        i_vals = df_demog[df_demog['nationality'] == 'Indian'][f"{col}_num"].dropna().values
        
        n1 = len(g_vals)
        n2 = len(i_vals)
        if n1 > 1 and n2 > 1:
            mean1 = np.mean(g_vals)
            mean2 = np.mean(i_vals)
            var1 = np.var(g_vals, ddof=1)
            var2 = np.var(i_vals, ddof=1)
            
            # Welch's t-test
            t_stat = (mean1 - mean2) / math.sqrt(var1/n1 + var2/n2)
            
            # Simple approximation of significance: df is roughly min(n1-1, n2-1) to (n1+n2-2)
            # t > 2 is roughly p < 0.05 for largeish n.
            sig = "*" if abs(t_stat) > 2.0 else ""
            
            print(f"{col}: t-stat={t_stat:.2f} {sig} | German mean={mean1:.2f} (n={n1}), Indian mean={mean2:.2f} (n={n2})")
