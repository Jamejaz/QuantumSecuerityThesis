import pandas as pd
import numpy as np
import os

# 📌 File Paths
input_file = "D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/question_topic.csv"
output_dir = "D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend"
os.makedirs(output_dir, exist_ok=True)

# ✅ Load Data
df = pd.read_csv(input_file)

# ✅ Convert '1k' notation to numeric values
def convert_k_to_number(value):
    if isinstance(value, str):
        value = value.lower().replace(',', '')  # Remove commas (e.g., '1,500' → '1500')
        if 'k' in value:
            return float(value.replace('k', '')) * 1000  # Convert '1k' → 1000
        if 'm' in value:
            return float(value.replace('m', '')) * 1000000  # Convert '1m' → 1000000
    try:
        return float(value)  # Convert normal numbers
    except ValueError:
        return np.nan  # Handle invalid cases

# ✅ Apply conversion
df['answers'] = df['answers'].apply(convert_k_to_number)
df['votes'] = df['votes'].apply(convert_k_to_number)
df['views'] = df['views'].apply(convert_k_to_number)

# ✅ Drop missing values
df = df[['Question','question_title', 'Question_body', 'Topic', 'answers', 'votes', 'views', 'url', 'Dominant_Keywords']].dropna()

# 📌 **1️⃣ Top 5 Most Viewed Questions Per Topic**
top_viewed = df.sort_values(by=['Topic', 'views'], ascending=[True, False])
top_viewed_per_topic = top_viewed.groupby('Topic').head(5)
top_viewed_per_topic['Score'] = top_viewed_per_topic['views']  # Score is based on views

# ✅ Save CSV
csv_views = f"{output_dir}/top_5_most_viewed.csv"
top_viewed_per_topic[['Topic', 'Dominant_Keywords', 'Question', 'question_title', 'Question_body', 'Score', 'url']].to_csv(csv_views, index=False)
print(f"✅ CSV Saved: {csv_views}")

# 📌 **2️⃣ Top 5 Most Voted Questions Per Topic**
top_voted = df.sort_values(by=['Topic', 'votes'], ascending=[True, False])
top_voted_per_topic = top_voted.groupby('Topic').head(5)
top_voted_per_topic['Score'] = top_voted_per_topic['votes']  # Score is based on votes

# ✅ Save CSV
csv_votes = f"{output_dir}/top_5_most_voted.csv"
top_voted_per_topic[['Topic', 'Dominant_Keywords', 'Question', 'question_title', 'Question_body', 'Score', 'url']].to_csv(csv_votes, index=False)
print(f"✅ CSV Saved: {csv_votes}")

# 📌 **3️⃣ Top 5 Most Difficult Questions Per Topic (High Views & Votes, Low Answers)**
df['difficulty_score'] = (df['views'] + df['votes']) / (df['answers'] + 1)  # Avoid division by zero
top_difficult = df.sort_values(by=['Topic', 'difficulty_score'], ascending=[True, False])
top_difficult_per_topic = top_difficult.groupby('Topic').head(5)
top_difficult_per_topic['Score'] = top_difficult_per_topic['difficulty_score']  # Score is difficulty metric

# ✅ Save CSV
csv_difficult = f"{output_dir}/top_5_most_difficult.csv"
top_difficult_per_topic[['Topic', 'Dominant_Keywords', 'Question', 'question_title', 'Question_body', 'Score', 'url']].to_csv(csv_difficult, index=False)
print(f"✅ CSV Saved: {csv_difficult}")
