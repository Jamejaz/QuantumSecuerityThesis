# Exploring Quantum Computing Security Discussions on Practitioner Platforms: A Multi-Platform Empirical Study

## Overview

This repository contains the replication package and supporting materials for the research paper:

**"Exploring Quantum Computing Security Discussions on Practitioner Platforms: A Multi-Platform Empirical Study"**

The study investigates how practitioners discuss quantum computing security (QCS) across multiple online platforms. Using large-scale data collection, topic modeling, sentiment analysis, trend analysis, and qualitative coding, the research provides insights into emerging security concerns, practitioner challenges, tool adoption, algorithm discussions, and emotional expressions within the quantum computing community.

## Abstract

Quantum computing introduces new opportunities and security challenges that affect software development, cryptography, infrastructure, and hardware systems. While academic research has extensively explored technical aspects of quantum security, less attention has been given to practitioner perspectives.

This study analyzes 15,353 discussions collected from Quantum Computing Stack Exchange (QCSE), Stack Overflow (SO), GitHub, Reddit, Math Stack Exchange (MSE), and Stack Exchange Security (SES). After applying security-focused filtering criteria, 5,163 quantum computing security-related posts were retained for analysis.

Topic modeling identified 17 recurring discussion themes, including cryptographic vulnerabilities, secure algorithm design, quantum state operations, error correction, hardware security constraints, and secure implementation concerns. Tool and framework analysis revealed Qiskit, Stim, and Cirq as the most frequently discussed technologies. Algorithm analysis showed strong practitioner interest in Variational Quantum Eigensolver (VQE), Shor's Algorithm, Quantum Phase Estimation (QPE), Quantum Fourier Transform (QFT), and Quantum Approximate Optimization Algorithm (QAOA).

Qualitative analysis identified five major practitioner challenge categories:

* Quantum Hardware Security Constraints
* Quantum Infrastructure & Tooling Risks
* Cryptographic Transition & Post-Quantum Threats
* Conceptual & Developer Readiness Gaps
* Algorithmic & Protocol Vulnerabilities

Sentiment analysis further revealed nine emotional categories, with Neutral discourse dominating practitioner discussions while Confidence, Curiosity, Frustration, and Confusion highlighted different aspects of practitioner experience.

This repository provides datasets, analysis scripts, topic modeling outputs, figures, and supplementary materials to support transparency, reproducibility, and future research in quantum computing security.

---

## Research Questions

The study addresses the following research questions:

### RQ1

What tools and frameworks are most frequently discussed in quantum computing security-related practitioner discussions?

### RQ2

What security-related topics emerge from practitioner discussions, and how do these topics evolve over time?

### RQ3

Which quantum and post-quantum algorithms are most frequently discussed within security-related practitioner discourse?

### RQ4

What challenges do practitioners encounter when developing, implementing, or securing quantum computing systems?

### RQ5

What emotional expressions are present in practitioner discussions on quantum computing security?

---

## Data Sources

The dataset was collected from the following platforms:

* Quantum Computing Stack Exchange (QCSE)
* Stack Overflow (SO)
* GitHub Discussions
* Reddit
* Math Stack Exchange (MSE)
* Stack Exchange Security (SES)

### Dataset Statistics

| Stage                            | Number of Posts |
| -------------------------------- | --------------: |
| Initial collected posts          |          15,353 |
| Security-relevant posts retained |           5,163 |

---

## Methodology

The study follows a Knowledge Discovery in Databases (KDD) process consisting of:

1. Data Collection
2. Data Cleaning and Preprocessing
3. Security-Relevance Filtering
4. Topic Modeling using Keyword-Assisted LDA
5. Tool and Framework Analysis
6. Algorithm Analysis
7. Temporal Trend Analysis
8. Qualitative Thematic Analysis
9. Sentiment Analysis

### Topic Modeling

* Method: Keyword-Assisted Latent Dirichlet Allocation (LDA)
* Number of Topics: 17
* Topic Coherence (c_v): ~0.52

### Sentiment Analysis

A prompt-based zero-shot sentiment classification approach was used to identify practitioner emotional expressions.

Sentiment categories:

* Neutral
* Confidence
* Curiosity
* Frustration
* Confusion
* Doubt
* Skepticism
* Agreement
* Disagreement

---

## Key Findings

### Most Discussed Tools and Frameworks

* Qiskit
* Stim
* Cirq
* PennyLane
* Q#
* Qiskit Aer
* OpenQASM

### Most Discussed Algorithms

* Variational Quantum Eigensolver (VQE)
* Shor's Algorithm
* Quantum Phase Estimation (QPE)
* Quantum Fourier Transform (QFT)
* Quantum Approximate Optimization Algorithm (QAOA)

### Practitioner Challenge Categories

1. Quantum Hardware Security Constraints
2. Quantum Infrastructure & Tooling Risks
3. Cryptographic Transition & Post-Quantum Threats
4. Conceptual & Developer Readiness Gaps
5. Algorithmic & Protocol Vulnerabilities

### Sentiment Findings

* Neutral: 83.44%
* Confidence and Curiosity indicate active exploration and learning.
* Frustration and Confusion are primarily associated with hardware limitations, execution issues, and toolchain instability.

## Reproducibility

This repository is intended as a replication package and contains:

* Data processing scripts
* Topic modeling outputs
* Sentiment classification outputs
* Statistical summaries
* Figures and tables used in the paper
* Supplementary analysis materials

Researchers can reproduce the major findings reported in the paper by following the provided workflow and scripts.


## License

This repository is released for academic and research purposes. Please ensure compliance with the terms of service of the original data sources when reusing or redistributing data.

## Contact

For questions, issues, or collaboration opportunities, please open an issue or contact the repository maintainers.

