import json

notebook_path = "data_analysis.ipynb"
with open(notebook_path, "r") as f:
    nb = json.load(f)

# Markdown cell for Section 1
cell_md_1 = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 1. Statistical Tests: German vs Indian Participants\\n",
        "\\n",
        "Here we aim to test if there are significant demographic differences (specifically between German and Indian participants) in terms of their preferences and Likert scale ratings.\\n",
        "We'll use **Chi-Square** tests for categorical preferences and **Mann-Whitney U** tests for ordinal evaluations."
    ]
}

# Code cell for section 1setup and Chi-Square
code_section_1a = """import scipy.stats as stats
import pandas as pd
import numpy as np

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
"""
cell_code_1a = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + "\\n" for line in code_section_1a.split("\\n")][:-1] # removing last empty line add
}

# Code cell for Mann-Whitney U
code_section_1b = """# 2. Likert Ratings across Demographics (Independent t-test)
metric_categories = {
    "significance": ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
    "trust": ["Not at all", "Slightly", "Moderately", "Very", "Extremely"],
    "clarity": ["Very Unclear", "Unclear", "Neutral", "Clear", "Very Clear"]
}

# Create a mapping to convert Likert strings to numeric
likert_mapping = {}
for metric, categories in metric_categories.items():
    likert_mapping[metric] = {cat: i+1 for i, cat in enumerate(categories)}

print("=== Rating Differences: German vs Indian (Independent t-test) ===")
for metric, categories in metric_categories.items():
    for version in ['manual', 'ai']:
        col = f"{version}_{metric}"
        # Map values to numeric
        numeric_series = df_demog[col].map(likert_mapping[metric])
        df_demog[f"{col}_num"] = numeric_series
        
        # Split into groups
        german_vals = df_demog[df_demog['nationality'] == 'German'][f"{col}_num"].dropna()
        indian_vals = df_demog[df_demog['nationality'] == 'Indian'][f"{col}_num"].dropna()
        
        if len(german_vals) > 1 and len(indian_vals) > 1:
            stat, p = stats.ttest_ind(german_vals, indian_vals, equal_var=False)
            sig = "*" if p < 0.05 else ""
            print(f"{col}: t-stat={stat:.4f}, p-value={p:.4f} {sig} (German mean={german_vals.mean():.2f}, Indian mean={indian_vals.mean():.2f})")
        else:
            print(f"{col}: Not enough data")
print("\\n* p < 0.05 indicates a significant difference in mean ratings.\\n")
"""
cell_code_1b = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + "\\n" for line in code_section_1b.split("\\n")][:-1]
}

# Markdown cell for Section 2
cell_md_2 = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 2. Statistical Tests: Differences across Points of Interest (PoI)\\n",
        "\\n",
        "We will test if the specific Point of Interest (PoI) significantly influenced participant responses using **Chi-Square** (for preferences) and **Kruskal-Wallis** (for ordinal evaluations)."
    ]
}

# Code cell for section 2
code_section_2 = """print("=== Preference Differences: Across PoIs (Chi-Square Test) ===")
# We use the full unique dataset for this
df_poi = survey_df_unique.copy()

for col in preference_cols:
    contingency = pd.crosstab(df_poi['poi_title'], df_poi[col])
    contingency = contingency.loc[:, (contingency != 0).any(axis=0)]
    
    if contingency.size > 0 and contingency.shape[0] > 1 and contingency.shape[1] > 1:
        chi2, p, dof, expected = stats.chi2_contingency(contingency.values)
        sig = "*" if p < 0.05 else ""
        print(f"{col}: p-value={p:.4f} {sig}")
    else:
        print(f"{col}: Not enough variation for Chi-Square")
print("\\n* p < 0.05 indicates the preference distribution significantly depends on the PoI.\\n")


print("=== Rating Differences: Across PoIs (One-way ANOVA) ===")
for metric, categories in metric_categories.items():
    for version in ['manual', 'ai']:
        col = f"{version}_{metric}"
        df_poi[f"{col}_num"] = df_poi[col].map(likert_mapping[metric])
        
        # Collect groups
        groups = []
        for poi in df_poi['poi_title'].unique():
            vals = df_poi[df_poi['poi_title'] == poi][f"{col}_num"].dropna()
            if len(vals) > 1:
                groups.append(vals)
        
        if len(groups) > 1:
            stat, p = stats.f_oneway(*groups)
            sig = "*" if p < 0.05 else ""
            print(f"{col}: F-stat={stat:.4f}, p-value={p:.4f} {sig}")
        else:
            print(f"{col}: Not enough groups")
print("\\n* p < 0.05 indicates mean ranks differ significantly across PoIs.\\n")
"""
cell_code_2 = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + "\\n" for line in code_section_2.split("\\n")][:-1]
}

nb["cells"] = nb["cells"][:32]
nb["cells"].extend([cell_md_1, cell_code_1a, cell_code_1b, cell_md_2, cell_code_2])

with open(notebook_path, "w") as f:
    json.dump(nb, f, indent=1)

print("Notebook updated using json successfully.")
