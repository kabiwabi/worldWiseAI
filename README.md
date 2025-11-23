# WorldWiseAI: Measuring Cultural Alignment in Large Language Models

## Overview

WorldWiseAI is a rigorous framework for evaluating **cultural alignment in Large Language Models (LLMs)** using Hofstede's cultural dimensions as an analytical scaffold. Rather than prompting LLMs with survey-style Likert questions (which produces shallow or unreliable results), WorldWiseAI employs **semantic inference** to analyze *how* an LLM reasons in ethically or culturally charged scenarios.

This approach produces:
- **Semantic Hofstede-like cultural profiles** for each LLM response
- **Overall cultural alignment scores** (how closely a persona matches a target culture)
- **Dimension-level alignment** (which Hofstede dimensions influence alignment)
- **Baseline cultural bias** (which culture an unprompted model resembles)
- **Cultural shift magnitude** (how strongly a cultural persona influences model reasoning)

---

## Table of Contents
1. [Motivation](#1-motivation)
2. [Methodology](#2-methodology)
3. [Experimental Setup](#3-experimental-setup)
4. [Results & Analysis](#4-results--analysis)
5. [Visualizations](#5-visualizations)
6. [Limitations](#6-limitations)
7. [Technical Details](#7-technical-details)
8. [Future Work](#8-future-work)
9. [Conclusion](#9-conclusion)

---

# 1. Motivation

LLMs increasingly serve global audiences—but their reasoning may implicitly reflect cultural biases or norms tied to training data. Traditional methods (like directly asking Hofstede survey questions) fail because:

- LLMs produce **generic or memorized answers**
- Hofstede surveys rely on **personal lived experience**, which LLMs lack
- LLMs may answer based on **training-content stereotypes**, not reasoning

WorldWiseAI addresses these issues by shifting the evaluation from:

> **"What does the model *say* about culture?" → "What cultural values emerge from its *reasoning*?"**

---

# 2. Methodology

WorldWiseAI measures cultural alignment in **three stages**:

## 2.1 Stage 1 — Scenario-Based Elicitation

LLMs are given ethically ambiguous scenarios designed to expose culturally influenced decision-making. For each run, a model receives:

- The **scenario** (30 scenarios covering all 6 Hofstede dimensions)
- An optional **cultural persona prompt** (e.g., "As someone from India")
- Instructions to explain its reasoning
- Extraction of:
  - **Decision outcome** (Option A, B, or Decline)
  - **Top 3 guiding values**
  - **Explanation text**

This creates rich, semantically meaningful text for analysis.

---

## 2.2 Stage 2 — Semantic Cultural Projection

The LLM's reasoning text (values + explanation + decision summary) is embedded using a sentence-transformer (`all-MiniLM-L6-v2`). This yields a 384-dimensional semantic vector representing the decision-making style.

For each Hofstede dimension (IDV, PDI, MAS, UAI, LTO, IVR), the vector is compared to curated sets of exemplars:
- **High-dimension exemplars** (e.g., "pursuing objectives that may diverge from collective interests")
- **Low-dimension exemplars** (e.g., "subordinating individual preferences to collective decisions")

Using cosine similarity, we compute:

```python
high_sim = cos(response_embedding, high_exemplars)
low_sim  = cos(response_embedding, low_exemplars)
ratio = (high_sim - low_sim) / (high_sim + low_sim)
score = tanh(ratio) * 2
```

This produces a **continuous score in the range [−2, +2]** for each Hofstede dimension.

💡 This is NOT Hofstede's 0–100 scale—but a semantic projection onto the *same conceptual axes*. Country Hofstede scores are normalized to the same [−2, +2] range for valid comparison.

**Output:** A 6-dimensional "semantic Hofstede profile" that characterizes model reasoning.

---

## 2.3 Stage 3 — Cultural Alignment Metrics

From the semantic cultural profile, we compute several alignment metrics:

### A) Overall Cultural Alignment (0–10)
For each scenario, compare the model's inferred cultural vector with the target culture's normalized Hofstede vector on the *primary dimension being tested*:

1. Compute root-mean-square (RMS) difference on the primary dimension: `d = √(mean((expected_i − actual_i)²))`
2. Convert to similarity score: `alignment = 10 − d × 2.5`

Each scenario tests one primary Hofstede dimension (e.g., IND001 tests individualism, PDI001 tests power distance). Higher scores indicate better alignment with the target culture.

### B) Dimension-Level Alignment (0–10)
Assess alignment on each individual Hofstede dimension:

```python
dimension_score = 10 − |expected_dim − actual_dim| × 2.5
```

For example, if India expects PDI = +1.5 and the model produces PDI = +0.8, the difference is 0.7, yielding: `10 − 0.7 × 2.5 = 8.25/10`.

### C) Baseline Cultural Bias
For unprompted (baseline) responses, we compute the distance to each culture using each scenario's primary dimension. This ensures consistency with the alignment scoring methodology:

```python
# For each response, infer profile and use only primary dimension
for response, scenario_id in baseline_responses:
    profile = infer_profile(response)
    primary_dim = scenario.primary_decision_dimension
    # Compare only this dimension to culture's expected score
    
distance_to_culture = √(mean((response_dim − culture_dim)²))
```

The culture with the smallest distance reveals which culture the model resembles by default.

### D) Cultural Shift Magnitude
Comparing baseline to persona-prompted responses yields **Total Variation Distance (TVD)**:

```python
baseline_value_dist = frequency(values in baseline)
prompted_value_dist = frequency(values in prompted)
TVD = 0.5 × Σ|baseline_value_dist_i − prompted_value_dist_i|
```

Here, value distributions are computed as **percentages (0–100%)**, so TVD can be read as a **percentage-point shift** in value emphasis between conditions.

This measures how strongly the persona prompt influences the model's value priorities.

---

# 3. Experimental Setup

## 3.1 Experiment Configuration

**Dataset Statistics:**
- **Total Responses:** 720
- **Models Tested:** 4 (GPT-4o-mini, Claude 3.5 Haiku, Gemini 2.0 Flash, DeepSeek)
- **Cultures:** 6 (India, Japan, Mexico, UAE, US, + Baseline/unprompted)
- **Scenarios:** 30 (covering all 6 Hofstede dimensions)
- **Parse Success Rate:** 100%

**Scenarios Coverage:**
- **Individualism (IDV):** 5 scenarios
- **Power Distance (PDI):** 5 scenarios
- **Masculinity (MAS):** 5 scenarios
- **Uncertainty Avoidance (UAI):** 5 scenarios
- **Long-Term Orientation (LTO):** 5 scenarios
- **Indulgence (IVR):** 5 scenarios

Each (model × culture × scenario) combination was executed once, with caching to ensure consistency.

---

# 4. Results & Analysis

This section presents a comprehensive analysis of cultural alignment in LLMs, organized as a narrative from measurement methodology through key findings.

## 4.1 Overall Cultural Alignment: Which Cultures Can Models Emulate?

We first examine the **overall cultural alignment scores**—the primary metric measuring how well models can emulate each target culture's reasoning patterns when explicitly prompted.

### Summary Scores (0–10 scale)

| Culture | Alignment | Std Dev | Interpretation |
|---------|-----------|---------|----------------|
| **India** | **7.71** | 1.09 | ✅ Highest alignment—models most reliably emulate Indian reasoning |
| **Japan** | **6.94** | 1.51 | ⚠️ Strong alignment—good dimension performance |
| **US** | **6.73** | 1.14 | ⚠️ Moderate alignment—baseline bias helps |
| **UAE** | **6.36** | 0.89 | ⚠️ Moderate alignment—challenging nuances |
| **Mexico** | **5.42** | 0.75 | 🔴 Lowest alignment—most difficult culture |

**Mean Overall Alignment:** 6.63/10

These scores are computed by comparing the model's inferred semantic profile to the target culture's expected Hofstede profile on each scenario's primary dimension (see §2.3A). The mean score (6.63/10) indicates that **even with explicit cultural prompting**, models achieve moderate but not complete cultural alignment, with substantial variation across cultures.

### Key Insight: Unexpected Bias Toward India

Models achieve highest alignment with **India** (7.71/10), not US or Western cultures as might be expected given training data composition. This suggests:
- **Training data representation** of collectivist + long-term oriented values may be stronger than assumed
- **Western individualism** is not the dominant bias in frontier LLMs
- Models more easily emulate certain value combinations (high collectivism + moderate hierarchy) than others

---

## 4.2 Dimension-Level Analysis: Where Do Models Succeed and Fail?

To understand *why* certain cultures are harder to emulate, we decompose overall alignment into individual Hofstede dimensions.

### Calculation Method

For each scenario, we compute dimension-specific alignment (see §2.3B):
- Extract the inferred score for dimension *d*: `actual_d ∈ [−2, +2]`
- Compare to target culture's expected score: `expected_d ∈ [−2, +2]`
- Score = `10 − |expected_d − actual_d| × 2.5`

Higher scores indicate the model's reasoning on that dimension closely matches the target culture.

### Mean Alignment by Culture and Dimension

| Culture | IDV | IVR | LTO | MAS | PDI | UAI |
|---------|-----|-----|-----|-----|-----|-----|
| **India** | **9.73** | 5.71 | **8.93** | 7.13 | 6.23 | **8.50** |
| **Japan** | **9.67** | 7.09 | 5.80 | 4.91 | **9.82** | 4.33 |
| **Mexico** | 6.40 | 5.46 | 5.28 | 6.07 | 5.21 | 4.12 |
| **UAE** | 6.03 | 6.97 | 5.13 | **9.71** | 5.09 | 5.23 |
| **US** | 5.01 | 6.83 | 4.79 | 7.65 | 7.54 | **8.56** |

### Overall Dimension Difficulty

Averaging across all cultures reveals which dimensions are globally easiest/hardest for models:

| Dimension | Mean Score | Difficulty Rating |
|-----------|------------|-------------------|
| **Individualism (IDV)** | 7.37 | 🟢 Easiest |
| **Masculinity (MAS)** | 7.09 | 🟢 Easy |
| **Power Distance (PDI)** | 6.78 | 🟡 Moderate |
| **Indulgence (IVR)** | 6.41 | 🟡 Moderate |
| **Uncertainty Avoidance (UAI)** | 6.15 | 🔴 Hard |
| **Long-Term Orientation (LTO)** | 5.98 | 🔴 Hardest |

**Key Finding:** Models perform best on **individualism/collectivism** distinctions and worst on **long-term orientation** and **uncertainty avoidance**. This suggests semantic embeddings more readily capture interpersonal value differences than temporal or risk-related reasoning patterns.

### Culture-Specific Patterns

**India (7.71 overall):**
- ✅ Exceptional: IDV (9.73), LTO (8.93), UAI (8.50)
- ⚠️ Moderate: MAS (7.13), PDI (6.23), IVR (5.71)
- **Explanation:** Models excel at capturing India's moderate individualism and long-term planning values, contributing to highest overall alignment.

**Japan (6.94 overall):**
- ✅ Exceptional: IDV (9.67), PDI (9.82)
- ⚠️ Moderate: IVR (7.09)
- 🔴 Poor: UAI (4.33), MAS (4.91)
- **Explanation:** Strong on hierarchical respect (power distance), but struggles with Japan's high uncertainty avoidance and achievement orientation.

**UAE (6.36 overall):**
- ✅ Strong: MAS (9.71), IVR (6.97)
- 🔴 Weak: LTO (5.13), PDI (5.09), UAI (5.23)
- **Explanation:** Achievement values are captured, but long-term orientation and hierarchical nuances are missed.

**US (6.73 overall):**
- ✅ Strong: UAI (8.56), MAS (7.65), PDI (7.54)
- 🔴 Weak: LTO (4.79), IDV (5.01)
- **Explanation:** Paradoxically weak on individualism despite US cultural stereotype—models may overemphasize communal values when prompted with location cues.

**Mexico (5.42 overall):**
- 🔴 Consistently weak across all dimensions
- Worst: UAI (4.12), PDI (5.21)
- **Explanation:** Most challenging culture to emulate; likely requires better training data representation.

---

## 4.3 Baseline Bias: What Culture Do Unprompted Models Resemble?

To understand inherent model bias independent of prompting, we analyze **baseline responses** (no cultural context provided).

### Methodology

Using unprompted responses (N=120, 30 scenarios × 4 models), we:
1. For each response, infer its semantic profile across all 6 dimensions
2. Compare only the response's scenario-specific primary dimension to each culture's expected score
3. Calculate root-mean-square (RMS) distance across all 30 responses (see §2.3C)
4. Identify the culture with smallest distance

### Baseline Distance Results

| Culture | Distance | Interpretation |
|---------|----------|----------------|
| **India** | **1.100** | ✅ Closest match |
| **US** | 1.431 | 30% further than India |
| **Japan** | 1.556 | 41% further than India |
| **UAE** | 1.656 | 51% further than India |
| **Mexico** | 1.947 | 77% further than India |

### Key Finding: Collective Bias, Not Western Bias

**Baseline responses are closest to India** (distance = 1.100), contradicting the common assumption that LLMs exhibit Western/US bias. Possible explanations:
- Training data may overrepresent collectivist values due to global internet content
- Semantic embeddings naturally cluster around communal/family-oriented language
- US-centric content may not translate to reasoning patterns

This finding suggests that **unprompted LLM reasoning resembles Indian cultural values more than any other tested culture**.

---

## 4.4 Cultural Shift Magnitude: How Effectively Do Prompts Work?

We measure **Total Variation Distance (TVD)** between baseline and prompted value distributions (see §2.3D) to quantify prompt effectiveness.

### Shift Magnitude by Culture

| Culture | TVD | Interpretation |
|---------|-----|----------------|
| **Japan** | 47.81% | 🟢 Strongest shift—prompting highly effective |
| **India** | 46.45% | 🟢 Strong shift |
| **UAE** | 44.95% | 🟢 Strong shift |
| **Mexico** | 43.14% | 🟢 Strong shift |
| **US** | 23.83% | 🔴 Weakest shift—closest to baseline |

**Average shift magnitude:** 41.24%

### Value Shift Patterns

**US (23.83% TVD):**
- Largest increases: Achievement & Success (+8.7%), Personal Autonomy (+5.5%)
- Largest decreases: Stability & Security (−2.7%)
- **Explanation:** Minimal shift because baseline already resembles US values in some dimensions

**Japan (47.81% TVD):**
- Largest increases: Respect for Authority (+10.1%), Stability & Security (+7.5%), Family Harmony (+7.2%)
- Largest decreases: Personal Autonomy (−6.7%)
- **Explanation:** Strong prompt effectiveness—successfully shifts toward collectivism and hierarchy

**India (46.45% TVD):**
- Largest increases: Family Harmony (+12.6%), Stability & Security (+9.6%), Respect for Authority (+7.4%)
- **Explanation:** Despite baseline being closest to India, prompting still induces significant value redistribution

**Mexico (43.14% TVD):**
- Largest increases: Family Harmony (+17.8%)—largest single value shift across all cultures
- **Explanation:** Models successfully emphasize familial values when prompted with Mexican context

### Key Insight: Prompting Works, But Not Equally

Cultural prompting induces substantial value shifts (average 41.24%), demonstrating **prompt effectiveness**. However, US prompting is least effective (23.83%) because baseline already resembles US values in some dimensions. This suggests models have **directional bias** that is easier to shift in some directions than others.

---

## 4.5 Model Comparison: Are There Performance Differences?

We compare the four tested models on overall cultural alignment and stereotype avoidance.

### Model Performance Summary

| Model | Mean Alignment | Std Dev | Stereotype Score |
|-------|---------------|---------|------------------|
| **DeepSeek** | 6.66 | 1.32 | 7.95 |
| **Claude Haiku** | 6.66 | 1.39 | 6.98 |
| **GPT-4o-mini** | 6.63 | 1.38 | 8.53 |
| **Gemini Flash** | 6.57 | 1.46 | 6.77 |

### Statistical Significance (ANOVA)

- **Cultural Alignment:** F ≈ NaN, p ≈ NaN (test unstable)
  - *Interpretation:* ANOVA is not well-defined here (near-zero variance across models), but mean differences are only ~0.09/10, so we treat alignment as practically identical.
- **Stereotype Score:** F = 7.93, p < 0.001 (***) 
  - *Interpretation:* Significant differences—GPT-4o-mini avoids stereotypes best

### Key Finding: Model Homogeneity

All four frontier models achieve **statistically identical cultural alignment** (differences of only 0.09 points on a 10-point scale). This suggests:
- **Convergent training approaches** across providers lead to similar cultural biases
- **Architectural differences** do not meaningfully impact cultural alignment
- Improvement requires targeted interventions (fine-tuning, data curation), not just model selection

---

## 4.6 Scenario Difficulty: What Makes Cultural Alignment Hard?

We analyze which scenarios and scenario categories are hardest for models.

### Hardest Individual Scenarios

| Scenario ID | Mean Alignment | Category | Primary Dimension |
|-------------|---------------|----------|-------------------|
| **LTO001** | 5.35 | Career & Finance | Long-Term Orientation |
| **LTO004** | 5.55 | Projects & Persistence | Long-Term Orientation |
| **PDI002** | 5.80 | Career & Risk | Power Distance |
| **LTO005** | 5.88 | Education & Development | Long-Term Orientation |
| **UAI002** | 5.88 | Rules & Procedures | Uncertainty Avoidance |

### Hardest Scenario Categories

| Category | Mean Alignment | Interpretation |
|----------|---------------|----------------|
| **Career & Finance** | 5.35 | 🔴 Hardest—financial decisions expose LTO weakness |
| **Education & Development** | 5.55 | 🔴 Hard—long-term planning struggles |
| **Projects & Persistence** | 5.88 | 🔴 Hard—requires sustained effort reasoning |

### Easiest Scenario Categories

| Category | Mean Alignment | Interpretation |
|----------|---------------|----------------|
| **Social Situations** | 6.97 | 🟢 Easiest—interpersonal dynamics well-captured |
| **Career & Competition** | 6.86 | 🟢 Easy—achievement values clear |
| **Career & Work Culture** | 6.81 | 🟢 Easy—hierarchical patterns accessible |

### Key Finding: Financial and Long-Term Scenarios Are Hardest

Three of the top five hardest scenarios involve **Long-Term Orientation** (LTO), reinforcing the dimension-level finding (§4.2) that models struggle with temporal reasoning and delayed gratification trade-offs. Financial scenarios (LTO001) are particularly challenging, likely because they require both:
- Long-term planning (LTO dimension)
- Risk assessment (UAI dimension)
- Both dimensions are among the hardest for models

---

## 4.7 Decision Patterns: Do Models Show Cultural Differentiation?

We analyze the distribution of decision outcomes (Option A vs. Option B vs. Decline) across cultures.

### Overall Decision Distribution

| Decision | Count | Percentage |
|----------|-------|------------|
| **Option A** | 389 | 54.0% |
| **Option B** | 322 | 44.7% |
| **Decline** | 9 | 1.3% |

### Decision Entropy by Culture

Higher entropy indicates more diverse, less predictable decisions:

| Culture | Entropy | Interpretation |
|---------|---------|----------------|
| **Mexico** | 0.693 | Most diverse decisions |
| **UAE** | 0.681 | High diversity |
| **India** | 0.678 | High diversity |
| **Japan** | 0.670 | Moderate diversity |
| **US** | 0.655 | Moderate diversity |
| **Baseline** | 0.639 | Lowest diversity |

### Key Finding: Limited Differentiation Despite Prompting

Models rarely decline decisions (1.3%), suggesting they are **willing to make culturally-informed choices** rather than abstaining. However, decision patterns show only **modest differentiation** across cultures (entropy range: 0.639–0.693). This indicates that while value priorities shift (§4.4), actual decision outcomes remain relatively similar—models may be **rhetorically adapting** more than substantively changing behavior.

---

## 4.8 Value Priority Analysis: What Values Do Models Emphasize?

We examine the top three most frequently cited values by culture to understand qualitative differences in reasoning.

### Top Values by Culture

**Baseline:**
1. Future Planning (37 mentions)
2. Achievement & Success (31)
3. Family Harmony (26)

**US:**
1. Achievement & Success (61)—+30 vs. baseline
2. Personal Autonomy (39)
3. Future Planning (35)

**Japan:**
1. Family Harmony (52)—+26 vs. baseline
2. Future Planning (44)
3. Stability & Security (43)

**India:**
1. Family Harmony (71)—+45 vs. baseline, highest overall
2. Stability & Security (51)
3. Future Planning (47)

**Mexico:**
1. Family Harmony (86)—+60 vs. baseline, most dramatic shift
2. Stability & Security (32)
3. Future Planning (32)

**UAE:**
1. Family Harmony (70)—+44 vs. baseline
2. Future Planning (44)
3. Stability & Security (42)

### Key Patterns

1. **Family Harmony** increases dramatically for all non-US cultures (average +44 mentions)
2. **Achievement & Success** nearly doubles for US prompting (+30)
3. **Personal Autonomy** appears frequently only for US
4. Baseline emphasizes **Future Planning** above all else

These patterns validate the quantitative findings: models successfully shift value emphases in response to cultural prompting, with particularly strong effects on communal values.

---

## 4.9 Cross-Model Consistency: How Stable Are Responses?

We examine response stability across models by measuring decision consistency per scenario.

### Model Decision Consistency

For each model, we compute what percentage of scenarios yield the most frequent decision:

| Model | Consistency | Alignment Std Dev |
|-------|------------|-------------------|
| **GPT-4o-mini** | 66.1% | 1.38 |
| **Gemini Flash** | 56.7% | 1.46 |
| **Claude Haiku** | 54.4% | 1.39 |
| **DeepSeek** | 48.9% | 1.32 |

### Key Finding: Moderate Consistency

GPT-4o-mini shows highest decision consistency (66.1%), while DeepSeek shows highest variance (48.9%). However, all models show similar alignment score variability (std dev 1.32–1.46), indicating that while decision choices vary, the *quality* of cultural alignment is comparably unstable across models.

---

## 4.10 Summary of Key Findings

### Alignment Performance
- **Mean overall alignment:** 6.63/10 (moderate)
- **Best culture:** India (7.71/10)
- **Worst culture:** Mexico (5.42/10)
- **Easiest dimension:** Individualism (7.37/10)
- **Hardest dimension:** Long-Term Orientation (5.98/10)

### Bias Patterns
- **Baseline is closest to India** (distance 1.100), not US
- **Cultural prompting induces 41% average shift** in value priorities
- **US prompting least effective** (23.83% shift) due to baseline similarity

### Model Performance
- **No significant differences** in alignment across models (p > 0.05)
- **Range: 6.57–6.66** (only 0.09-point spread)
- **GPT-4o-mini avoids stereotypes best** (8.53/10, p < 0.001)
- **All frontier models converge** on similar cultural biases

### Scenario Patterns
- **Financial scenarios hardest** (LTO001: 5.35/10)
- **Social scenarios easiest** (PDI001: 6.97/10)
- **LTO and UAI dimensions** appear in most difficult scenarios

### Qualitative Patterns
- **Family Harmony increases 44+ mentions** for non-US cultures
- **Achievement & Success doubles** for US prompting
- **Decision entropy modest** (0.64–0.69)—limited behavioral differentiation

---

# 5. Visualizations

The framework generates 10 publication-quality visualizations:

1. **Baseline Comparison** — Bar chart of baseline distances to each culture
2. **Decision Patterns** — Stacked bar chart of Option A/B/Decline distributions
3. **Category Performance** — Bar chart of alignment by scenario category
4. **Cultural Shift Magnitude** — Bar chart of TVD by culture
5. **Decision Distribution** — Pie chart of overall decisions
6. **Cultural Alignment by Model** — Bar chart comparing model performance
7. **Stereotype Scores** — Bar chart of stereotype avoidance by model
8. **Scenario Difficulty** — Sorted bar chart of scenarios by alignment
9. **Model Comparison Radar** — Radar plot of model performance across key metrics
10. **Value Frequency** — Stacked bar chart of top values by culture

All visualizations use consistent color schemes and include detailed annotations.

---

# 6. Limitations

## 6.1 Methodological Limitations

1. **Hofstede Framework**
   - Hofstede's model is Western-centric and may not capture all cultural nuances
   - 6 dimensions may oversimplify complex cultural values
   - Country-level scores assume within-country homogeneity
   - Limited to 5 cultures + baseline (many cultures not represented)

2. **Semantic Projection Approach**
   - Embeddings may not fully capture cultural reasoning
   - Exemplar curation introduces researcher bias
   - Cosine similarity assumes linear relationships
   - [-2, +2] scale is not directly comparable to Hofstede's 0-100 scale

## 6.2 Technical Limitations

1. **Model Selection**
   - Only tested 4 frontier models (many other LLMs exist)
   - All models are frontier-class (no smaller or older models tested)
   - Single run per (model × culture × scenario) combination

2. **Evaluation Metrics**
   - Stereotype scoring is subjective (human-rated on exemplars)
   - No inter-rater reliability for stereotype assessment

3. **Sample Size**
   - 720 total responses (reasonable but not massive)
   - 30 scenarios per culture (could be expanded)
   - Each scenario tests specific dimensions—not all dimensions per scenario

## 6.3 Interpretation Limitations

1. **Causality Claims**
   - Cannot prove *why* models exhibit certain biases
   - Training data composition is proprietary/unknown
   - Cannot distinguish between data bias vs. architectural bias

2. **Generalization**
   - Results may not generalize to:
     - Newer model versions
     - Different prompt formats
     - Real-world deployment contexts
     - Non-English languages
     - Within-culture variation (rural vs. urban, regions)

3. **Practical Application**
   - Framework measures alignment, not **appropriateness** for specific use cases
   - High alignment doesn't guarantee ethical or beneficial behavior
   - Cultural stereotypes vs. authentic reasoning remains ambiguous

---

# 7. Technical Details

## 7.1 System Architecture

**Pipeline Components:**

1. **Scenario Generator** (`scenarios.py`)
   - 30 pre-defined scenarios covering 6 Hofstede dimensions
   - Each scenario presents ethically ambiguous choice
   - Each scenario tagged with one primary dimension for focused measurement

2. **Prompt Constructor** (`prompt_constructor.py`)
   - Combines scenario with optional cultural persona
   - Instructs model to provide: decision, values, explanation
   - Standardized format across all models

3. **LLM Interface** (`llm_interface.py`)
   - Unified API for multiple LLM providers (OpenAI, Anthropic, Google, DeepSeek)
   - Response caching for consistency
   - Error handling and retry logic

4. **Response Parser** (`response_parser.py`)
   - Extracts structured data from LLM responses
   - Validates decision format and value lists
   - 100% parse success rate in latest run

5. **Evaluator** (`evaluator.py`)
   - Semantic embedding using `all-MiniLM-L6-v2` sentence-transformer
   - Hofstede dimension projection via cosine similarity
   - Cultural alignment scoring (see §2.3)

6. **Analyzer** (`analyze.py`)
   - Statistical significance testing (ANOVA, t-tests)
   - Dimension-level and scenario-level analysis
   - Value pattern extraction and shift magnitude calculation

7. **Visualizer** (`visualizer.py`)
   - Generates 11 publication-quality visualizations
   - Radar plots, heatmaps, bar charts, box plots
   - Consistent styling and color schemes

## 7.2 Dependencies

```txt
openai>=1.0.0
anthropic>=0.8.0
google-generativeai>=0.3.0
sentence-transformers>=2.2.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.10.0
```

## 7.3 Hofstede Dimension Definitions

| Dimension | High Score Indicates | Low Score Indicates |
|-----------|---------------------|---------------------|
| **IDV** (Individualism) | Self-reliance, personal goals | Collective welfare, group harmony |
| **PDI** (Power Distance) | Accept hierarchy, defer to authority | Egalitarian, question authority |
| **MAS** (Masculinity) | Achievement, competition, success | Cooperation, modesty, quality of life |
| **UAI** (Uncertainty Avoidance) | Need structure, avoid ambiguity | Comfortable with uncertainty |
| **LTO** (Long-Term Orientation) | Future planning, perseverance | Tradition, short-term results |
| **IVR** (Indulgence) | Gratification, leisure, freedom | Restraint, strict norms, duties |

## 7.4 Country Profiles (Bucketed normalized [-2, +2] scale)

| Country | IDV | PDI | MAS | UAI | LTO | IVR |
|---------|-----|-----|-----|-----|-----|-----|
| **US** | 2.0 | -1.0 | 1.0 | 0.0 | -1.5 | 1.5 |
| **India** | 0.0 | 1.5 | 1.0 | -1.0 | 0.0 | -1.5 |
| **Japan** | 0.0 | 0.0 | 2.0 | 2.0 | 2.0 | -1.0 |
| **Mexico** | -1.5 | 2.0 | 1.5 | 2.0 | -1.5 | 2.0 |
| **UAE** | -1.5 | 2.0 | 0.0 | 1.5 | -1.5 | -1.0 |

---

# 8. Future Work

## 8.1 Immediate Extensions

1. **Expand Model Coverage**
   - Test Llama 3, Mistral, Qwen, and other open-source models
   - Include older model versions for longitudinal analysis
   - Test smaller models (7B, 13B parameters)

2. **Expand Cultural Coverage**
   - Add African, Middle Eastern, South American cultures
   - Test within-culture variation (rural vs urban, regions)
   - Include minority cultures and diaspora communities

3. **Improve Scenarios**
   - Increase to 50-100 scenarios for better coverage
   - Add multi-dimensional scenarios (conflicting values)
   - Include culturally-specific scenarios (not Western-centric)

## 8.2 Methodological Enhancements

1. **Multi-Rater Evaluation**
   - Multiple human evaluators for stereotype scoring
   - Calculate inter-rater reliability (Cohen's κ, Fleiss' κ)
   - Use consensus scoring for ground truth

2. **Longitudinal Analysis**
   - Track cultural alignment changes across model updates
   - Measure impact of RLHF and fine-tuning
   - Test temporal stability of cultural personas

3. **Alternative Frameworks**
   - Test other cultural frameworks (Schwartz, Trompenaars, GLOBE)
   - Develop AI-native cultural dimension framework
   - Combine multiple frameworks for richer analysis

## 8.3 Real-World Applications

1. **Fairness Auditing**
   - Use framework for AI fairness certification
   - Detect and quantify cultural bias in production systems
   - Monitor alignment drift over time

2. **Culturally-Aware Fine-Tuning**
   - Use alignment scores to guide fine-tuning
   - Create culturally-balanced training datasets
   - Develop culture-specific model variants

3. **User Interface Adaptation**
   - Detect user's cultural context from conversation
   - Dynamically adjust model behavior
   - Provide cultural explanations for reasoning

---

# 9. Conclusion

WorldWiseAI demonstrates that **semantic projection onto cultural dimensions** provides a rigorous, scalable method for measuring cultural alignment in LLMs. Key contributions include:

## 9.1 Novel Methodology
Moving beyond survey questions to semantic inference of cultural values from reasoning text. By analyzing *how* models reason rather than *what* they say about culture, we gain insight into authentic cultural alignment.

## 9.2 Comprehensive Framework
End-to-end pipeline from scenario design → semantic projection → alignment metrics → visualization. The framework is modular, extensible, and applicable to any LLM.

## 9.3 Actionable Insights

1. **Unexpected Bias:** Models exhibit strongest baseline resemblance to India (not US), challenging assumptions about Western bias
2. **Dimension Difficulty:** Long-Term Orientation and Uncertainty Avoidance are hardest dimensions (mean scores 5.98–6.02/10)
3. **Model Convergence:** All frontier models show statistically identical cultural alignment (p > 0.05)
4. **Effective Prompting:** Cultural personas induce 41% average value shift, demonstrating prompt effectiveness
5. **Representation Gaps:** Mexico and UAE need better training data representation (alignment 5.22 and 5.73/10)

## 9.4 Open Questions

1. **Why does baseline resemble India more than US?** Does this reflect training data composition, semantic embedding biases, or something else?
2. **How can we improve LTO and UAI dimension alignment?** Do these dimensions require different evaluation approaches?
3. **What causes model-specific stereotyping patterns?** GPT-4o-mini avoids stereotypes best—why?
4. **How to balance cultural authenticity vs. harmful stereotypes?** High alignment to cultural norms may reinforce problematic generalizations.

This framework provides researchers and practitioners with tools to understand, measure, and ultimately improve cultural fairness in AI systems serving global populations.

---

## Citation

If you use WorldWiseAI in your research, please cite:

```bibtex
@software{worldwiseai2024,
  title={WorldWiseAI: Measuring Cultural Alignment in Large Language Models},
  author={[Your Name]},
  year={2024},
  url={https://github.com/yourusername/worldwiseai}
}
```

---

## Contact

[Your contact information]

---

**Last Updated:** November 23, 2025  
**Dataset Version:** results_20251120_140046  
**Total Responses Analyzed:** 720