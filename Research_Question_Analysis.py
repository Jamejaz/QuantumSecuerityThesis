import pandas as pd
import re

# ========== Load Dataset ==========
df_raw = pd.read_csv(
    r'D:\MS Business Analytics\Thesis and Internship\Programming\Total Data for Thesis\New_Preprocessed_Data\LDA_5_2\17topics\question_topic.csv'
)
df_raw.rename(columns={"Questions": "Dominant_Keywords"}, inplace=True)

# ========== Define Keyword Lists ==========

quantum_tools = [
    "openqkd", "qkdnet", "secoqc", "qunetsim", "netsquid", "simulaqron", "squanch",
    "liboqs", "oqs", "kyber", "dilithium", "frodo", "ntru", "rainbow", "mceliece", "pqc-crypto",
    "qiskit", "cirq", "qdk", "qutip", "stim", "projectq", 
    "pennylane", "openqasm", "braket", "forest"
]

quantum_algorithms = [
    "bb84", "e91", "qkd", "shor", "grover", "vqe", "qaoa",
    "quantum key distribution", "shor code", "steane code", "surface code",
    "magic state distillation", "zero noise extrapolation", "quantum phase estimation", "qpe", "quantum fourier transform", "qft", 
    "quantum teleportation", "hhl", "amplitude amplification", "swap test", "quantum annealing", "quantum cryptography", "quantum secure communication", "quantum authentication", 
    "quantum digital signature", "quantum error correction", "stabilizer code"


]

classical_algorithms = [
    "rsa", "aes", "sha-2", "sha-3", "hmac", "ecc",
    "ntru", "kyber", "frodo", "rainbow", "mceliece", "sphincs", "xmss", "lattice", "post quantum"
]

challenge_categories = {
    "Technical": [
        "error", "noise", "decoherence", "leakage", "crosstalk", "fault", "stability",
        "latency", "scalability", "precision", "synchronization", "gate fidelity",
        "hardware limitation", "measurement error", "control error", "signal loss",
        "thermal noise", "qubit failure", "readout error", "timing issue", "circuit noise", "gate noise", "hardware error", "depolarizing noise"
    ],
    "Implementation": [
        "implementation", "benchmark", "simulation", "verification", "circuit depth",
        "compilation", "runtime", "deployment", "debugging", "compiler issue",
        "resource overhead", "optimization", "test case", "gate decomposition", "device mismatch", "tableau", "conversion", "encoding", "decoding", "circuit transformation", "generate circuit"
    ],
    "Security": [
        "attack", "vulnerability", "eavesdropping", "authentication", "privacy", "key loss",
        "qkd failure", "side-channel", "protocol breach", "intercept", "spoofing",
        "key exhaustion", "tampering", "message forgery", "quantum threat", "quantum-safe", "post-quantum", "cryptographic failure", "data breach", 
        "secure transmission", "man-in-the-middle", "quantum intercept", "quantum spoofing"

    ],
    "General": [
        "problem", "issue", "challenge", "difficult", "limitation", "unstable",
        "complex", "bug", "error-prone", "confusing", "unclear", "not working",
        "unexpected result", "no output"
    ]
}

adoption_keywords = [
    "adoption", "deployment", "integration", "standard", "interoperability",
    "secure system", "compliance", "real-world", "use case", "production",
    "framework", "product", "enterprise", "design pattern", "application",
    "system design", "rollout", "commercial", "deployment strategy"
]

development_keywords = [
    "error", "noise", "calibration", "correction", "fault", "leakage",
    "stabilizer", "decoherence", "crosstalk", "gate fidelity", "testbed", "compiler",
    "debug", "runtime", "latency", "circuit", "qubit", "error mitigation", 
    "measurement", "stability", "timing", "simulation", "hardware limitation"
]

learning_keywords = [
    "learning", "tutorial", "basics", "beginner", "introduction", "how to", 
    "understand", "what is", "getting started", "guide", "overview",
    "help", "simple explanation", "definition", "difference between", 
    "step by step", "documentation", "confused", "resources", "explain"
]

exploration_keywords = [
    "future", "potential", "research", "exploration", "compare", "comparison",
    "alternative", "limitation", "theory", "proposal", "approach", 
    "open problem", "state of the art", "novel", "suggestion", "hypothesis", 
    "evaluation", "versus", "paper", "survey", "idea","why", "explain", "reason", "intuition", "interpret", "meaning", "how does", "what happens if"
]

implementation_keywords = [
    "implementation", "simulate", "compile", "execute", "run", "build", "code", 
    "workflow", "layout", "gates", "circuit", "qubit register", "noise model", 
    "qaoa", "vqe", "mixer", "qiskit", "pennylane", "qulacs", "runtime", 
    "ibm hardware", "test circuit", "compile error", "execution", "generate", "build circuit", "construct", "create", "design", "manual encoding", "simulate attack", "test security", "security test", "protocol implementation", "secure protocol", "simulate qkd"


]

