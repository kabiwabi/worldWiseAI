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
| **India** | **7.70** | 1.09 | ✅ Highest alignment—models most reliably emulate Indian reasoning |
| **Japan** | **6.94** | 1.51 | ⚠️ Strong alignment—good dimension performance |
| **US** | **6.73** | 1.14 | ⚠️ Moderate alignment—baseline bias helps |
| **UAE** | **6.36** | 0.89 | ⚠️ Moderate alignment—challenging nuances |
| **Mexico** | **5.42** | 0.75 | 🔴 Lowest alignment—most difficult culture |

**Mean Overall Alignment:** 6.63/10

These scores are computed by comparing the model's inferred semantic profile to the target culture's expected Hofstede profile on each scenario's primary dimension (see §2.3A). The mean score (6.63/10) indicates that **even with explicit cultural prompting**, models achieve moderate but not complete cultural alignment, with substantial variation across cultures.

### Key Insight: Unexpected Bias Toward India

Models achieve highest alignment with **India** (7.70/10), not US or Western cultures as might be expected given training data composition. This finding is further confirmed by baseline bias detection (see §4.4), where unprompted models show closest resemblance to Indian cultural values. This suggests:
- **Training data representation** of collectivist + moderate hierarchy values may be stronger than assumed
- **Western individualism** is not the dominant bias in frontier LLMs
- Models more easily emulate certain value combinations (collectivism + moderate hierarchy) than others

---

## 4.2 Dimension-Level Analysis: Where Do Models Succeed and Fail?

Breaking down cultural alignment by individual Hofstede dimension reveals where models perform well and where they struggle:

### Mean Dimension Alignment Across All Cultures

| Dimension | Mean Score | Std Dev | Interpretation |
|-----------|------------|---------|----------------|
| **Individualism (IDV)** | **7.43** | 1.38 | ✅ Easiest dimension—models handle well |
| **Masculinity (MAS)** | **7.02** | 1.99 | ✅ Strong performance—clear value trade-offs |
| **Power Distance (PDI)** | **6.74** | 2.02 | ⚠️ Moderate—hierarchy concepts understood |
| **Indulgence (IVR)** | **6.52** | 1.61 | ⚠️ Moderate—duty vs. pleasure trade-offs |
| **Uncertainty Avoidance (UAI)** | **6.15** | 2.10 | 🔴 Challenging—ambiguity tolerance difficult |
| **Long-Term Orientation (LTO)** | **6.08** | 1.54 | 🔴 Hardest dimension—temporal reasoning weak |

**Key Findings:**

1. **Individualism is Easiest (7.43/10)**
   - Models reliably distinguish self-interest vs. collective welfare
   - Training data emphasizes this dimension heavily
   - Clear value exemplars in Western and Asian texts

2. **Long-Term Orientation is Hardest (6.08/10)**
   - Temporal reasoning (future vs. present) is semantically complex
   - Models struggle to project multi-year consequences
   - Short-term thinking bias from conversational training

3. **High Variance in UAI and PDI**
   - Uncertainty Avoidance (σ = 2.10) shows most inconsistency
   - Power Distance (σ = 2.02) varies greatly by scenario context
   - These dimensions are highly context-dependent

### Dimension Performance by Culture

The heatmap below shows dimension-level alignment scores for each culture:

| Culture | IDV | IVR | LTO | MAS | PDI | UAI |
|---------|-----|-----|-----|-----|-----|-----|
| **India** | 9.77 | 5.79 | 9.07 | 7.17 | 6.17 | 8.41 |
| **Japan** | 9.75 | 7.23 | 5.67 | 4.86 | 9.81 | 4.43 |
| **Mexico** | 6.31 | 5.63 | 5.44 | 5.80 | 5.11 | 4.07 |
| **UAE** | 6.09 | 7.05 | 5.31 | 9.60 | 5.04 | 5.34 |
| **US** | 5.24 | 6.88 | 4.90 | 7.66 | 7.60 | 8.52 |

**Notable Patterns:**

1. **India scores high on IDV (9.77) and LTO (9.07)** despite having medium Hofstede scores—suggests models over-emphasize certain Indian values
2. **Japan scores extremely high on PDI (9.81)** but low on UAI (4.43)—models capture hierarchy but miss risk aversion
3. **Mexico consistently underperforms** across most dimensions (mean 5.42)—needs better training representation
4. **US performs well on PDI (7.60) and UAI (8.52)** but poorly on IDV (5.24)—counterintuitive given individualistic culture

