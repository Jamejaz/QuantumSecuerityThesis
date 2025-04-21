import pandas as pd
import re
import gensim
import spacy
import nltk
from nltk.corpus import stopwords
import Stemmer
import tqdm

def preprocess():
    # Download stopwords if not already downloaded
    nltk.download('stopwords')

    # Load standard NLTK stopwords
    stop_words = set(stopwords.words('english'))

    # Extend stopwords with additional words
    stop_words.update([
        'make', 'need', 'get', 'thing', 'good', 'well', 'go', 'work', 'way', 'think', 'know', 'say', 'take', 'use', 'find', 'help', 'give', 'put', 'keep', 'see', 'seem', 'try', 'start', 'stop', 'want', 'like', 'ask', 'explain', 'x', 'com', 'time', 'post', 'begin', 'otim', 'blog', 'paper', 'close',
        'people', 'question', 'answer', 'thing', 'example', 'case', 'part', 'point', 'problem', 'solution', 'issue', 'idea', 'method', 'heard', 'user', 'comment', 'timelin', 'guy', 'follow', 'topic', 'https', 'professor', 'lecture',
        'actually', 'probably', 'maybe', 'really', 'already', 'just', 'kind', 'sort', 'basically', 'definitely', 'obviously', 'literally', '_', 'install', 'Paper', "Game"
    ])

    # Load Spacy model for lemmatization
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

    # Initialize Stemmer
    stemmer = Stemmer.Stemmer('english')

    # Load CSV data
    df = pd.read_csv(r'D:\MS Business Analytics\Thesis and Internship\Programming\Total Data for Thesis\NoDuplicates_Master_File.csv')

    # Convert questions to lowercase
    df['question'] = df['question'].astype(str).str.lower()

    # **Step 1: Keep any question that contains any form of "quantum"**
    df = df[df['question'].str.contains(r'quantum[a-z]*', regex=True, na=False)]  # Matches quantum, quantumly, quantumerror, etc.

    # List of relevant keywords
    keywords = {
        "error correction", "surface code", "steane code", "shor code", "quantum parity check", "syndrome measurement",
        "stabilizer", "fault tolerant", "magic state distillation", "state injection model", "zero noise extrapolation",
        "probabilistic error cancellation", "measurement error mitigation", "vqe", "quantum key distribution",
        "BB84", "E91", "NTRU", "Rainbow", "homomorphic encryption", "quantum shielding", "cirq", "randomised benchmarking",
        "depolarizing channel", "decoherence", "toric code", "stim", "color code", "lattice structure", "encryption",
        "no cloning theorem", "quantum teleportation", "bell test", "entanglement purification", "dynamical decoupling",
        "cross talk", "qubit leakage", "quantum gate calibration", "qkd", "noise", "error", "surface", "steane", "shor", "toric"
    }

    # Convert keywords to lowercase
    keywords = {kw.lower() for kw in keywords}

    # **Step 2: Apply additional keyword filtering**
    df = df[df['question'].apply(lambda x: any(kw in x for kw in keywords))]

    # Remove duplicate questions
    df.drop_duplicates(subset=['question'], keep='first', inplace=True)

    # Convert questions to a list
    data = df['question'].tolist()

    # Initialize progress bar
    pbar = tqdm.tqdm(total=len(data))

    new_data = []
    for doc in data:
        # Remove code snippets
        new_doc = re.sub(r'<code>.*?</code>', '', doc, flags=re.S)
        # Remove HTML tags
        new_doc = re.sub(r'<.*?>', '', new_doc)
        # Convert text to lowercase, tokenize, remove punctuation
        new_doc = gensim.utils.simple_preprocess(str(new_doc), deacc=True)
        # Lemmatization (keeping only nouns, adjectives, verbs, and adverbs)
        new_doc = lemmatization(nlp, new_doc)
        # Stemming
        new_doc = stemmer.stemWords(new_doc)
        # Remove stopwords
        new_doc = [word for word in new_doc if word not in stop_words]
        new_data.append(new_doc)
        pbar.update(1)

    # Remove low-frequency words while keeping keywords safe
    new_data = remove_low_frequency_words(new_data, threshold=10, keywords=keywords, pbar=pbar)

    # Convert list back to strings for CSV
    df['question'] = [",".join(doc) for doc in new_data]

    # Save preprocessed data to CSV
    df.to_csv(r'D:\MS Business Analytics\Thesis and Internship\Programming\Total Data for Thesis\preprocessed_NODuplicate_Master_File.csv', index=False)

    pbar.close()

def lemmatization(nlp, doc, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """Applies lemmatization to words, keeping only specific parts of speech."""
    return [token.lemma_ for token in nlp(" ".join(doc)) if token.pos_ in allowed_postags]

def remove_low_frequency_words(data, threshold=10, keywords=None, pbar=None):
    """Removes words that appear less than `threshold` times in the dataset, but keeps keywords."""
    if keywords is None:
        keywords = set()  # Ensure it's a set for quick lookup

    word_freq = {}
    for doc in data:
        for word in doc:
            word_freq[word] = word_freq.get(word, 0) + 1
        if pbar:
            pbar.update(1)

    # Identify words to remove (excluding keywords)
    low_freq_words = {word for word, count in word_freq.items() if count < threshold and word not in keywords}

    # Remove low-frequency words, but keep keywords
    filtered_data = [[word for word in doc if word not in low_freq_words] for doc in data]
    
    if pbar:
        pbar.update(len(data))

    return filtered_data

# Run preprocessing
preprocess()
