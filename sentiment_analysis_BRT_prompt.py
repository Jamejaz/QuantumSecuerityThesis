import pandas as pd
import torch
import re
from transformers import pipeline, AutoTokenizer
from tqdm import tqdm

# ✅ Define Input & Output CSV Paths
input_csv = "D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5/11topics/question_topic.csv"
output_csv = "D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5/11topics/sentiment_question_topic.csv"

# ✅ Load data with error handling
try:
    df = pd.read_csv(input_csv)
except Exception as e:
    raise ValueError(f"❌ Error loading CSV file: {e}")

# ✅ Ensure required columns exist
required_columns = ["question_title", "Question_body"]
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"❌ The CSV file must contain a '{col}' column.")

# ✅ Initialize zero-shot classification pipeline using DeBERTa
classifier = pipeline("zero-shot-classification", model="microsoft/deberta-v3-base")

# ✅ Define Custom Sentiment Categories for Q&A
labels = [
    "Confidence (Positive)",
    "Frustration (Negative)",
    "Doubt (Uncertainty)",
    "Confusion (Struggling)",
    "Curiosity (Exploratory)",
    "Skepticism (Critical Thinking)",
    "Agreement (Supportive)",
    "Disagreement (Opposition)",
    "Neutral (Informative)"
]

# ✅ Combine question title and body for better classification
df["Full_Text"] = df["question_title"].astype(str) + " " + df["Question_body"].astype(str)

# ✅ Function to clean text (remove special characters, links, etc.)
def clean_text(text):
    if pd.isna(text) or not isinstance(text, str):
        return ""
    text = re.sub(r"\[.*?\]|\(.*?\)|\{.*?\}", "", text)  # Remove brackets
    text = re.sub(r"http\S+|www\S+", "", text)  # Remove links
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove special characters
    return text.lower().strip()

df["Full_Text"] = df["Full_Text"].apply(clean_text)

# ✅ Function to classify sentiment with structured prompt
def classify_text(text):
    if text.strip() == "":
        return "Unknown", 0.0  # Handle missing or empty text entries
    
    # ✅ Add context using a structured prompt
    prompt = f"This is a technical discussion about quantum computing and software development. Identify the most appropriate sentiment category:\n\n'{text}'"

    # ✅ Perform zero-shot classification
    try:
        result = classifier(prompt, labels)
        sentiment = result["labels"][0]  # Get highest probability label
        score = round(result["scores"][0], 4)  # Get confidence score

        return sentiment, score
    except Exception as e:
        print(f"❌ Classification error: {e}")
        return "Error", 0.0  # ✅ Prevent crashes from unexpected errors

# ✅ Apply classification with batch processing (Faster Execution)
tqdm.pandas()
df[["Sentiment", "Sentiment Score"]] = df["Full_Text"].progress_apply(lambda x: pd.Series(classify_text(x)))

# ✅ Save the output with sentiment labels
df.to_csv(output_csv, index=False)

print(f"✅ Sentiment analysis complete! Output saved to: {output_csv}")
