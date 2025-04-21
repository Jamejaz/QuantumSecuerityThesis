import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 1. Load the data
all_questions = pd.read_csv('D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/q3_algorithm_all_questions.csv')
summary = pd.read_csv('D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/q3_algorithm_summary.csv')

# 2. Normalize and clean algorithm names
all_questions['Mentions_Algorithm'] = all_questions['Mentions_Algorithm'].str.lower().str.strip()
summary['Algorithm'] = summary['Algorithm'].str.lower().str.strip()

# Replace common variants with canonical names
all_questions['Mentions_Algorithm'] = all_questions['Mentions_Algorithm'].replace({
    "shor's algorithm": 'shor',
    "shors": 'shor',
    "shor algorithm": 'shor',
    "grover's algorithm": 'grover',
    "grovers": 'grover',
    "rsa encryption": 'rsa',
    "quantum key distribution": 'qkd',
    "quantum fourier transform": 'qft',
    "post-quantum encryption": 'post-quantum signature',
    "post-quantum signatures": 'post-quantum signature'
    # Add more variants as needed
})

# 3. Define Classical vs Quantum Mapping (extended)
algorithm_type = {
    'shor': 'Quantum',
    'grover': 'Quantum',
    'bb84': 'Quantum',
    'rsa': 'Classical',
    'aes': 'Classical',
    'lattice': 'Classical',
    'ecc': 'Classical',
    'nist pqc': 'Classical',
    'qkd': 'Quantum',
    'simon': 'Quantum',
    'hhl': 'Quantum',
    'post-quantum signature': 'Classical',
    'b92': 'Quantum',
    'hash-based cryptography': 'Classical',
    'qft': 'Quantum',
    'vqe': 'Quantum',
    'qpe': 'Quantum',
    'qaoa': 'Quantum',
    'kyber': 'Classical',
    'rainbow': 'Classical'
}

# Assign type to summary
summary['type'] = summary['Algorithm'].map(algorithm_type)

# 4. Prepare Metrics
all_questions['views'] = pd.to_numeric(all_questions['views'], errors='coerce')
all_questions['votes'] = pd.to_numeric(all_questions['votes'], errors='coerce')
all_questions['answers'] = pd.to_numeric(all_questions['answers'], errors='coerce')
all_questions['difficulty_score'] = (all_questions['views'] + all_questions['votes']) / (all_questions['answers'] + 1)

# Group Metrics from full dataset
metrics = all_questions.groupby('Mentions_Algorithm').agg(
    total_questions=('question_title', 'count'),
    average_views=('views', 'mean'),
    average_votes=('votes', 'mean'),
    average_difficulty=('difficulty_score', 'mean')
).reset_index()

# Merge with summary
final_table = summary.merge(metrics, left_on='Algorithm', right_on='Mentions_Algorithm', how='left')

# 5. Output Path
output_path = 'D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/RQ3_outputs'
os.makedirs(output_path, exist_ok=True)

# Save Final Table
final_table.to_csv(os.path.join(output_path, 'rq3_algorithms_metrics_full.csv'), index=False)

# 6. Top-10 Algorithms by Question Count
top10_algorithms = final_table.sort_values('total_questions', ascending=False).head(10)

# Bar Chart – Total Questions
plt.figure(figsize=(12, 6))
plt.bar(top10_algorithms['Algorithm'], top10_algorithms['total_questions'], width=0.4, color='skyblue')
plt.title('Number of Questions for Top-10 Algorithms')
plt.ylabel('Total Questions')
plt.xlabel('Algorithms')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'Top10_algorithms_total_questions.png'))
plt.show()

# Bar Chart – Difficulty Score
top10_difficulty = final_table.sort_values('average_difficulty', ascending=False).head(10)
plt.figure(figsize=(12, 6))
plt.bar(top10_difficulty['Algorithm'], top10_difficulty['average_difficulty'], width=0.4, color='salmon')
plt.title('Average Difficulty Score for Top-10 Algorithms')
plt.ylabel('Average Difficulty Score')
plt.xlabel('Algorithms')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'Top10_algorithms_difficulty_score_only.png'))
plt.show()

# 7. Trend Chart – 2017 Onward
top5_algorithms_list = final_table.sort_values('total_questions', ascending=False).head(5)['Algorithm'].tolist()
trend_df = all_questions[all_questions['Mentions_Algorithm'].isin(top5_algorithms_list)].copy()

# Add BiAnnual time index
trend_df['date'] = pd.to_datetime(trend_df['date'], errors='coerce')
trend_df['BiAnnual'] = trend_df['date'].dt.year.astype(str) + "-H" + (trend_df['date'].dt.month // 7 + 1).astype(str)
trend_df = trend_df[trend_df['date'].dt.year >= 2017]

# Build trend table
trend_top5 = trend_df.groupby(['BiAnnual', 'Mentions_Algorithm']).size().unstack(fill_value=0)
years = list(range(2017, 2026))
biannual_periods = [f"{year}-H1" for year in years] + [f"{year}-H2" for year in years]
biannual_periods = sorted(biannual_periods)
trend_top5 = trend_top5.reindex(biannual_periods, fill_value=0)

# Plot Trend Line
plt.figure(figsize=(16, 8))
trend_top5.plot(marker='o')
plt.title('Trend of Number of Questions for Top-5 Algorithms (2017–2025)')
plt.ylabel('Number of Questions')
plt.xlabel('Period (Year-Half)')
plt.xticks(ticks=np.arange(len(biannual_periods)), labels=biannual_periods, rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'Top5_algorithms_trend_biannual_questions_2017onwards.png'))
plt.show()

print(f"\n✅ FINAL Cleaned RQ3 Analysis Completed. All outputs saved at:\n{output_path}\n")