stage_keywords = {
    "Implementation": implementation_keywords,
    "Development": development_keywords,
    "Adoption": adoption_keywords,
    "Learning": learning_keywords,
    "Exploration": exploration_keywords
}

# Define lifecycle and challenge detection functions
def detect_lifecycle_stages(text):
    text = str(text).lower()
    scores = {stage: sum(1 for word in keywords if re.search(r'\b' + re.escape(word) + r'\b', text))
              for stage, keywords in stage_keywords.items()}
    scores = {k: v for k, v in scores.items() if v > 0}
    if not scores:
        return "Unclassified", ""
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores[0][0], sorted_scores[1][0] if len(sorted_scores) > 1 else ""


def detect_challenges(text):
    text = str(text).lower()
    scores = {}
    for category, keywords in challenge_categories.items():
        count = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', text))
        if count > 0:
            scores[category] = count
    if not scores:
        return "Unclassified", ""
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores[0][0], sorted_scores[1][0] if len(sorted_scores) > 1 else ""


# Set your output path base
output_base = r'D:\MS Business Analytics\Thesis and Internship\Programming\Total Data for Thesis\New_Preprocessed_Data\LDA_5_2\17topics\trend'

# ---------------- Q1: Tools ----------------
df_q1 = df_raw.copy()
df_q1["Mentions_Tool"] = df_q1["Question"].apply(
    lambda q: ", ".join([tool for tool in quantum_tools if tool in str(q).lower()])
)
df_q1.to_csv(f"{output_base}/q1_tools_all_questions.csv", index=False)

# Q1 Summary
q1_exploded = df_q1[df_q1["Mentions_Tool"] != ""].copy()
q1_exploded["Tool"] = q1_exploded["Mentions_Tool"].str.split(", ")
q1_exploded = q1_exploded.explode("Tool")
q1_exploded["Tool"] = q1_exploded["Tool"].str.strip()
q1_summary = q1_exploded["Tool"].value_counts().reset_index()
q1_summary.columns = ["Tool", "Total_Questions"]
q1_summary["Percentage"] = 100 * q1_summary["Total_Questions"] / len(df_raw)
q1_summary.to_csv(f"{output_base}/q1_tools_summary.csv", index=False)

# ---------------- Q2: Lifecycle ----------------
df_q2 = df_raw.copy()
df_q2[["Primary_Stage", "Secondary_Stage"]] = df_q2["Question_body"].apply(
    lambda x: pd.Series(detect_lifecycle_stages(x))
)
df_q2.to_csv(f"{output_base}/q2_lifecycle_all_questions.csv", index=False)

# Q2 Summary
topic_totals = df_q2["Topic"].value_counts().reset_index()
topic_totals.columns = ["Topic", "Total_Questions"]
stage_counts = df_q2.groupby(["Topic", "Primary_Stage"]).size().reset_index(name="Count")
q2_summary = pd.merge(stage_counts, topic_totals, on="Topic")
q2_summary["Percentage"] = 100 * q2_summary["Count"] / q2_summary["Total_Questions"]
q2_summary.to_csv(f"{output_base}/q2_lifecycle_summary.csv", index=False)

# ---------------- Q3: Algorithms ----------------
df_q3 = df_raw.copy()
df_q3["Mentions_Algorithm"] = df_q3["Question"].apply(
    lambda q: ", ".join([alg for alg in quantum_algorithms + classical_algorithms if alg in str(q).lower()])
)
df_q3.to_csv(f"{output_base}/q3_algorithm_all_questions.csv", index=False)

q3_exploded = df_q3[df_q3["Mentions_Algorithm"] != ""].copy()
q3_exploded["Algorithm"] = q3_exploded["Mentions_Algorithm"].str.split(", ")
q3_exploded = q3_exploded.explode("Algorithm")
q3_exploded["Algorithm"] = q3_exploded["Algorithm"].str.strip()
q3_summary = q3_exploded["Algorithm"].value_counts().reset_index()
q3_summary.columns = ["Algorithm", "Total_Questions"]
q3_summary["Percentage"] = 100 * q3_summary["Total_Questions"] / len(df_raw)
q3_summary.to_csv(f"{output_base}/q3_algorithm_summary.csv", index=False)

# ---------------- Q4: Challenges ----------------
df_q4 = df_raw.copy()
df_q4[["Primary_Challenge", "Secondary_Challenge"]] = df_q4["Question"].apply(
    lambda x: pd.Series(detect_challenges(x))
)
df_q4.to_csv(f"{output_base}/q4_challenges_all_questions.csv", index=False)

q4_valid = df_q4[df_q4["Primary_Challenge"] != "Unclassified"]
q4_summary = q4_valid["Primary_Challenge"].value_counts().reset_index()
q4_summary.columns = ["Challenge", "Total_Questions"]
q4_summary["Percentage"] = 100 * q4_summary["Total_Questions"] / len(df_raw)
q4_summary.to_csv(f"{output_base}/q4_challenges_summary.csv", index=False)

print("✅ All Q1–Q4 files generated: full datasets + summaries")

