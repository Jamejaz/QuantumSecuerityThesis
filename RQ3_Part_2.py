import pandas as pd
import os

# 1. Load cleaned data
all_questions = pd.read_csv("D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/q3_algorithm_all_questions.csv")

# 2. Normalize column
all_questions['Mentions_Algorithm'] = all_questions['Mentions_Algorithm'].str.lower().str.strip()

# 3. Filter to only final 13 algorithms
algorithms_of_interest = ['shor', 'grover', 'qft', 'rsa', 'qkd', 'vqe', 'qpe', 'ecc', 'qaoa', 'hhl', 'kyber', 'rainbow', 'ntru']
df_filtered = all_questions[all_questions['Mentions_Algorithm'].isin(algorithms_of_interest)].copy()

# 4. Clean numeric columns
df_filtered['views'] = pd.to_numeric(df_filtered['views'], errors='coerce')
df_filtered['votes'] = pd.to_numeric(df_filtered['votes'], errors='coerce')
df_filtered['answers'] = pd.to_numeric(df_filtered['answers'], errors='coerce')

# 5. Difficulty score formula
df_filtered['difficulty_score'] = (df_filtered['views'] + df_filtered['votes']) / (df_filtered['answers'] + 1)

# 6. Group and summarize
summary = df_filtered.groupby('Mentions_Algorithm').agg(
    Total_Questions=('question_title', 'count'),
    Average_Views=('views', 'mean'),
    Average_Votes=('votes', 'mean'),
    Average_Difficulty=('difficulty_score', 'mean')
).reset_index()

# 7. Set output path
output_path = "D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/RQ3_outputs"
os.makedirs(output_path, exist_ok=True)

# 8. Save CSV
summary.to_csv(f"{output_path}/RQ3_algorithm_final_metrics_filtered.csv", index=False)

# 9. Done
print("✅ Metrics table saved to:", f"{output_path}/RQ3_algorithm_final_metrics_filtered.csv")
