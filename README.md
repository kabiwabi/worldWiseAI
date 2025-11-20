# WorldWiseAI: Measuring Cultural Alignment in Large Language Models

## Overview
WorldWiseAI is a framework for rigorously evaluating **cultural alignment in Large Language Models (LLMs)** using Hofstede’s cultural dimensions as an analytical scaffold. Instead of prompting LLMs with survey-style Likert questions (which produces shallow or unreliable results), WorldWiseAI uses **semantic inference** to analyze *how* an LLM reasons in ethically or culturally charged scenarios.

This approach produces:
- A **semantic Hofstede-like cultural profile** for each LLM response
- **Overall cultural alignment** scores (how closely a persona matches a target culture)
- **Dimension-level alignment** (which Hofstede dimensions influence that alignment)
- **Baseline cultural bias** (which culture an unprompted model resembles)
- **Cultural shift magnitude** (how strongly a cultural persona influences model reasoning)

The framework includes:
- A full evaluation pipeline
- A scenario generator and parser
- A semantic cultural projection model
- Visualization tools
- Full results analysis

---

# 1. Motivation
LLMs increasingly serve global audiences—but their reasoning may implicitly reflect cultural biases or norms tied to training data.

Traditional methods (like directly asking Hofstede survey questions) fail because:
- LLMs produce **generic or memorized answers**.
- Hofstede surveys rely on **personal lived experience**, which LLMs lack.
- LLMs may answer based on **training-content stereotypes**, not reasoning.

WorldWiseAI addresses these issues by shifting the evaluation from:

> **"What does the model *say* about culture?" → "What cultural values emerge from its *reasoning*?""**

---

# 2. Methodology
WorldWiseAI measures cultural alignment in **three stages**:

## 2.1 Stage 1 — Scenario-Based Elicitation
LLMs are given ethically ambiguous scenarios designed to expose culturally influenced decision-making. For each run, a model receives:

- The **scenario**
- An optional **cultural persona prompt** (e.g., “As someone from India”)
- Instructions to explain its reasoning
- Extraction of:
  - **Decision outcome**
  - **Top 5 guiding values**
  - **Explanation text**

This creates rich, semantically meaningful text for analysis.

---

## 2.2 Stage 2 — Semantic Cultural Projection
The LLM’s reasoning text (values + explanation + decision summary) is embedded using a sentence-transformer. This yields a semantic vector representing the decision-making style.

For each Hofstede dimension (IDV, PDI, MAS, UAI, LTO, IVR), the vector is compared to a curated set of:
- **High-dimension exemplars** (e.g., High Individualism)<br>
- **Low-dimension exemplars** (e.g., Low Individualism)

Using cosine similarity:

```
high_sim = cos(response, high_exemplars)
low_sim  = cos(response, low_exemplars)
ratio = (high_sim - low_sim) / (high_sim + low_sim)
score = tanh(ratio) * 2
```

This produces a **continuous score in the range [-2, +2]** for each Hofstede dimension.

👉 This is NOT Hofstede’s 0–100 scale—but a semantic projection onto the *same conceptual axes*. Hofstede country scores are normalized to the same [-2, +2] range to enable valid comparison.

**Output:** A 6-dimensional "semantic Hofstede profile" that characterizes model reasoning.

---

## 2.3 Stage 3 — Cultural Alignment Metrics
From the semantic cultural profile, we compute several alignment metrics.

### **A) Overall Cultural Alignment (0–10)**
For each scenario, compare the model’s inferred cultural vector with the target culture’s normalized Hofstede vector:

- Take the **Euclidean distance** across the *scenario-relevant dimensions*
- Convert to a 0–10 similarity score:

```
alignment = 10 - distance * 2.5
```

This yields a single holistic measure of cultural fit.

### **B) Dimension-Level Alignment (0–10)**
Individually assess how close the model is on each Hofstede dimension:

```
score = 10 - |expected_dim - actual_dim| * 2.5
```

This reveals *which dimensions* contribute most to alignment or misalignment.

