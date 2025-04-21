import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 1. Load the data
df = pd.read_csv('D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/q1_tools_all_questions.csv')

# 2. Preprocess
df['Mentions_Tool'] = df['Mentions_Tool'].str.lower().str.split(',')
df_exploded = df.explode('Mentions_Tool')
df_exploded['Mentions_Tool'] = df_exploded['Mentions_Tool'].str.strip()

# Convert views, votes, answers to numeric
df_exploded['views'] = pd.to_numeric(df_exploded['views'], errors='coerce')
df_exploded['votes'] = pd.to_numeric(df_exploded['votes'], errors='coerce')
df_exploded['answers'] = pd.to_numeric(df_exploded['answers'], errors='coerce')

# 3. Define tools list
tools_list = [
    'qiskit', 'stim', 'cirq', 'openqasm', 'qutip', 'braket',
    'simulaqron', 'projectq', 'oqs', 'kyber', 'dilithium', 'rainbow', 'ntru'
]

# 4. Output Path
output_path = 'D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/Q1_outputs'
os.makedirs(output_path, exist_ok=True)

# 5. Filter only selected tools
filtered_df = df_exploded[df_exploded['Mentions_Tool'].isin(tools_list)]

# 6. Calculate Metrics
metrics_table = filtered_df.groupby('Mentions_Tool').agg(
    Total_Questions=('question_title', 'count'),
    Average_Views=('views', 'mean'),
    Average_Votes=('votes', 'mean')
).reset_index()

metrics_table = metrics_table.sort_values(by='Total_Questions', ascending=False)

# 7. Top-10 Tools for Bar Charts
top10_tools = metrics_table.head(10)['Mentions_Tool'].tolist()
top10_df = filtered_df[filtered_df['Mentions_Tool'].isin(top10_tools)]

# 8. Top-5 Tools for Trend Line Chart
top5_tools = metrics_table.head(5)['Mentions_Tool'].tolist()
top5_df = filtered_df[filtered_df['Mentions_Tool'].isin(top5_tools)]

# 9. Difficulty Score Calculation
top10_df['Difficulty_Score'] = (top10_df['views'] + top10_df['votes']) / (top10_df['answers'] + 1)

difficulty_table = top10_df.groupby('Mentions_Tool').agg(
    Average_Difficulty=('Difficulty_Score', 'mean')
).reset_index()

difficulty_table = difficulty_table.sort_values(by='Average_Difficulty', ascending=False)

# Save Difficulty Table
difficulty_table.to_csv(os.path.join(output_path, 'top10_tools_difficulty_summary.csv'), index=False)

# 10. Plot Difficulty Bar Chart (Top-10 Tools)
plt.figure(figsize=(12, 6))
plt.bar(difficulty_table['Mentions_Tool'], difficulty_table['Average_Difficulty'], width=0.4, color='salmon')
plt.title('Average Difficulty Score for Top-10 Tools/Frameworks')
plt.ylabel('Average Difficulty Score')
plt.xlabel('Tools/Frameworks')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'Top10_tools_difficulty_score_only.png'))
plt.show()

# 11. Plot Number of Questions Bar Chart (Top-10 Tools)
questions_table = top10_df.groupby('Mentions_Tool').agg(
    Total_Questions=('question_title', 'count')
).reset_index()

plt.figure(figsize=(12, 6))
plt.bar(questions_table['Mentions_Tool'], questions_table['Total_Questions'], width=0.4, color='skyblue')
plt.title('Number of Questions for Top-10 Tools/Frameworks')
plt.ylabel('Total Questions')
plt.xlabel('Tools/Frameworks')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'Top10_tools_total_questions.png'))
plt.show()

# 12. Plot Trend Chart for Top-5 Tools (Questions over Bi-Annual Periods)
top5_df['date'] = pd.to_datetime(top5_df['date'], errors='coerce')
top5_df['BiAnnual'] = top5_df['date'].dt.year.astype(str) + "-H" + (top5_df['date'].dt.month // 7 + 1).astype(str)

# Create complete periods from 2017 to 2025
years = list(range(2017, 2026))
biannual_periods = [f"{year}-H1" for year in years] + [f"{year}-H2" for year in years]
biannual_periods = sorted(biannual_periods)

trend_top5_biannual = top5_df.groupby(['BiAnnual', 'Mentions_Tool']).size().unstack(fill_value=0)
trend_top5_biannual = trend_top5_biannual.reindex(biannual_periods, fill_value=0)

# Plot Trend Chart
plt.figure(figsize=(16, 8))
trend_top5_biannual.plot(marker='o')
plt.title('Trend of Top-5 Tools/Frameworks')
plt.ylabel('Number of Questions')
plt.xlabel('Time Period')
plt.xticks(ticks=np.arange(len(biannual_periods)), labels=biannual_periods, rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'Top5_tools_framework_trend_biannual_questions_2017onwards.png'))
plt.show()

print(f"\n✅ FINAL Cleaned Q1 Analysis Completed. All outputs saved at:\n{output_path}\n")