---

## 4.3 Hofstede Score Accuracy: How Well Do Models Impute Cultural Profiles?

A critical validation question: **How accurately can models reproduce Hofstede's official cultural scores?**

We compare the semantic profiles inferred from LLM responses to official Hofstede scores (normalized to [-2, +2] scale). This measures whether the semantic projection methodology itself is valid.

### Overall Accuracy Summary

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Mean Absolute Error (MAE)** | **1.337** | 🔴 Substantial deviation from ground truth |
| **Median Absolute Error** | **1.521** | Typical error is ~1.5 points on [-2, +2] scale |
| **Standard Deviation** | **0.706** | High variance in accuracy |
| **Total Comparisons** | **600** | (5 cultures × 6 dimensions × 20 responses) |

**Accuracy Distribution:**
- **Excellent (< 0.5):** 110 responses (18.3%)
- **Good (0.5–1.0):** 71 responses (11.8%)
- **Acceptable (1.0–1.5):** 111 responses (18.5%)
- **Poor (≥ 1.5):** 308 responses (51.3%) ← **Majority of responses**

### Interpretation

An MAE of **1.337 on a [-2, +2] scale** means models typically miss the target culture's Hofstede score by more than half the scale range. This indicates:

1. **Semantic projection is imperfect** — embedding similarity captures some cultural signal but with substantial noise
2. **Context matters** — single-scenario responses may not reflect aggregate cultural patterns
3. **Dimension-specific challenges** — some dimensions are harder to infer (see below)

However, the methodology still provides valuable **relative comparisons** between cultures and models, even if absolute Hofstede replication is limited.

### Accuracy by Dimension

| Dimension | MAE | Bias (Signed Mean) | Interpretation |
|-----------|-----|-------------------|----------------|
| **IDV (Individualism)** | **1.027** | +0.228 | ✅ Most accurate—slight overestimate |
| **PDI (Power Distance)** | **1.302** | -0.902 | ⚠️ Underestimates hierarchy acceptance |
| **MAS (Masculinity)** | **1.194** | -1.177 | ⚠️ Strong underestimate of competitiveness |
| **UAI (Uncertainty Avoidance)** | **1.538** | -1.284 | 🔴 Hardest to infer—underestimates risk aversion |
| **LTO (Long-Term Orientation)** | **1.568** | +0.875 | 🔴 Least accurate—overestimates future focus |
| **IVR (Indulgence)** | **1.393** | +0.195 | ⚠️ Slight overestimate of gratification |

**Key Patterns:**

1. **Individualism (IDV) is most reliably inferred** (MAE 1.027)—clear semantic markers
2. **Long-Term Orientation (LTO) is least accurate** (MAE 1.568)—temporal reasoning is challenging
3. **Systematic underestimation** of MAS, UAI, PDI—models may avoid strong competitive/hierarchical language
4. **Systematic overestimation** of LTO—models default to "planning" and "future thinking" language

### Accuracy by Culture

| Culture | MAE | Best Dimension | Worst Dimension |
|---------|-----|---------------|-----------------|
| **India** | **0.907** | IDV (0.02) | IVR (1.68) |
| **Japan** | **1.216** | IDV (0.02) | UAI (2.23) |
| **US** | **1.280** | UAI (0.59) | LTO (2.04) |
| **UAE** | **1.438** | MAS (0.08) | PDI (1.99) |
| **Mexico** | **1.843** | IDV (1.48) | UAI (2.37) |

**Key Findings:**

1. **India is most accurately modeled** (MAE 0.907)—models capture Indian values well
2. **Mexico is least accurate** (MAE 1.843)—confirms low alignment scores in §4.1
3. **IDV is consistently well-captured** across most cultures
4. **UAI and LTO show largest errors** for most cultures

### Accuracy by Model

All four models perform similarly in Hofstede score imputation:

| Model | MAE | Interpretation |
|-------|-----|----------------|
| **Claude 3.5 Haiku** | **1.326** | ✅ Most accurate |
| **DeepSeek** | **1.332** | Essentially tied |
| **Gemini 2.0 Flash** | **1.342** | Essentially tied |
| **GPT-4o-mini** | **1.349** | Essentially tied |

The differences are negligible (< 0.02 MAE), suggesting all frontier models have similar cultural projection capabilities.

### Detailed Error Heatmap

