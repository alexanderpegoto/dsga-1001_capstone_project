import sqlite3
import pandas as pd
import re
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import numpy as np

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




## Q2. Is there a gender difference in the spread (variance/dispersion) 
## of the ratings distribution? Again, it is advisable to consider 
## the statistical significance of any observed gender differences 
## in this spread.

print("H0 (Null Hypothesis): There is a gender difference in the spread of the ratings distribution.")
print("H1: There is a no gender difference in the spread of the ratings distribution.")

# Set a threshold for the minimum number of ratings
k = 5.37  # This df_num["Number of ratings"].mean()

# Threshold
filtered_data = df_num[df_num["Number of Ratings"] >= k]

# Drop rows with missing average ratings
filtered_data = filtered_data.dropna(subset=["Average Rating"])

# Separate ratings by gender
male_ratings = filtered_data[filtered_data["Male"] == 1]["Average Rating"]
female_ratings = filtered_data[filtered_data["Female"] == 1]["Average Rating"]

# Calculate variances for each gender
male_variance = np.var(male_ratings, ddof=1)  # Sample variance
female_variance = np.var(female_ratings, ddof=1)

# Output results
print(f"Male Variance: {male_variance}")
print(f"Female Variance: {female_variance}")

## KS Test for Distribution (sensitive to differences in shape, spread, and median).

from scipy.stats import ks_2samp

# Perform the KS test
ks_stat, p_value = ks_2samp(male_ratings, female_ratings)

# Output results
print(f"KS Statistic: {ks_stat}")
print(f"p-value: {p_value}")

# Interpret the results
if p_value < 0.005:
    print("We are dropping the assumed null hypothesis, H1 is true. There is a significant difference in the spread of ratings between male and female professors.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference in the spread of ratings between male and female professors.")

########################
### Chi-sqaure Test for Variance comparison

#from scipy.stats import chi2

# Variance and sample sizes
#male_variance = np.var(male_ratings, ddof=1)  
#female_variance = np.var(female_ratings, ddof=1)
#male_n = len(male_ratings)
#female_n = len(female_ratings)

# Chi-Square statistic
#chi2_stat = (male_n - 1) * male_variance / female_variance

# Degrees of freedom
#df_male = male_n - 1
#df_female = female_n - 1

# p-value from chi-square distribution
#p_value = 1 - chi2.cdf(chi2_stat, df=df_male)

#print(f"Chi-Square Statistic: {chi2_stat}")
#print(f"p-value: {p_value}")

# Interpret the results
#if p_value < 0.005:
#    print("We are dropping the assumed null hypothesis, H1 is true. There is a significant difference in the spread of ratings between male and female professors.")
#else:
#    print("Fail to reject the null hypothesis. There is no significant difference in the spread of ratings between male and female professors.")
#####################

### MW U test distribution (median-based comparison).
from scipy.stats import mannwhitneyu

# Perform Mann-Whitney U Test
u_stat, p_value = mannwhitneyu(male_ratings, female_ratings, alternative="two-sided")

# Output results
print(f"Mann-Whitney U Statistic: {u_stat}")
print(f"p-value: {p_value}")

# Interpret the results
if p_value < 0.005:
    print("We are dropping the assumed null hypothesis, H1 is true. There is a significant difference in the spread of ratings between male and female professors.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference in the spread of ratings between male and female professors.")


# Histograms
plt.hist(male_ratings, bins=30, alpha=0.5, label='Male Ratings', density=True)
plt.hist(female_ratings, bins=30, alpha=0.5, label='Female Ratings', density=True)
plt.legend()
plt.title("Histogram of Ratings by Gender")
plt.xlabel("Rating")
plt.ylabel("Density")
plt.show()

# CDFs
male_cdf = np.sort(male_ratings)
female_cdf = np.sort(female_ratings)
plt.step(male_cdf, np.arange(1, len(male_cdf) + 1) / len(male_cdf), label="Male CDF")
plt.step(female_cdf, np.arange(1, len(female_cdf) + 1) / len(female_cdf), label="Female CDF")
plt.legend()
plt.title("Cumulative Distribution Functions of Ratings")
plt.xlabel("Rating")
plt.ylabel("CDF")
plt.show()


