# --------------------------- IMPORTS ---------------------------
import re
import pandas as pd
import numpy as np
import gensim
import gensim.corpora as corpora
from gensim.models.coherencemodel import CoherenceModel
import tqdm
import os
import logging
import pickle
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis

# --------------------------- Configuration ---------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --------------------------- Keyword Set ---------------------------
KEYWORDS = {
    "error correction", "surface code", "steane code", "shor code", "quantum parity check", "syndrome measurement",
    "stabilizer", "fault-tolerant", "magic state distillation", "state injection model", "zero noise extrapolation",
    "probabilistic error cancellation", "measurement error mitigation", "vqe", "quantum key distribution",
    "BB84", "E91", "NTRU", "Rainbow", "homomorphic encryption", "quantum shielding", "Cirq", "randomized benchmarking",
    "depolarizing channel", "decoherence", "toric code", "stim", "color code", "lattice structure", "encryption",
    "no cloning theorem", "quantum teleportation", "Bell test", "entanglement purification", "dynamical decoupling",
    "cross talk", "qubit leakage", "quantum gate calibration", "QKD", "noise", "error", "surface", "steane",
    "shor", "color", "toric"
}

# --------------------------- Utilities ---------------------------
def clean_keywords(words):
    """Remove non-alphabetic tokens from keyword list."""
    return [word for word in words if re.match(r"^[a-zA-Z]+$", word)]

def boost_keywords(tokens, boost_factor=3):
    """Duplicate important technical keywords."""
    boosted = []
    for token in tokens:
        if token in KEYWORDS:
            boosted.extend([token] * boost_factor)
        else:
            boosted.append(token)
    return boosted

def get_texts_id2word_corpus():
    """Load the dataset and prepare texts, id2word dictionary, and corpus for LDA."""
    logging.info("🔄 Loading dataset...")
    df = pd.read_csv('D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/Final_Data_file.csv')
    df['Question'] = df['Question'].fillna('')
    data_preprocessed = [boost_keywords(doc.split(',')) for doc in df['Question'].tolist()]

    id2word = corpora.Dictionary(data_preprocessed)
    id2word.filter_extremes(no_below=5, no_above=0.5)
    corpus = [id2word.doc2bow(doc) for doc in data_preprocessed]

    logging.info(f"📘 Dictionary created with {len(id2word)} unique tokens.")
    return df, data_preprocessed, id2word, corpus

def train_lda(texts, id2word, corpus, k, a, b):
    """Train the LDA model and return model and coherence score."""
    logging.info(f"🎯 Training LDA: Topics={k}, Alpha={a}, Beta={b}...")
    lda_model = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        id2word=id2word,
        num_topics=k,
        random_state=100,
        chunksize=500,
        passes=10,
        iterations=100,
        alpha=a,
        eta=b
    )

    coherence_model = CoherenceModel(model=lda_model, texts=texts, dictionary=id2word, coherence='c_v')
    coherence_score = coherence_model.get_coherence()

    logging.info(f"✅ Model trained | Coherence Score: {coherence_score:.4f}")
    return lda_model, coherence_score

def assign_questions_to_topics(lda_model, corpus, df):
    """Assign the dominant topic and keywords to each question."""
    topic_assignments = []
    dominant_keywords = []

    for doc in corpus:
        topic_dist = lda_model.get_document_topics(doc, minimum_probability=0)
        dominant_topic = sorted(topic_dist, key=lambda x: x[1], reverse=True)[0][0]
        topic_assignments.append(dominant_topic)

        topic_words = lda_model.show_topic(dominant_topic, topn=10)
        cleaned_keywords = clean_keywords([word for word, _ in topic_words])[:5]
        dominant_keywords.append(", ".join(cleaned_keywords))

    df['Topic'] = topic_assignments
    df['Dominant_Keywords'] = dominant_keywords
    return df

def save_topic_weightage(lda_model, id2word, save_path):
    """Save topic-keyword weightage matrix."""
    keywords = []
    topics = []
    weights = []

    for topic_id in range(lda_model.num_topics):
        terms = lda_model.get_topic_terms(topic_id, topn=50)
        for word_id, weight in terms:
            keywords.append(id2word[word_id])
            topics.append(topic_id)
            weights.append(weight)

    weight_df = pd.DataFrame({
        'Topic': topics,
        'Keyword': keywords,
        'Weight': weights
    })
    weight_df.to_csv(f"{save_path}/topic_keyword_matrix.csv", index=False)
    logging.info(f"📁 Topic weightage matrix saved to {save_path}/topic_keyword_matrix.csv")

def record_lda(df, topics, alpha, beta, lda_model, coherence_score, corpus, id2word):
    """Save topic-level, question-level, model, corpus, dictionary, and visualization to files."""
    path = f'D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/{topics}topics'
    os.makedirs(path, exist_ok=True)

    # Save topic summary
    topic_counts = df['Topic'].value_counts().reindex(range(topics), fill_value=0)
    topics_df = pd.DataFrame({
        "Topic": range(topics),
        "Keywords": [
            ", ".join(clean_keywords([word for word, _ in lda_model.show_topic(t, topn=10)]))
            for t in range(topics)
        ],
        "Question_Count": topic_counts.values,
        "Coherence_Score": [coherence_score] * topics
    })
    topics_df.to_csv(f'{path}/topics.csv', index=False)

    # Save question-topic assignment
    df.to_csv(f'{path}/question_topic.csv', index=False)

    # Save topic weightage
    save_topic_weightage(lda_model, id2word, save_path=path)

    # Save model, corpus, dictionary
    lda_model.save(f"{path}/lda_model.model")
    with open(f"{path}/corpus.pkl", 'wb') as f:
        pickle.dump(corpus, f)
    id2word.save(f"{path}/id2word.dict")

    # Save pyLDAvis visualization
    vis_data = gensimvis.prepare(lda_model, corpus, id2word)
    pyLDAvis.save_html(vis_data, f"{path}/lda_visualization.html")

    logging.info(f"✅ All outputs saved to {path}")

def iterate_parameter():
    """Grid search over different topic numbers with fixed alpha and beta."""
    df, texts, id2word, corpus = get_texts_id2word_corpus()

    topics_range = range(2, 21, 1)  # Trying 2 to 20 topics
    alpha = ['asymmetric']
    beta = [0.01]

    model_results = {'Topics': [], 'Alpha': [], 'Beta': [], 'Coherence': []}
    pbar = tqdm.tqdm(total=len(topics_range) * len(alpha) * len(beta), desc="🔍 Searching LDA Params")

    for k in topics_range:
        for a in alpha:
            for b in beta:
                lda_model, coherence_score = train_lda(texts, id2word, corpus, k, a, b)
                df_topic = assign_questions_to_topics(lda_model, corpus, df)

                model_results['Topics'].append(k)
                model_results['Alpha'].append(a)
                model_results['Beta'].append(b)
                model_results['Coherence'].append(coherence_score)

                record_lda(df_topic, k, a, b, lda_model, coherence_score, corpus, id2word)
                pbar.update(1)

    coherence_df = pd.DataFrame(model_results)
    coherence_df.to_csv('D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/topics_cv.csv', index=False)
    logging.info("✅ All coherence scores saved to topics_cv.csv")
    pbar.close()

# --------------------------- Entry Point ---------------------------
if __name__ == '__main__':
    iterate_parameter()
