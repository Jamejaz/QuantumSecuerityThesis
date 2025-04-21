import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_topic_distribution(topics_path, output_path):
    """
    Plot topic distribution from a topics.csv file.
    
    Args:
    - topics_path (str): Path to the topics.csv file.
    - output_path (str): Path to save the output plot.
    """
    # Load the topics.csv file
    topics = pd.read_csv(topics_path)
    
    # Sort by the number of documents assigned to each topic
    topics = topics.sort_values(by='Question_Count', ascending=False)
    
    # Set plot style
    sns.set_theme(style="whitegrid")
    
    # Create barplot
    plt.figure(figsize=(12, 6))
    chart = sns.barplot(
        data=topics,
        x="Topic",  # Topic index
        y="Question_Count",  # Number of documents
        palette="viridis"
    )
    
    # Customize labels and title
    chart.set_xlabel("Topic Index", fontsize=12)
    chart.set_ylabel("Number of questions", fontsize=12)
    chart.set_title("Topic Distribution", fontsize=14)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='right')

    # Save and display the plot
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()

# Main Execution
if __name__ == "__main__":
    # Path to the topics.csv file for a specific K
    topics_path = 'D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/topics.csv'
    
    # Path to save the plot
    output_path = 'D:/MS Business Analytics/Thesis and Internship/Programming/Total Data for Thesis/New_Preprocessed_Data/LDA_5_2/17topics/topic_distribution.png'
    
    # Plot the topic distribution
    plot_topic_distribution(topics_path, output_path)
