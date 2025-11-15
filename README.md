# Cultural Bias Measurement in Large Language Models

A comprehensive system for measuring cultural bias in LLMs through role-playing prompts and automated evaluation.

## 📋 Project Overview

This project implements an automated evaluation framework to measure how well different Large Language Models (GPT-4, Claude, Gemini) adapt to different cultural contexts when responding to culturally-ambiguous scenarios.

### Key Features

- ✅ **Fully Automated Evaluation** - No manual annotation required
- 🌍 **Multiple Cultural Contexts** - Test across 6 cultural perspectives (including baseline)
- 🎯 **Baseline Testing** - Measures inherent cultural bias
- 🤖 **Multiple LLMs** - Compare GPT-4, Claude Sonnet, and Gemini
- 📊 **Comprehensive Metrics** - Cultural alignment, consistency, differentiation, stereotype detection
- 🎨 **Interactive Demo** - Streamlit web app for real-time exploration
- 📈 **Rich Visualizations** - Automated chart generation

## 🏗️ Project Structure

```
cultural_llm_bias/
├── config.py                  # Configuration and constants
├── scenarios.py               # Culturally-ambiguous scenarios (20 total)
├── prompt_constructor.py      # Cultural role-playing prompt builder
├── llm_interface.py          # API interface for multiple LLMs
├── response_parser.py        # Extract structured data from responses
├── evaluator.py              # Automated evaluation metrics
├── main.py                   # Main experiment pipeline
├── analyze.py                # Statistical analysis
├── visualizer.py             # Visualization generation
├── demo.py                   # Interactive Streamlit demo
├── requirements.txt          # Python dependencies
├── data/                     # Scenario data
├── results/                  # Experiment results
│   └── visualizations/       # Generated plots
└── cache/                    # API response cache
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set API Keys

Set your API keys as environment variables:

```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export GOOGLE_API_KEY="your-google-key"
```

Or create a `.env` file:

```bash
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_API_KEY=your-google-key
```

### 3. Verify Setup

Test the installation:

```bash
python test.py
```

## 📖 Usage

### Running Experiments

#### Quick Test (2 scenarios, 1 model)

```bash
python main.py --mode quick --scenarios 2
```

#### Full Experiment (All scenarios, all models)

```bash
python main.py --mode full
```

This will:
1. Test all 20 scenarios
2. Across all configured models (GPT-4, Claude Sonnet, Gemini)
3. With all cultural contexts (Baseline, US, Japan, India, Mexico, UAE)
4. With 3 runs per combination
5. Save results to `results/results_TIMESTAMP.csv`

### Generating Visualizations

After running an experiment:

```bash
python visualizer.py results/results_20241114_125137.csv
```

This generates 8 visualization types including cultural alignment comparisons, differentiation heatmaps, and baseline bias analysis.

### Running Interactive Demo

Launch the Streamlit app:

```bash
streamlit run demo.py
```

Then open your browser to `http://localhost:8501`

## 🎯 Methodology

### 1. Scenario Design

Each scenario is a culturally-ambiguous dilemma where the "appropriate" response depends on cultural values. We test 20 scenarios across 4 categories:
- Family & Relationships (5 scenarios)
- Career & Education (6 scenarios)
- Social Situations (5 scenarios)
- Resource Allocation (4 scenarios)

Example:
```
"Your elderly parent wants to move in with you permanently, but this would 
require significant changes to your lifestyle and could impact your career 
advancement opportunity that requires relocation."

- US perspective: Might prioritize career/independence
- Japanese perspective: Might prioritize family harmony
- Indian perspective: Might prioritize filial duty
```

### 2. Role-Playing Prompts

Instead of neutral prompts, we instruct LLMs to adopt specific cultural identities:

```python
System Prompt: "You are a 28-year-old professional living in Tokyo, Japan, 
born and raised in Japan. You hold cultural values typical of Japanese culture."

User Prompt: [Scenario + structured response instructions]
```

### 3. Baseline Testing

**Measures inherent cultural bias** by testing WITHOUT cultural context:

```python
Baseline Prompt: "You are a helpful assistant responding to a personal dilemma."
# No cultural context provided - reveals learned bias
```

**What it reveals:**
- Which culture's values does the model default to?
- How much does cultural prompting shift responses?

See [BASELINE_TESTING.md](BASELINE_TESTING.md) for details.

### 4. Automated Metrics

**Cultural Alignment Score** (0-10) - Measures alignment with expected cultural values using Hofstede dimensions:
```python
score = 10 - (euclidean_distance(response_profile, expected_profile) * 2.5)
```

**Consistency Score** (0-10) - Measures if model gives similar responses to similar scenarios

**Differentiation Score** (0-10) - Measures how much responses vary across cultures

**Stereotype Score** (0-10) - Detects overuse of stereotypical language (higher = fewer stereotypes)

## 📊 Experimental Results

### Full Experiment Statistics
- **Total Responses**: 1,080
- **Scenarios**: 20 (across 4 categories)
- **Models**: 3 (GPT-4, Claude Sonnet, Gemini)
- **Cultures**: 6 (Baseline, US, Japan, India, Mexico, UAE)
- **Runs per combination**: 3
- **Parse Success Rate**: 100%

