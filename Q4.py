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

print("H0 (Null Hypothesis): There a gender difference in the tags awarded by students.")
print("H1: There is a no gender difference in the tags awarded by students.")

### Q4. Is there a gender difference in the tags awarded by students? Make sure 
### to teach each of the 20 tags for a potential gender difference and report 
### which of them exhibit a statistically significant different. Comment on the
### 3 most gendered (lowest p-value) and least gendered (highest p-value) tags.


