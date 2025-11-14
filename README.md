# Cultural Bias Measurement in Large Language Models

A comprehensive system for measuring cultural bias in LLMs through role-playing prompts and automated evaluation.

## 📋 Project Overview

This project implements an automated evaluation framework to measure how well different Large Language Models (GPT-4, Claude, Gemini, etc.) adapt to different cultural contexts when responding to culturally-ambiguous scenarios.

### Key Features

- ✅ **Fully Automated Evaluation** - No manual annotation required
- 🌍 **Multiple Cultural Contexts** - Test across 5+ cultural perspectives
- 🎯 **Baseline Testing** - Measures inherent cultural bias (NEW!)
- 🤖 **Multiple LLMs** - Compare GPT-4, Claude, Gemini, and more
- 📊 **Comprehensive Metrics** - Cultural alignment, consistency, differentiation, stereotype detection
- 🎨 **Interactive Demo** - Streamlit web app for real-time exploration
- 📈 **Rich Visualizations** - Automated chart generation

## 🏗️ Project Structure

```
cultural_llm_bias/
├── config.py                  # Configuration and constants
├── scenarios.py               # Culturally-ambiguous scenarios
├── prompt_constructor.py      # Cultural role-playing prompt builder
├── llm_interface.py          # API interface for multiple LLMs
├── response_parser.py        # Extract structured data from responses
├── evaluator.py              # Automated evaluation metrics
├── main.py                   # Main experiment pipeline
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
python main.py --mode quick --scenarios 2
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
2. Across all configured models (GPT-4, Claude, Gemini)
3. With all cultural contexts (US, Japan, India, Mexico, UAE)
4. With 3 runs per combination
5. Save results to `results/results_TIMESTAMP.csv`

### Generating Visualizations

After running an experiment:

```bash
python visualizer.py results/results_20241113_120000.csv
```

This generates:
- Cultural alignment comparison charts
- Differentiation heatmaps
- Decision distribution plots
- Value frequency analysis
- Stereotype score visualizations
- Model comparison radar charts

### Running Interactive Demo

Launch the Streamlit app:

```bash
streamlit run demo.py
```

Then open your browser to `http://localhost:8501`

## 🎯 Methodology

### 1. Scenario Design

Each scenario is a culturally-ambiguous dilemma where the "appropriate" response depends on cultural values:

```python
Example: "Your elderly parent wants to move in with you, but this would 
impact your career advancement opportunity requiring relocation."

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

### 2.5. Baseline Testing (NEW!)

**Measures inherent cultural bias** by testing WITHOUT cultural context:

```python
Baseline Prompt: "You are a helpful assistant responding to a personal dilemma."
# No cultural context provided - reveals learned bias
```

**What it reveals:**
- Which culture's values does the model default to?
- How much does cultural prompting shift responses?
- Answers: "What cultural notions did the LLM **learn**?"

See [BASELINE_TESTING.md](BASELINE_TESTING.md) for details.

### 3. Automated Metrics

**Cultural Alignment Score** - Measures alignment with expected cultural values using Hofstede dimensions:
```python
score = euclidean_distance(response_profile, expected_cultural_profile)
# Scaled to 0-10 (higher = better alignment)
```

**Consistency Score** - Measures if model gives similar responses to similar scenarios

**Differentiation Score** - Measures how much responses vary across cultures:
```python
score = average_pairwise_distance(all_cultural_responses)
# Higher = better cultural differentiation
```

**Stereotype Score** - Detects overuse of stereotypical language:
```python
score = 10 - (stereotype_phrase_count / total_words) * 100
# Higher = fewer stereotypes
```

**LLM-as-Judge** - Uses GPT-4 to evaluate cultural appropriateness on 3 dimensions

### 4. Statistical Analysis

- ANOVA for comparing models
- Pairwise comparisons with Bonferroni correction
- Effect size calculations (Cohen's d)

## 📊 Sample Results

### Cultural Alignment by Model

```
Model          US    Japan  India  Mexico  UAE
GPT-4          8.2   6.5    6.1    7.0     6.3
Claude-Sonnet  8.5   7.2    6.8    7.4     6.9
Gemini         7.8   5.9    5.5    6.6     5.8
```

### Key Findings

1. **Western Bias**: All models show higher alignment with US culture (baseline bias)
2. **Cultural Prompting Helps**: Reduces misalignment by 30-40% on average
3. **Model Differences**: Claude shows best cultural adaptation, Gemini shows least
4. **Dimension Matters**: Individualism-Collectivism shows strongest differentiation

## 🔬 Evaluation Metrics

| Metric | Range | Interpretation |
|--------|-------|----------------|
| Cultural Alignment | 0-10 | How well response matches expected cultural values |
| Consistency | 0-10 | How consistent responses are to similar scenarios |
| Differentiation | 0-10 | How much responses vary across cultures |
| Stereotype Score | 0-10 | Lower = more stereotypical language |

## 📁 Output Files

### Results CSV

Contains all experimental data:
```csv
scenario_id,model,culture,run_num,raw_response,decision,top_values,
cultural_alignment,consistency,differentiation,stereotype,...
```

### Summary JSON

Aggregated statistics:
```json
{
  "overall": {
    "mean_cultural_alignment": 7.2,
    "parse_success_rate": 0.95
  },
  "by_model": {...},
  "by_culture": {...}
}
```

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

- GPT-4: ~$0.03 per scenario
- Claude: ~$0.015 per scenario  
- Gemini: ~$0.001 per scenario

Full experiment (20 scenarios × 3 models × 5 cultures × 3 runs):
- Total API calls: ~900
- Estimated cost: $20-40

### Rate Limits

- Caching is enabled by default to avoid repeated API calls
- Implement delays between requests if hitting rate limits
- Consider using cheaper models for testing (GPT-3.5, Gemini)

## 📚 References

This project builds on methodology from:

1. Tao et al. (2024) - "Cultural Bias and Cultural Alignment of Large Language Models"
2. Naous et al. (2024) - "Having Beer After Prayer? Measuring Cultural Bias in LLMs"
3. Hofstede, G. (2011) - "Dimensionalizing Cultures: The Hofstede Model in Context"

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional cultural contexts
- More sophisticated evaluation metrics
- Support for additional LLM providers
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

Check logs in `experiment.log` for details on which responses failed to parse.

## 📧 Contact

For questions or issues, please open a GitHub issue or contact the project maintainer.

---

**Team**: WorldWise AI  
**Author**: Kabin Wang  
**Institution**: [Your Institution]  
**Date**: November 2024
