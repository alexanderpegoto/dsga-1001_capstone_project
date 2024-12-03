import sqlite3
import pandas as pd
import re
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import numpy as np


# General info, Define  column names
column_names = ["Average Rating", 
                "Average Difficulty", 
                "Number of ratings",
                "Received a 'pepper'?",
                "The proportion of students that said they would take the class again",
                "The number of ratings coming from online classes",
                "Male",
                "Female"]
df_num = pd.read_csv("rmpCapstoneNum.csv", header=None, names=column_names)
print(df_num.columns)

# Major|University|States, define column names
column_names2 = ["Major/Field", "University", "US State (2 letter abbreviation)" ]
df_qual = pd.read_csv("rmpCapstoneQual.csv", header=None, names=column_names2)
print(df_qual.columns)

# 3 Tags, define column names
column_names3 = ["Tough grader", 
                 "Good feedback", 
                 "Respected", 
                 "Lots to read", 
                 "Participation matters", 
                 "Don’t skip class or you will not pass", 
                 "Lots of homework", 
                 "Inspirational", 
                 "Pop quizzes!", 
                 "Accessible", 
                 "So many papers", 
                 "Clear grading", 
                 "Hilarious",
                 "Test heavy", 
                 "Graded by few things", 
                 "Amazing lectures", 
                 "Caring", 
                 "Extra credit", 
                 "Group projects", 
                 "Lecture heavy"]
df_tags = pd.read_csv("rmpCapstoneTags.csv", header=None, names=column_names3)
print(df_tags.columns)


## Q2. Is there a gender difference in the spread (variance/dispersion) 
## of the ratings distribution? Again, it is advisable to consider 
## the statistical significance of any observed gender differences 
## in this spread.

print("H0 (Null Hypothesis): There is a gender difference in the spread of the ratings distribution.")
print("H1: There is a no gender difference in the spread of the ratings distribution.")

# Set a threshold for the minimum number of ratings
k = 5.37  # This df_num["Number of ratings"].mean()

# Step 1: Apply the threshold
filtered_data = df_num[df_num["Number of ratings"] >= k]

# Step 2: Drop rows with missing average ratings
filtered_data = filtered_data.dropna(subset=["Average Rating"])

# Step 3: Separate ratings by gender
male_ratings = filtered_data[filtered_data["Male"] == 1]["Average Rating"]
female_ratings = filtered_data[filtered_data["Female"] == 1]["Average Rating"]

# Step 4: Calculate variances for each gender
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


