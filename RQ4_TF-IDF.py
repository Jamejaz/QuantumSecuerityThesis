import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import re

# Load data
df = pd.read_csv('D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/q4_challenges_all_questions.csv')

# Clean challenge type and Question_body
df['Challenge_Type'] = df['Primary_Challenge'].str.strip().str.title()
df = df[df['Challenge_Type'].notna() & (df['Challenge_Type'] != '')]
df['Question_body'] = df['Question_body'].fillna('').astype(str)

# Combine all Question_body texts by Challenge_Type
grouped = df.groupby('Challenge_Type')['Question_body'].apply(lambda texts: ' '.join(texts)).reset_index()

# TF-IDF setup
vectorizer = TfidfVectorizer(
    max_df=0.85,
    min_df=2,
    stop_words='english',
    max_features=1000
)

# Apply TF-IDF
tfidf_matrix = vectorizer.fit_transform(grouped['Question_body'])
feature_names = vectorizer.get_feature_names_out()

# Build results
results = []
for i, challenge in enumerate(grouped['Challenge_Type']):
    row = tfidf_matrix[i].tocoo()
    for idx, val in zip(row.col, row.data):
        results.append({
            'Challenge_Type': challenge,
            'Keyword': feature_names[idx],
            'TFIDF_Score': round(val, 4)
        })

# Convert to DataFrame
tfidf_df = pd.DataFrame(results)

# Get top 30 keywords per category
top_keywords = tfidf_df.sort_values(by='TFIDF_Score', ascending=False).groupby('Challenge_Type').head(30)

# Save CSV
output_path = 'D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/RQ4_outputs'
os.makedirs(output_path, exist_ok=True)
top_keywords.to_csv(os.path.join(output_path, 'tfidf_keywords_per_challenge.csv'), index=False)

# Generate WordCloud for each Challenge Type
print("🎯 Generating TF-IDF word clouds...")
for challenge in top_keywords['Challenge_Type'].unique():
    challenge_data = top_keywords[top_keywords['Challenge_Type'] == challenge]
    word_freq = dict(zip(challenge_data['Keyword'], challenge_data['TFIDF_Score']))
    
    wordcloud = WordCloud(width=1000, height=500, background_color='white').generate_from_frequencies(word_freq)
    
    plt.figure(figsize=(12,6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'TF-IDF Word Cloud – {challenge} Challenges', fontsize=16)
    plt.tight_layout()
    
    filename = f'tfidf_wordcloud_{challenge.lower().replace(" ", "_")}.png'
    plt.savefig(os.path.join(output_path, filename))
    plt.close()

print("✅ TF-IDF CSV and word clouds saved to:", output_path)