### **C) Baseline Cultural Bias**
Unprompted responses are averaged to form a baseline profile.
Distance to each country's cultural vector reveals **which culture the model resembles by default**.

### **D) Cultural Shift Magnitude**
Comparing baseline values to persona-prompted values yields a **total variation distance (TVD)** that measures:
- How strongly the persona prompt influences the model
- Which cultures exert greatest or weakest shifts

---

# 3. Experimental Setup
Experiments vary across:

- **Models:** GPT-4o-mini, Claude Haiku, Gemini Flash, etc.
- **Cultures:** US, India, Japan, Mexico, UAE, baseline (no culture)
- **Scenarios:** Ethically ambiguous cases tied to one or more Hofstede dimensions
- **Runs:** Each (model × culture × scenario) combination executed once

Caching ensures consistency across experiments.

---

# 4. Results Analysis (Most Important Section)

This section summarizes insights from the evaluation pipeline, grounded in the semantic projection methodology.

## 4.1 Overall Cultural Alignment (0–10)
Example (your latest run):

```
India............. 7.71
US................ 6.49
Japan............. 6.40
UAE............... 5.73
Mexico............ 5.22
```

### Interpretation
- The model most reliably emulates **Indian cultural reasoning**.
- The US and Japan are moderately aligned.
- UAE and Mexico are harder to emulate.

This pattern matches expectations for modern LLMs, whose training data over-represent certain cultural norms and online contexts.

---

## 4.2 Dimension-Level Alignment
Your new analysis reveals *why* certain cultures align better than others.

### Example output
```
           IDV   IVR   LTO   MAS   PDI   UAI
India     9.58  5.52  8.89  7.31  6.23  8.80
Japan     9.58  6.91  5.91  4.98  9.79  3.98
UAE       6.05  6.74  5.07  9.71  5.12  4.96
US        5.24  7.07  4.75  7.63  7.50  8.39
Mexico    6.15  5.58  5.27  6.08  5.22  3.97
```

### Interpretation
- **India**: high alignment comes from strong performance on **IDV**, **LTO**, **UAI**
- **Japan**: misalignment primarily from low **UAI** and **MAS**
- **UAE**: high **MAS**, weak **LTO**
- **US**: strong **UAI**, moderate **MAS**, weak **LTO**
- **Mexico**: difficulties in **UAI** and **PDI**

This breakdown directly explains the overall scores.

---

## 4.3 Baseline Cultural Bias
The model’s default reasoning (no persona) resembles:
- **Most strongly**: India
- **Moderately**: US and Japan
- **Least**: Mexico and UAE

This suggests an emergent bias toward **collectivist + long-term + moderate uncertainty avoidance** tendencies.

---

## 4.4 Cultural Shift Magnitude
Using value distributions and TVD:

- India shifts the model most (largest TVD)
- Japan and Mexico produce moderate shifts
- US produces the smallest shift

This suggests the model "accepts" US cultural framing more easily, possibly because US norms are embedded in training corpora.

---

## 4.5 Scenario Difficulty
Scenarios involving:
- **Uncertainty Avoidance (UAI)** and
- **Long-Term Orientation (LTO)**

were the hardest for all models.

Meanwhile, scenarios involving:
- **Individualism (IDV)**
- **Power Distance (PDI)**

were easier and more consistent.

---

# 5. Visualizations
Your `visualizer.py` module supports:
- Radar charts comparing model vs country profiles
- Heatmaps of dimension-level alignment
- Value distribution plots
- Cultural shift magnitude graphs

These visually tie together semantic profiles and alignment metrics.

---

# 6. Limitations
- Hofstede scores are **approximate anchors**, not absolute truth.
- Semantic embeddings capture **orientation**, not **survey magnitude**.
- Persona prompting measures **expressed reasoning**, not **true cultural identity**.
- Some cultures (e.g., UAE) lack direct Hofstede LTO/IVR data and rely on regional proxies.

---

# 7. Diagrams & Architecture