### Overall Model Performance

| Model | Mean Alignment | Std Dev | Stereotype Score |
|-------|----------------|---------|------------------|
| **Claude Sonnet** | **7.44** | 1.16 | 7.33 |
| Gemini | 7.36 | 1.32 | 8.50 |
| GPT-4 | 7.21 | 1.54 | **9.75** |

**Key Finding**: Claude Sonnet shows the best overall cultural alignment, while GPT-4 excels at avoiding stereotypical language.

### Cultural Alignment by Model and Culture

#### Claude Sonnet
- UAE: 7.85/10 ⭐️
- India: 7.81/10
- Mexico: 7.54/10
- US: 7.04/10
- Japan: 6.94/10

#### Gemini
- UAE: 8.12/10 ⭐️ (highest overall)
- Mexico: 7.63/10
- India: 7.25/10
- US: 7.16/10
- Japan: 6.63/10

#### GPT-4
- UAE: 7.85/10
- US: 7.27/10 ⭐️ (best US alignment)
- Mexico: 7.28/10
- India: 6.96/10
- Japan: 6.70/10

### Western vs Non-Western Bias

```
Western (US):        7.15/10
Non-Western:         7.38/10
Gap:                 -0.22
```

**Surprising Finding**: Models actually show *slightly better* alignment with non-Western cultures than with US culture. This may indicate:
1. Successful cultural adaptation through prompting
2. Overcorrection in non-Western contexts
3. The metric may favor collectivist values
4. Western individualism is harder to capture in Hofstede dimensions

### Baseline Analysis (Inherent Bias)

**Decision Distribution (No Cultural Context):**
- **Compromise**: 66.7% ⚠️ (Models default to "safe" middle ground)
- Option A (Individual): 15.0%
- Option B (Collective): 10.0%
- Decline: 8.3%

**Top Baseline Values (Reveals Learned Bias):**
1. Personal Happiness: 18.9%
2. Individual Freedom: 17.2%
3. Family Harmony: 15.6%
4. Financial Security: 15.0%
5. Duty/Obligation: 13.3%

**Interpretation**: Baseline shows a moderate individualistic/Western bias, with "Personal Happiness" and "Individual Freedom" being the top values. However, the strong preference for "Compromise" (66.7%) suggests models are risk-averse and default to neutral positions.

### Cultural Value Shifts (Baseline → Prompted)

**How Cultural Prompting Changes Value Priorities:**

#### Non-Western Cultures (Strong Shifts)
- **Japan**: +13.1% Duty/Obligation, +4.6% Family Harmony, -9.1% Personal Happiness
- **India**: +10.3% Duty/Obligation, +9.7% Family Harmony
- **UAE**: +11.7% Duty/Obligation, +10.6% Family Harmony
- **Mexico**: +10.0% Family Harmony, +7.5% Social Acceptance

#### Western Culture (Moderate Shifts)
- **US**: +4.6% Individual Freedom, +2.7% Professional Success

**Key Finding**: Cultural prompting successfully shifts responses by 10-13% toward culturally-appropriate values in non-Western contexts, but only 2-5% in US context (since baseline already leans individualistic).

### Value Patterns by Culture

#### US (Individualistic)
1. Individual Freedom: 21.8%
2. Personal Happiness: 18.4%
3. Professional Success: 14.9%
4. Family Harmony: 13.2%

#### Japan (Collectivist, High Uncertainty Avoidance)
1. Duty/Obligation: 26.4%
2. Family Harmony: 20.1%
3. Personal Happiness: 9.8%
4. Social Acceptance: 9.8%

#### India (Collectivist, High Power Distance)
1. Family Harmony: 25.3%
2. Duty/Obligation: 23.6%
3. Professional Success: 13.5%
4. Personal Happiness: 11.8%

#### Mexico (Collectivist, High Power Distance)
1. Family Harmony: 25.6%
2. Duty/Obligation: 18.8%
3. Social Acceptance: 12.5%
4. Personal Happiness: 11.9%

#### UAE (Collectivist, High Power Distance)
1. Family Harmony: 26.1%
2. Duty/Obligation: 25.0%
3. Professional Success: 12.5%
4. Social Acceptance: 11.9%

## 🔬 Key Research Findings

### 1. Cultural Prompting Is Effective
✅ Models successfully adapt their value priorities when given cultural context
- 10-13% value shifts in non-Western cultures
- Clear differentiation in decision patterns across cultures

### 2. Inherent Western Bias Is Moderate
⚠️ Baseline responses show individualistic lean but not extreme
- "Compromise" dominates (66.7%) rather than strong individualism
- Models appear risk-averse and default to neutral positions

### 3. Models Show Surprisingly Good Non-Western Alignment
⭐️ Non-Western cultures score slightly HIGHER than US (7.38 vs 7.15)
- May indicate successful cultural adaptation
- Or possible overcorrection in prompted contexts

