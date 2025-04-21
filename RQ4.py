import pandas as pd
import matplotlib.pyplot as plt
import os

# Load preprocessed data
df = pd.read_csv('D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/q4_challenges_all_questions.csv')
df['Challenge_Type'] = df['Primary_Challenge'].str.strip().str.title()
df = df[df['Challenge_Type'].notna() & (df['Challenge_Type'] != '')]
df['views'] = pd.to_numeric(df['views'], errors='coerce')
df['votes'] = pd.to_numeric(df['votes'], errors='coerce')
df['answers'] = pd.to_numeric(df['answers'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['difficulty_score'] = (df['views'] + df['votes']) / (df['answers'] + 1)

output_path = 'D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/RQ4_outputs'

# ✅ PIE CHART
challenge_counts = df['Challenge_Type'].value_counts()
plt.figure(figsize=(9, 9))
labels = [f'{label} ({count})' for label, count in zip(challenge_counts.index, challenge_counts.values)]
plt.pie(challenge_counts.values, labels=labels, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 10})
plt.title('Distribution of Questions by Challenge Type', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'pie_chart_challenge_distribution.png'))
plt.show()

# 📈 TREND CHART
df['BiAnnual'] = df['date'].dt.year.astype(str) + "-H" + (df['date'].dt.month // 7 + 1).astype(str)
trend_df = df.groupby(['BiAnnual', 'Challenge_Type']).size().unstack(fill_value=0)
trend_df = trend_df.loc[trend_df.index >= '2017-H1']
trend_df.index = pd.CategoricalIndex(trend_df.index, ordered=True)
trend_df = trend_df.sort_index()

plt.figure(figsize=(14,7))
trend_df.plot(marker='o')
plt.title('Challenges Trend')
plt.ylabel('Number of Mentions')
plt.xlabel('Time Period')
plt.xticks(rotation=45)
plt.legend(title='Challenge Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'trend_challenges_over_time_biannual_fixed.png'))
plt.show()

# 📊 BAR CHARTS: Avg Views, Votes, Difficulty
challenge_metrics = df.groupby('Challenge_Type').agg(
    avg_views=('views', 'mean'),
    avg_votes=('votes', 'mean'),
    avg_difficulty=('difficulty_score', 'mean')
).reset_index()

# Avg Views
plt.figure(figsize=(10,6))
plt.bar(challenge_metrics['Challenge_Type'], challenge_metrics['avg_views'], width=0.5, color='orange')
plt.title('Average Views per Challenge')
plt.ylabel('Average Views')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'avg_views_challenges.png'))
plt.show()

# Avg Votes
plt.figure(figsize=(10,6))
plt.bar(challenge_metrics['Challenge_Type'], challenge_metrics['avg_votes'], width=0.5, color='green')
plt.title('Average Votes per Challenge')
plt.ylabel('Average Votes')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'avg_votes_challenges.png'))
plt.show()

# Avg Difficulty
plt.figure(figsize=(10,6))
plt.bar(challenge_metrics['Challenge_Type'], challenge_metrics['avg_difficulty'], width=0.5, color='red')
plt.title('Average Difficulty Score per Challenge')
plt.ylabel('Average Difficulty Score')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_path, 'avg_difficulty_challenges.png'))
plt.show()

# Save Summary Table
challenge_metrics.to_csv(os.path.join(output_path, 'RQ4_challenges_summary.csv'), index=False)

print("📈 All charts generated and saved to:", output_path)