This section shows how the system is wired end-to-end and how the main findings are visualized. All figures are generated from `visualizer.py` using the results CSV.

## 7.1 System Architecture Overview

![Architecture Diagram](/mnt/data/architecture_diagram.png)

*Figure 1 – High-level architecture of WorldWiseAI. Scenarios and cultural personas are combined into prompts, sent to the LLMs, parsed into structured decisions + values, projected into Hofstede-style dimensions via semantic embeddings, and finally aggregated into metrics and visualizations.*

## 7.2 Baseline Cultural Bias

![Baseline Comparison](/mnt/data/baseline_comparison.png)

*Figure 2 – Baseline (no-persona) decision distribution and top values. This reveals the inherent value bias of the unprompted model before any cultural steering is applied.*

## 7.3 Cultural Alignment by Model and Culture

![Cultural Alignment](/mnt/data/cultural_alignment_by_model.png)

*Figure 3 – Overall cultural alignment scores by model and culture, with error bars. This highlights which cultures are easiest or hardest to emulate and shows that models cluster closely in performance.*

## 7.4 Cultural Shift Magnitude

![Cultural Shift](/mnt/data/cultural_shift_magnitude.png)

*Figure 4 – How strongly each cultural persona shifts the model away from its baseline value distribution (TVD). Collectivist cultures like Japan, UAE, and Mexico induce the largest shifts; the US prompt shifts the model the least.*

## 7.5 Performance by Scenario Category

![Category Performance](/mnt/data/category_performance.png)

*Figure 5 – Mean alignment scores grouped by scenario category (e.g., Social Situations, Career & Competition). This shows which kinds of dilemmas are easiest or hardest across all cultures and models.*

## 7.6 Scenario Difficulty Ranking

![Scenario Difficulty](/mnt/data/scenario_difficulty.png)

*Figure 6 – Scenario-level difficulty ranking. Scenarios with heavy Uncertainty Avoidance (UAI) or Long-Term Orientation (LTO) demands tend to have lower alignment scores, indicating that these dimensions are more challenging for LLMs.*

## 7.7 Decision Distribution by Culture

![Decision Distribution](/mnt/data/decision_distribution.png)

*Figure 7 – How often each culture chooses Option A, Option B, or declines to decide. This reveals culturally patterned decision tendencies layered on top of the same underlying scenarios.*

## 7.8 Decision Patterns by Model

![Decision Patterns](/mnt/data/decision_patterns.png)

*Figure 8 – Stacked percentages of decisions per model. This highlights model-level preferences (e.g., more risk-averse or compromise-seeking models) independent of culture.*

## 7.9 Value Frequencies by Culture

![Value Frequency](/mnt/data/value_frequency.png)

*Figure 9 – Top values (e.g., Family Harmony, Future Planning, Respect for Authority) by culture. This chart makes the emergent cultural signatures visible at the value level.*

## 7.10 Stereotype Scores by Model and Culture

![Stereotype Scores](/mnt/data/stereotype_scores.png)

*Figure 10 – Human-rated stereotype scores for each model–culture combination. Higher boxes indicate more frequent or stronger cultural stereotyping in the explanations.*

## 7.11 Model Comparison Radar

![Radar Plot](/mnt/data/model_comparison_radar.png)

*Figure 11 – Radar plot comparing models across aggregate metrics (Cultural Alignment, Stereotyping, Consistency, Differentiation). This provides a compact multidimensional comparison of model behavior.*

# 8. Summary & Contributions & Contributions
WorldWiseAI provides:
- A novel semantic method to measure cultural alignment in LLMs
- A full pipeline for extracting cultural profiles from text
- Dimension and overall alignment metrics
- Cross-model, cross-culture comparison tools
- Comprehensive scenario and value analysis

This approach offers a deeper understanding of how cultural norms emerge in LLM reasoning—without requiring unrealistic survey-style interactions.

---

If you want, I can now:
- Add diagrams
- Add citations
- Add a “How to run experiments” section
- Add instructions for reproducing results

Just tell me what you want next!

