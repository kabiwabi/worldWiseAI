# Baseline Testing Feature

## 🎯 Overview

The baseline testing feature has been added to automatically measure **inherent cultural bias** in LLMs. This addresses the core requirement: *"evaluate the cultural notions learned by LLMs"*.

## 🔬 What is Baseline Testing?

**Baseline testing** runs scenarios **WITHOUT** any cultural context in the prompt, revealing what cultural values the model exhibits by default. This shows the "learned" cultural bias baked into the model's training data.

### Example Comparison:

**With Cultural Prompting (Existing):**
```
System: "You are a 28-year-old professional living in Tokyo, Japan, 
born and raised in Japan. You hold Japanese cultural values..."

User: [Scenario about family vs. career conflict]
```

**Baseline (NEW - No Cultural Context):**
```
System: "You are a helpful assistant responding to a personal dilemma."

User: [Same scenario]
```

## 📊 What Baseline Reveals

### 1. **Default Cultural Bias**
- Which culture's values does the model naturally align with?
- Does it default to Western (US) values?
- Example: "Baseline responses are CLOSEST to US cultural values"

### 2. **Cultural Shift Magnitude**
- How much does cultural prompting change responses?
- Can the model overcome its default bias?
- Measures the gap between baseline and prompted responses

### 3. **Learned vs. Adaptive Behavior**
- **Learned**: What's baked into training data (baseline)
- **Adaptive**: Can it adapt when prompted? (with cultural context)

## 🚀 How to Use

### Automatic Inclusion

Baseline is now **automatically included** in all experiments:

```bash
python main.py --mode quick
# Now tests: baseline, US, Japan

python main.py --mode full
# Now tests: baseline, US, Japan, India, Mexico, UAE
```

### Manual Control

```python
from main import ExperimentRunner

# Include baseline (default)
runner = ExperimentRunner(
    scenarios=["FAM001", "FAM002"],
    models=["gpt-4"],
    cultures=["US", "Japan"],
    include_baseline=True  # Adds "baseline" to cultures
)

# Exclude baseline
runner = ExperimentRunner(
    scenarios=["FAM001"],
    models=["gpt-4"],
    cultures=["US", "Japan"],
    include_baseline=False  # Only test specified cultures
)
```

## 📈 Results and Analysis

### 1. **Summary Statistics**

The `summary_TIMESTAMP.json` file now includes:

```json
{
  "baseline_bias": {
    "closest_culture": "US",
    "distance": 0.45,
    "all_distances": {
      "US": 0.45,
      "Japan": 1.82,
      "India": 2.13,
      "Mexico": 1.56,
      "UAE": 1.98
    },
    "interpretation": "Baseline responses are closest to US cultural values"
  }
}
```

### 2. **Automated Analysis**

Run `analyze.py` to see baseline bias detection:

```bash
python analyze.py results/results_TIMESTAMP.csv
```

Output includes:
```
🔍 BASELINE BIAS DETECTION
Analyzing inherent cultural bias (responses without cultural context)
─────────────────────────────────────────────────────────────────

Baseline Distance from Each Culture:
(Lower distance = baseline is closer to this culture's values)
  US................................ 0.453
  Mexico............................ 1.562
  Japan............................. 1.823
  India............................. 2.134
  UAE............................... 1.982

⚠️  INHERENT BIAS DETECTED:
  Baseline responses are CLOSEST to: US
  Distance: 0.453

  This suggests the model has an inherent US cultural bias
  when not explicitly prompted with a cultural context.
```

### 3. **Visualizations**

New visualization: `baseline_comparison.png`

Shows:
- Decision distribution in baseline vs. other cultures
- Value frequency in baseline responses
- Reveals which values dominate without cultural prompting

## 🔍 Interpreting Results

### Strong Baseline Bias

```
Baseline → US: 0.3
Baseline → Japan: 2.1
Baseline → India: 2.4
```

**Interpretation**: Model has strong US bias. Without cultural prompting, it responds like an American.

### Weak Baseline Bias

```
Baseline → US: 1.2
Baseline → Japan: 1.4
Baseline → India: 1.3
```

**Interpretation**: Model is relatively neutral or represents a mix of cultures.

