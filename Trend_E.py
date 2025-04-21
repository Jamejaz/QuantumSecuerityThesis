import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define topic titles for K=11
topicsText = [
    'T1: Programming Constructs',
    'T2: Fourier Transform & Phase Estimation',
    'T3: Computational Complexity & Shor’s Algorithm',
    'T4: Stim Simulation & Decoding',
    'T5: Fault-Tolerant Error Correction',
    'T6: Controlled & Native Gate Operations',
    'T7: Matrix Ops & Quantum Operators',
    'T8: Group Structures in QEC',
    'T9: Teleportation Simulation',
    'T10: State Transmission & Cryptography',
    'T11: Qiskit Simulations & Experiments',
    'T12: Optimization & Quantum-Classical Integration',
    'T13: Installation & Environment Troubleshooting',
    'T14: Quantum Chemistry & Hamiltonians',
    'T15: State Transformations & Density Matrices',
    'T16: Qiskit Backend Management',
    'T17: Q# Programming & Post-Quantum Integration'

]

def topics_trend():
    # Load the data
    documents = pd.read_csv('D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/question_topic.csv')

    # Validate and parse date column
    if 'date' in documents.columns:
        documents['date'] = pd.to_datetime(documents['date'], errors='coerce', utc=True)
        documents['date'] = documents['date'].dt.tz_convert(None)
    else:
        print("⚠️ 'date' column is missing.")
        return

    documents = documents.dropna(subset=['date'])
    documents = documents.sort_values(by='date')

    # Initialize storage for 17 topics
    topics_documents = [pd.DataFrame(columns=documents.columns) for _ in range(17)]
    topics_documents_count = [0] * 17

    # Assign questions to corresponding topic
    for _, row in documents.iterrows():
        topic = int(row['Topic'])

        if 0 <= topic < 17:
            topics_documents[topic] = pd.concat([topics_documents[topic], row.to_frame().T], ignore_index=True)
            topics_documents_count[topic] += 1

    # Save each topic's data
    output_dir = "D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/trend_documents"
    os.makedirs(output_dir, exist_ok=True)

    for num in range(17):
        topics_documents[num].to_csv(f"{output_dir}/{num}.csv", index=False)

    print(f"✅ All topic documents saved to: {output_dir}")

    # Plot trend for each topic
    for num in range(17):
        data = get_draw_documents(topics_documents[num], topicsText[num])
        if not data.empty:
            sns.set_theme()
            sns.lmplot(data=data, order=3, x="date", y="Number of Questions", height=10)
            plt.title(f'{topicsText[num]} - Distribution of Questions over Time', loc='left')
            plt.subplots_adjust(top=0.95)

            image_dir = "D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/trend/image"
            os.makedirs(image_dir, exist_ok=True)

            plt.savefig(f"{image_dir}/{num}.png")
            plt.show()

def get_draw_documents(documents, topic_name):
    if documents.empty:
        return pd.DataFrame(columns=['date', 'Number of Questions', 'Question Types'])

    documents['date'] = pd.to_datetime(documents['date'], errors='coerce')
    documents['YearMonth'] = documents['date'].dt.to_period('M')
    grouped = documents.groupby('YearMonth').size().reset_index(name='Number of Questions')
    grouped['date'] = grouped['YearMonth'].astype(str).apply(lambda x: float(x[:4]) + (int(x[5:7]) - 1) / 12)
    grouped['Question Types'] = topic_name

    return grouped[['date', 'Number of Questions', 'Question Types']]

# Run the analysis
topics_trend()