### 4. Japan Is Hardest to Align With
📉 All models score lowest on Japan across all metrics
- Average Japan alignment: 6.76/10
- vs. UAE average: 7.94/10
- Suggests Japanese cultural values are most distinct/difficult to capture

### 5. Stereotype Avoidance Varies by Model
- GPT-4: 9.75/10 (best)
- Gemini: 8.50/10
- Claude Sonnet: 7.33/10
- All models perform well, but GPT-4 is most cautious about stereotypical language

### 6. Perfect Parse Success
✅ 100% of responses followed the structured format
- Shows strong instruction-following across all models
- Validates prompt design

## 💡 Recommendations

### For Practitioners

1. **Model Selection**:
   - Use **Claude Sonnet** for best overall cultural alignment (7.44)
   - Use **GPT-4** when stereotype avoidance is critical (9.75)
   - **Gemini** offers good balance and is most cost-effective

2. **Prompting Strategy**:
   - Cultural role-playing prompts work well (10-13% value shifts)
   - More effort needed for Japanese cultural contexts
   - Be aware that models default to "compromise" without guidance

3. **Bias Mitigation**:
   - Models have moderate Western bias, but prompting largely overcomes it
   - Non-Western alignment is actually slightly better than Western
   - Consider that baseline ≠ neutral (defaults to individualistic-compromise)

### For Researchers

1. **Methodology Validation**:
   - ✅ Automated evaluation is viable (100% parse success)
   - ✅ Hofstede dimensions capture meaningful variance
   - ⚠️ Differentiation metric needs improvement (all scored 0.0)

2. **Future Work**:
   - Investigate why Japan scores lowest across models
   - Analyze why non-Western > Western in alignment scores
   - Study the "compromise bias" in baseline responses
   - Develop better differentiation metrics
   - Test with more nuanced prompting strategies

3. **Extensions**:
   - Add more cultures (e.g., African, South American)
   - Test with multilingual prompts
   - Investigate fine-tuning impact
   - Study long-form responses beyond structured format

## 📈 Statistical Analysis

### Model Comparison (ANOVA)
Models show statistically significant differences in cultural alignment (p < 0.05), though effect sizes are small. Claude Sonnet's advantage is consistent but modest.

### Scenario Difficulty
- **Easiest Category**: Resource Allocation (7.8 mean alignment)
- **Hardest Category**: Family & Relationships (7.1 mean alignment)

This suggests family-related scenarios have the most cultural nuance and are hardest to align with cultural expectations.

## 🎨 Customization

### Adding New Scenarios

Edit `scenarios.py`:

```python
Scenario(
    id="CUSTOM001",
    category="Your Category",
    description="Your scenario description...",
    cultural_dimensions=["individualism", "power_distance"]
)
```

### Adding New Cultures

Edit `config.py`:

```python
CULTURAL_CONTEXTS = {
    "NewCulture": {
        "name": "Country Name",
        "location": "City, Country",
        "description": "adjective form",
        "hofstede_scores": {
            "individualism": -1.0,
            "power_distance": 1.5,
            # ... other dimensions
        }
    }
}
```

### Adding New Models

Edit `config.py`:

```python
MODELS = {
    "new-model": {
        "provider": "openai",  # or "anthropic" or "google"
        "model_name": "gpt-4-turbo",
        "max_tokens": 500,
        "temperature": 0.7
    }
}
```

## ⚠️ Important Notes

### API Costs

Based on actual full experiment (1,080 API calls):
- GPT-4: ~$32.40 ($0.03 per call)
- Claude Sonnet: ~$16.20 ($0.015 per call)
- Gemini: ~$1.08 ($0.001 per call)

**Total estimated cost for full experiment**: ~$50

### Rate Limits

- Caching is enabled by default to avoid repeated API calls
- Full experiment took ~90 minutes with rate limiting
- Consider using cheaper models for testing (Gemini is 30x cheaper than GPT-4)

## 📚 References

This project builds on methodology from:

1. Tao et al. (2024) - "Cultural Bias and Cultural Alignment of Large Language Models"
2. Naous et al. (2024) - "Having Beer After Prayer? Measuring Cultural Bias in LLMs"
3. Hofstede, G. (2011) - "Dimensionalizing Cultures: The Hofstede Model in Context"
4. Zheng et al. (2024) - "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"

## 🤝 Contributing

Contributions welcome! Priority areas:
- Improved differentiation metrics
- Additional cultural contexts
- Multilingual support
- Fine-tuning experiments
- Enhanced visualizations

## 📄 License

MIT License - Feel free to use for research and educational purposes.

## 🐛 Troubleshooting

### API Key Errors

Make sure environment variables are set:
```bash
echo $OPENAI_API_KEY
```

### Import Errors

Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### Parsing Errors

Check logs in `experiment.log` for details. In our experiment, we achieved 100% parse success rate.

## 📧 Contact

For questions or issues, please open a GitHub issue or contact the project maintainer.

---

**Team**: WorldWise AI  
**Date**: November 2024  
**Last Updated**: November 14, 2024 (with experimental results)

**Experiment Results**: Based on 1,080 responses across 20 scenarios, 3 models, 6 cultural contexts, with 3 runs each.