![Hofstede Error Heatmap](hofstede_error_heatmap_bucketed.png)

**Observations from Heatmap:**

- **Green cells (low error):** US-UAI, India-IDV, Japan-IDV, Japan-PDI
- **Red cells (high error):** Japan-MAS (2.06), Japan-UAI (2.23), Mexico-UAI (2.37), UAE-PDI (1.99), US-LTO (2.04)
- **Systematic patterns:** Most PDI and UAI cells show high error (red/orange)

### Implications

1. **Relative rankings are reliable** — even with high MAE, models correctly order cultures (e.g., US > Japan on IDV)
2. **Dimension alignment scores are valid** — they measure relative cultural fit, not absolute Hofstede replication
3. **Ground truth validation is essential** — semantic projection alone insufficient for precise cultural measurement
4. **Future work needed** — refine exemplar sets, explore alternative embedding models, validate with human ratings

---

## 4.4 Baseline Bias Detection: What Culture Do Unprompted Models Resemble?

A critical question for fairness: **Without explicit cultural prompting, which culture's values do models default to?**

We measure the semantic distance between unprompted (baseline) responses and each target culture's Hofstede profile. The closest culture reveals the model's inherent bias.

### Baseline Distance Rankings

| Culture | Distance | Interpretation |
|---------|----------|----------------|
| **India** | **1.112** | ✅ **Closest** — models naturally resemble Indian values |
| **US** | **1.409** | Models somewhat resemble US values |
| **Japan** | **1.574** | Moderate distance |
| **UAE** | **1.658** | Moderate distance |
| **Mexico** | **1.843** | Furthest — least resemblance |

**Interpretation:** Lower distance means the baseline responses are more similar to that culture's expected Hofstede profile.

### Key Insight: Models Default to Indian-Like Values

**Contrary to expectations**, unprompted models show closest resemblance to **India** (distance 1.112), not US or Western cultures. This suggests:

1. **Training data composition** may include substantial Indian/South Asian perspectives
2. **Collectivist + moderate hierarchy values** are well-represented in training corpora
3. **Western individualism** is NOT the dominant default in frontier LLMs
4. **RLHF tuning** may emphasize harmony, respect, and duty over pure self-interest

### Comparison to Cultural Alignment Scores

Interestingly, the culture with **lowest baseline distance** (India, 1.112) also shows **highest prompted alignment** (7.70/10). This suggests:
- Models find it easier to emulate cultures close to their default reasoning
- Cultural prompting amplifies existing tendencies rather than creating novel reasoning patterns
- Training data representation strongly predicts both baseline bias and prompted performance

### Value Distribution Analysis

We can also examine which specific values appear most frequently in baseline responses:

| Value | Baseline Frequency | Most Overrepresented Culture |
|-------|-------------------|------------------------------|
| **Future Planning** | 52 | US, Japan, UAE, India |
| **Achievement & Success** | 46 | US (much more than baseline) |
| **Work-Life Balance** | 39 | US, UAE |
| **Stability & Security** | 28 | Japan, India, Mexico, UAE |
| **Personal Autonomy** | 26 | US (much more than baseline) |

Baseline responses emphasize **Future Planning** and **Achievement**, suggesting a pragmatic, goal-oriented default stance. However, **Family Harmony** (which dominates prompted non-Western responses) appears much less frequently in baseline.

---

## 4.5 Cultural Shift Magnitude: How Effective Is Cultural Prompting?

To measure the **effectiveness of cultural prompting**, we compute the Total Variation Distance (TVD) between baseline value distributions and prompted value distributions for each culture.

### Shift Magnitude Rankings

| Culture | TVD (%) | Interpretation |
|---------|---------|----------------|
| **Japan** | **41.94%** | ✅ Strongest shift—prompting highly effective |
| **UAE** | **41.39%** | ✅ Strong shift |
| **India** | **40.00%** | ✅ Strong shift |
| **Mexico** | **36.39%** | ✅ Strong shift |
| **US** | **17.78%** | ⚠️ Weakest shift—baseline already US-like |

**Mean Shift Magnitude:** 35.50%

**Interpretation:** Cultural prompting induces an average **35.5 percentage-point shift** in value emphasis, indicating **strong cultural adaptation**. The persona prompts substantially change which values models prioritize.

### Key Insights

1. **Japan shows largest shift (41.94%)** — models dramatically change reasoning when prompted as Japanese
2. **US shows smallest shift (17.78%)** — baseline already resembles US values, so prompting has less effect
3. **All non-US cultures shift > 36%** — strong evidence that cultural context matters