### Cultural Prompting Effectiveness

Compare baseline distance to prompted alignment:

```
Baseline → Japan: 2.1 (far from Japan)
With Japan prompt → Japan alignment: 7.5/10 (good alignment)
```

**Cultural shift**: 5.4 points - prompting successfully overcomes bias!

```
Baseline → Japan: 2.1
With Japan prompt → Japan alignment: 5.2/10 (poor alignment)
```

**Cultural shift**: 3.1 points - prompting helps but doesn't fully overcome bias

## 📊 Research Implications

### Answers Key Questions:

1. **"What cultural notions did the LLM learn?"**
   - ✅ Revealed by baseline testing
   - Shows inherent bias from training data

2. **"Can LLMs adapt to different cultures?"**
   - ✅ Compare baseline vs. prompted responses
   - Measures cultural shift magnitude

3. **"Which models have less baked-in bias?"**
   - ✅ Compare baseline distances across models
   - Lower baseline bias = more neutral model

## 🎓 Academic Context

This approach aligns with established methodology:

**Tao et al. (2024)** - "Cultural Bias and Cultural Alignment"
- Used neutral prompts to establish baseline
- Compared to culturally-prompted responses
- Measured shift magnitude

**This implementation extends their work:**
- Automated baseline bias calculation
- Statistical comparison of learned vs. adaptive behavior
- Identifies closest cultural match

## 💡 Example Use Cases

### Use Case 1: Model Selection

```
Model A Baseline → US: 0.3 (strong US bias)
Model B Baseline → US: 1.2 (weaker US bias)

Choose Model B for global deployment!
```

### Use Case 2: Prompt Engineering

```
Baseline: Prioritizes individual freedom (US value)

With Japanese prompt: Still prioritizes individual freedom
→ Need stronger cultural framing in prompt

With refined Japanese prompt: Prioritizes family harmony
→ Successful cultural adaptation
```

### Use Case 3: Training Data Analysis

```
All models show baseline → US: < 0.5

Suggests: Western-centric training data across providers
Action: Advocate for more diverse training corpora
```

## 📝 Technical Details

### Implementation

**Location**: Multiple files updated
- `config.py` - Added baseline to CULTURAL_CONTEXTS
- `prompt_constructor.py` - Detects baseline and uses neutral prompt
- `evaluator.py` - Handles baseline (returns 5.0 for alignment)
- `evaluator.py` - New `calculate_baseline_bias()` function
- `main.py` - Auto-includes baseline in experiments
- `analyze.py` - Baseline bias detection analysis
- `visualizer.py` - New baseline comparison plot
- `demo.py` - Baseline option in UI

### Baseline Culture Definition

```python
"baseline": {
    "name": "Baseline (No Cultural Context)",
    "location": "No specific location",
    "description": "neutral",
    "hofstede_scores": {
        "individualism": 0.0,      # All dimensions neutral
        "power_distance": 0.0,
        "masculinity": 0.0,
        "uncertainty_avoidance": 0.0,
        "long_term_orientation": 0.0,
        "indulgence": 0.0,
    }
}
```

### Baseline Bias Calculation

```python
def calculate_baseline_bias(
    baseline_responses,
    cultural_contexts,
    scenario_dimensions
) -> Dict[str, float]:
    """
    1. Infer cultural profile from baseline responses
    2. Calculate Euclidean distance to each culture
    3. Return distances (lower = closer match)
    """
```

## ✅ Verification

Run tests to verify baseline functionality:

```bash
python test.py
```

Should see:
```
✓ Prompt construction for baseline (no cultural context)
✓ Baseline alignment score: 5.00/10 (neutral)
```

## 🎯 Summary

**Before**: Only tested model behavior WITH cultural prompting
**After**: Tests BOTH learned bias (baseline) AND adaptive capability (prompted)

This fully addresses the requirement:
> "evaluate the cultural notions learned by LLMs"

The baseline reveals what was **learned** (inherent bias), while cultural prompting tests what can be **adapted** (prompted behavior).

---

**Added**: November 2024
**Impact**: Strengthens research rigor and requirement alignment
**Status**: ✅ Fully Integrated and Tested
