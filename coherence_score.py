import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load coherence score data
csv_path = "D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_1/topics_cv.csv"
df = pd.read_csv(csv_path)

# Sort by number of topics (just in case)
df = df.sort_values(by="Topics")

# Create the plot
plt.figure(figsize=(10, 5))
plt.plot(df['Topics'], df['Coherence'], marker='o', linestyle='-', color='b', label="Coherence Score")

# Set X-axis to display only whole numbers
plt.xticks(np.arange(min(df['Topics']), max(df['Topics']) + 1, step=1))

# Add labels and title
plt.xlabel("Number of Topics (k)")
plt.ylabel("Coherence Score")
plt.title("LDA Coherence Score vs. Number of Topics")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