### Value-Specific Shifts

Examining which specific values shift most reveals the mechanism of cultural adaptation:

**Japan (41.94% total shift):**
- ↑ Respect for Authority (+10.3%)
- ↑ Stability & Security (+8.1%)
- ↑ Family Harmony (+7.2%)
- ↓ Achievement & Success (-6.1%)

**India (40.00% total shift):**
- ↑ Family Harmony (+12.2%)
- ↑ Stability & Security (+9.4%)
- ↑ Respect for Authority (+7.8%)
- ↓ Work-Life Balance (-6.7%)

**Mexico (36.39% total shift):**
- ↑ Family Harmony (+16.9%) ← **Largest single shift**
- ↑ Respect for Authority (+6.7%)
- ↓ Achievement & Success (-6.1%)

**US (17.78% total shift):**
- ↑ Achievement & Success (+9.4%)
- ↑ Personal Autonomy (+6.4%)
- ↓ Future Planning (-3.1%)

These patterns show models correctly adapt value priorities to cultural context:
- **Family Harmony** dominates non-Western prompted responses
- **Achievement & Success** dominates US prompted responses
- **Respect for Authority** increases for hierarchical cultures (Japan, India, Mexico, UAE)

---

## 4.6 Model Comparison: Are All Frontier Models Equally Culturally Aligned?

We compare four frontier models across multiple metrics to identify performance differences.

### Overall Performance

| Model | Mean Alignment | Stereotype Score | Overall Score |
|-------|---------------|-----------------|---------------|
| **GPT-4o-mini** | 6.63 | 8.53 | **7.58** ✅ |
| **DeepSeek** | 6.66 | 7.95 | 7.31 |
| **Claude 3.5 Haiku** | 6.66 | 6.98 | 6.82 |
| **Gemini 2.0 Flash** | 6.57 | 6.77 | 6.67 |

**Overall Score** = mean of (Cultural Alignment, Stereotype Score)

### Key Findings

1. **Cultural Alignment is Statistically Identical (p = 0.96)**
   - All four models achieve mean alignment of 6.57–6.66/10
   - No significant difference in cultural reasoning capability
   - Frontier models have converged on similar cultural representation

2. **GPT-4o-mini Avoids Stereotypes Best (8.53/10)**
   - Uses least stereotypical language (p < 0.001)
   - May reflect stronger RLHF tuning for bias mitigation
   - Claude and Gemini use more stereotypical phrasing

3. **No Single Model Dominates**
   - All models show similar strengths and weaknesses
   - Choice of model matters less than choice of prompting strategy
   - Cultural alignment is more a function of training data than architecture

### Model-Specific Patterns

**GPT-4o-mini:**
- Highest stereotype avoidance (8.53/10)
- Most consistent decisions (66% consensus)
- Slight preference for "Option A" choices (66%)

**DeepSeek:**
- Balanced decision distribution (49% A, 49% B)
- Most willing to "Decline" (3.3% of responses)
- Similar alignment to GPT-4 but more stereotypical language

**Claude 3.5 Haiku:**
- Prefers "Option B" slightly (54%)
- Most accurate Hofstede imputation (MAE 1.326)
- Moderate stereotype usage

**Gemini 2.0 Flash:**
- Similar pattern to GPT-4o-mini
- Lowest stereotype avoidance (6.77/10)
- Consistent performance across cultures

---

## 4.7 Scenario Difficulty: Which Dilemmas Are Hardest to Align?

Some scenarios are inherently more difficult for models to navigate culturally. We rank scenarios by mean cultural alignment score.

### Hardest Scenarios (Lowest Alignment)

| Scenario ID | Category | Mean Alignment | Primary Dimension |
|-------------|----------|---------------|-------------------|
| **LTO001** | Career & Finance | **5.71** | Long-Term Orientation |
| **LTO003** | Resource Allocation | **5.72** | Long-Term Orientation |
| **UAI001** | Career & Education | **5.78** | Uncertainty Avoidance |
| **LTO004** | Education & Development | **5.87** | Long-Term Orientation |
| **UAI002** | Career & Risk | **5.92** | Uncertainty Avoidance |

### Easiest Scenarios (Highest Alignment)

