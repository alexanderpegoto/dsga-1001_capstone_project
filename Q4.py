import pandas as pd
from scipy.stats import ttest_ind


### load data

# File paths
file_paths = {
    "num": "rmpCapstoneNum.csv",
    "qual": "rmpCapstoneQual.csv",
    "tags": "rmpCapstoneTags.csv"
}

# Define column names
columns = {
    "num": [
        "Average Rating", "Average Difficulty", "Number of Ratings",
        "Received a 'pepper'?", "Proportion Would Retake",
        "Online Ratings Count", "Male", "Female"
    ],
    "qual": ["Major/Field", "University", "State"],
    "tags": [
        "Tough Grader", "Good Feedback", "Respected", "Lots to Read",
        "Participation Matters", "Don’t Skip Class", "Lots of Homework",
        "Inspirational", "Pop Quizzes", "Accessible", "So Many Papers",
        "Clear Grading", "Hilarious", "Test Heavy", "Graded by Few Things",
        "Amazing Lectures", "Caring", "Extra Credit", "Group Projects",
        "Lecture Heavy"
    ]
}

# Function to load data with specified column names
def load_data(file_path, col_names):
    return pd.read_csv(file_path, header=None, names=col_names)

# Load datasets
df_num = load_data(file_paths["num"], columns["num"])
df_qual = load_data(file_paths["qual"], columns["qual"])
df_tags = load_data(file_paths["tags"], columns["tags"])

# Display column names for verification
print("Numerical DataFrame Columns:", df_num.columns.tolist())
print("Qualitative DataFrame Columns:", df_qual.columns.tolist())
print("Tags DataFrame Columns:", df_tags.columns.tolist())

### Q4. Is there a gender difference in the tags awarded by students? Make sure
### to teach each of the 20 tags for a potential gender difference and report 
### which of them exhibit a statistically significant different. Comment on the 
### 3 most gendered (lowest p-value) and least gendered (highest p-value) tags.

# Normalize tag data by the number of ratings
df_tags_normalized = df_tags.div(df_num["Number of Ratings"], axis=0)

# Filter by gender
male_tags = df_tags_normalized[df_num["Male"] == 1]
female_tags = df_tags_normalized[df_num["Female"] == 1]

# Perform t-tests for gender differences in each tag (comparing the means of two independent groups)
p_values = {}
for tag in df_tags.columns:
    t_stat, p_val = ttest_ind(male_tags[tag], female_tags[tag], nan_policy='omit')
    p_values[tag] = p_val

# Convert p-values to DataFrame
p_values_df = pd.DataFrame(list(p_values.items()), columns=["Tag", "p-value"])
p_values_df.sort_values(by="p-value", inplace=True)

# Identify the most and least gendered tags
most_gendered = p_values_df.head(3)
least_gendered = p_values_df.tail(3)

# Filter for significant tags (p < 0.0005)
significant_tags = p_values_df[p_values_df["p-value"] < 0.0005]

# Results
print("Statistically Significant Tags (p < 0.0005):")
print(significant_tags)

print("\nMost Gendered Tags:")
print(most_gendered)

print("\nLeast Gendered Tags:")
print(least_gendered)

# Calculate the mean normalized tag frequency for each gender
male_tag_means = male_tags.mean()
female_tag_means = female_tags.mean()

# Identify the top 3 tags for each gender
top_male_tags = male_tag_means.sort_values(ascending=False).head(3)
print("top 3 tags that male proffessors received")
print(top_male_tags,"\n")

top_female_tags = female_tag_means.sort_values(ascending=False).head(3)
print("top 3 tags that female proffessors received")
print(top_female_tags,"\n")






