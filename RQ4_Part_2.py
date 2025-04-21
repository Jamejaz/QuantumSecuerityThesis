import pandas as pd
import os

# 1. Load data
df = pd.read_csv('D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/q4_challenges_all_questions.csv')

# 2. Preprocessing
df['Challenge_Type'] = df['Primary_Challenge'].str.strip()
df['views'] = pd.to_numeric(df['views'], errors='coerce')
df['votes'] = pd.to_numeric(df['votes'], errors='coerce')
df['answers'] = pd.to_numeric(df['answers'], errors='coerce')

# Difficulty = (Views + Votes) / (Answers + 1)
df['difficulty_score'] = (df['views'] + df['votes']) / (df['answers'] + 1)

# 3. Output Path
output_path = 'D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/RQ4_outputs/top10_questions_with_bodies'
os.makedirs(output_path, exist_ok=True)

# 4. Extract Top-10 Questions per Challenge Type
top10_questions_per_challenge = {}

for challenge in df['Challenge_Type'].unique():
    top10 = df[df['Challenge_Type'] == challenge].sort_values(
        by=['views', 'votes'], ascending=[False, False]
    ).head(10)
    
    # Save only needed columns
    top10 = top10[['Challenge_Type', 'question_title', 'Question_body', 'views', 'votes', 'difficulty_score']]
    
    top10_questions_per_challenge[challenge] = top10

    # Save each separately
    top10.to_csv(os.path.join(output_path, f'top10_questions_{challenge.lower()}.csv'), index=False)

# 5. Combine all into one file (optional)
all_top10_questions = pd.concat(top10_questions_per_challenge.values(), keys=top10_questions_per_challenge.keys())

# Save combined file
all_top10_questions.to_csv(os.path.join(output_path, 'top10_questions_all_challenges.csv'))

print(f"✅ Top 10 questions per Challenge with full bodies saved inside: {output_path}")