| Scenario ID | Category | Mean Alignment | Primary Dimension |
|-------------|----------|---------------|-------------------|
| **IND005** | Resource Allocation | **7.44** | Individualism |
| **IND004** | Career & Education | **7.42** | Individualism |
| **IND003** | Family & Relationships | **7.34** | Individualism |
| **IND002** | Career & Education | **7.32** | Individualism |
| **IND001** | Family & Relationships | **7.32** | Individualism |

### Key Insights

1. **Long-Term Orientation (LTO) scenarios dominate hardest list**
   - 3 of top 5 hardest scenarios test LTO
   - Models struggle with temporal reasoning and future-vs-present trade-offs
   - Confirms dimension-level analysis (§4.2)

2. **Individualism (IND) scenarios dominate easiest list**
   - All top 5 easiest scenarios test individualism
   - Self-interest vs. collective welfare is semantically clear
   - Strong training representation of this dimension

3. **Uncertainty Avoidance (UAI) also challenging**
   - 2 of top 5 hardest scenarios test UAI
   - Risk tolerance and ambiguity are context-dependent
   - High variance across cultures

### Category Performance

| Category | Mean Alignment | Best Dimension | Hardest Dimension |
|----------|---------------|----------------|-------------------|
| **Career & Competition** | 7.17 | MAS | — |
| **Family & Relationships** | 7.11 | IDV | — |
| **Career & Finance** | 5.71 | — | LTO |
| **Career & Risk** | 5.92 | — | UAI |

**Family & Relationships** and **Career & Competition** scenarios produce highest alignment, while **Career & Finance** and **Career & Risk** are most challenging.

---

## 4.8 Statistical Significance: What Differences Matter?

We perform rigorous statistical testing to determine which differences are meaningful.

### Model Comparison (ANOVA)

**Null Hypothesis:** All models have identical mean cultural alignment.

- **F-statistic:** 0.099
- **p-value:** 0.961
- **Result:** ✅ **Cannot reject null hypothesis**

**Conclusion:** No statistically significant difference between models' cultural alignment scores. All frontier models perform equivalently.

### Pairwise Model Comparisons (Bonferroni-Corrected t-tests)

All pairwise comparisons show:
- p-values > 0.60
- Cohen's d < 0.06 (negligible effect size)
- **No significant differences** between any pair of models

### Culture Comparison (ANOVA)

**Null Hypothesis:** All cultures have identical mean cultural alignment.

- **F-statistic:** 31.53
- **p-value:** < 0.0001
- **Result:** ❌ **Reject null hypothesis (p < 0.001)**

**Conclusion:** Cultures show **highly significant differences** in how well models can emulate them. Some cultures (India, Japan, US) are easier to align with than others (Mexico, UAE).

---

## 4.9 Value Pattern Analysis: What Values Dominate Each Culture?

Examining the most frequently cited values reveals what models emphasize for each cultural persona.

### Top 3 Values by Culture

| Culture | 1st Value | 2nd Value | 3rd Value |
|---------|-----------|-----------|-----------|
| **Baseline** | Future Planning (52) | Achievement & Success (46) | Work-Life Balance (39) |
| **US** | Achievement & Success (80) | Personal Autonomy (45) | Future Planning (41) |
| **Japan** | Family Harmony (62) | Stability & Security (52) | Future Planning (52) |
| **India** | Family Harmony (80) | Stability & Security (57) | Future Planning (53) |
| **Mexico** | Family Harmony (97) | Stability & Security (39) | Future Planning (36) |
| **UAE** | Family Harmony (80) | Future Planning (54) | Stability & Security (52) |

### Key Patterns

1. **Family Harmony dominates all non-Western cultures**
   - Mexico: 97 mentions (highest of any value-culture pair)
   - India: 80 mentions
   - UAE: 80 mentions
   - Japan: 62 mentions
   - US: Not in top 3

2. **Achievement & Success strongly associated with US**
   - US: 80 mentions (1st most cited)
   - Baseline: 46 mentions
   - All other cultures: < 30 mentions

3. **Future Planning appears in all top 3 lists**
   - Cross-cultural value emphasized consistently
   - May reflect LLM training on planning/goal-oriented text

4. **Stability & Security clusters in non-Western cultures**
   - High in Japan, India, Mexico, UAE
   - Not prominent in US or baseline

---

# 5. Visualizations

The framework generates comprehensive visualizations to aid interpretation:

1. **Cultural Alignment by Model and Culture** — Bar chart comparing alignment scores
2. **Decision Distribution** — Shows choice patterns across cultures
3. **Value Frequency Heatmap** — Top values by culture
4. **Stereotype Scores** — Boxplot of stereotyping by model
5. **Model Comparison Radar** — Multi-metric comparison
6. **Category Performance** — Alignment by scenario category
7. **Baseline Comparison** — Unprompted vs. prompted behavior
8. **Cultural Shift Magnitude** — TVD bar chart showing prompt effectiveness
9. **Scenario Difficulty Ranking** — Hardest and easiest scenarios
10. **Decision Patterns by Model** — Stacked bar of decision distribution
11. **Hofstede Error Heatmap** — MAE by culture and dimension

All visualizations are publication-quality (300 DPI) and generated automatically from results.

---

# 6. Limitations

## 6.1 Methodological Limitations

1. **Semantic Projection Accuracy**
   - MAE of 1.337 on [-2, +2] scale indicates substantial deviation from ground truth
   - Embedding similarity captures cultural signal but with noise
   - Single-scenario responses may not reflect aggregate cultural patterns

2. **Hofstede Framework Constraints**
   - Hofstede's dimensions may not fully capture cultural complexity
   - Framework developed from Western organizational psychology
   - May miss non-Western cultural concepts (e.g., face, Ubuntu)

3. **Scenario Design**
   - 30 scenarios provide good coverage but not exhaustive
   - Some scenarios may be Western-centric in framing
   - Limited to individual-level dilemmas (not institutional or policy contexts)

## 6.2 Technical Limitations

1. **Embedding Model Constraints**
   - `all-MiniLM-L6-v2` trained on English text
   - May not capture non-English cultural concepts
   - Fixed 384-dimensional representation

2. **Single-Run Evaluation**
   - Each (model × culture × scenario) tested only once
   - Doesn't capture model temperature-induced variability
   - No error bars on individual responses

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

1. **Improve Semantic Projection Accuracy**
   - Explore alternative embedding models (multilingual, larger models)
   - Refine cultural exemplar sets based on error analysis
   - Validate with human ratings of cultural alignment
   - Reduce MAE from 1.337 to < 1.0

2. **Multi-Rater Evaluation**
   - Multiple human evaluators for stereotype scoring
   - Calculate inter-rater reliability (Cohen's κ, Fleiss' κ)
   - Use consensus scoring for ground truth

3. **Longitudinal Analysis**
   - Track cultural alignment changes across model updates
   - Measure impact of RLHF and fine-tuning
   - Test temporal stability of cultural personas

4. **Alternative Frameworks**
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

1. **Unexpected Bias:** Models exhibit strongest baseline resemblance to **India** (distance 1.112), not US—challenging assumptions about Western bias
2. **Dimension Difficulty:** Long-Term Orientation (6.08/10) and Uncertainty Avoidance (6.15/10) are hardest dimensions to align
3. **Model Convergence:** All frontier models show statistically identical cultural alignment (p = 0.96)—no single model dominates
4. **Effective Prompting:** Cultural personas induce **35.5% average value shift** (TVD), demonstrating strong prompt effectiveness
5. **Representation Gaps:** Mexico (5.42/10) and UAE (6.36/10) need better training data representation
6. **Imputation Accuracy:** Semantic projection produces MAE of **1.337** on [-2, +2] scale—useful for relative comparisons but imperfect for absolute Hofstede replication
7. **Highest Alignment:** India achieves **7.70/10** alignment—models most reliably emulate Indian cultural reasoning
8. **Stereotype Avoidance:** GPT-4o-mini scores **8.53/10** on stereotype avoidance—significantly better than other models (p < 0.001)

## 9.4 Open Questions

1. **Why does baseline resemble India more than US?** Does this reflect training data composition, semantic embedding biases, or RLHF tuning priorities?
2. **How can we improve LTO and UAI dimension alignment?** Do these dimensions require different evaluation approaches or better exemplar design?
3. **What causes high Hofstede imputation error?** Is the issue with embedding models, exemplar quality, or fundamental limits of semantic projection?
4. **How to balance cultural authenticity vs. harmful stereotypes?** High alignment to cultural norms may reinforce problematic generalizations.
5. **Why does Mexico consistently underperform?** Is this a training data issue, methodological limitation, or genuine difficulty in modeling Mexican cultural values?

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

**Last Updated:** November 25, 2024  
**Dataset Version:** results_20251122_172747  
**Total Responses Analyzed:** 720