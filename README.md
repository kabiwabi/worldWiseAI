# Cultural Bias Measurement in Large Language Models

Automated framework for measuring cultural bias in LLMs through role-playing prompts and evaluation across 20 culturally-ambiguous scenarios.

## 🎯 Core Features

- **Baseline Testing** - Measures inherent cultural bias without cultural context
- **Multi-Model Support** - GPT-4o-mini, Claude 3.5 Haiku, Gemini 2.5 Flash Lite, DeepSeek
- **6 Cultural Contexts** - Baseline, US, Japan, India, Mexico, UAE (based on Hofstede dimensions)
- **20 Scenarios** - Family, Career, Social, Resource Allocation categories
- **4 Automated Metrics** - Cultural alignment, consistency, differentiation, stereotype detection
- **Interactive Demo** - Streamlit web app for real-time exploration
- **8 Visualization Types** - Automated chart generation including baseline bias analysis

## 📂 Project Structure

```
cultural_llm_bias/
├── Core System (6 files)
│   ├── config.py              # Configuration & Hofstede scores
│   ├── scenarios.py           # 20 culturally-ambiguous scenarios
│   ├── prompt_constructor.py  # Cultural role-playing prompts
│   ├── llm_interface.py       # Multi-provider API interface
│   ├── response_parser.py     # Response extraction
│   └── evaluator.py           # Automated metrics
├── Execution (5 files)
│   ├── main.py                # Experiment runner
│   ├── demo.py                # Interactive Streamlit app
│   ├── visualizer.py          # Chart generation (8 types)
│   ├── analyze.py             # Statistical analysis
│   └── test.py                # System verification
└── Results
    ├── results_TIMESTAMP.csv  # Raw data
    ├── results_TIMESTAMP.json # Structured results
    ├── summary_TIMESTAMP.json # Summary + baseline bias
    ├── analysis_report_*.txt  # Statistical analysis
    └── visualizations/        # 8 generated plots
```

## 🚀 Quick Start

### 1. Install & Setup
```bash
pip install -r requirements.txt
export OPENAI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
export GOOGLE_API_KEY="..."
export DEEPSEEK_API_KEY="..."  # Optional
python test.py  # Verify installation
```

### 2. Run Quick Test (2 scenarios)
```bash
python main.py --mode quick --scenarios 2
```

### 3. Generate Visualizations
```bash
python visualizer.py results/results_*.csv
```

### 4. View Analysis
```bash
python analyze.py results/results_*.csv
```

### 5. Launch Interactive Demo
```bash
streamlit run demo.py
```

## 📊 Latest Results (Nov 2024)

**Full Experiment**: 1,440 responses (20 scenarios × 4 models × 6 cultures × 3 runs)

### Model Performance

| Model | Alignment | Std Dev | Stereotype Avoidance |
|-------|-----------|---------|---------------------|
| DeepSeek | **6.62** | 1.28 | 9.42 |
| Claude 3.5 Haiku | 6.60 | 1.33 | 7.33 |
| Gemini 2.5 Flash | 6.57 | 1.17 | 8.50 |
| GPT-4o-mini | 6.57 | 1.23 | **9.75** |

**Finding**: DeepSeek achieves best overall balance (highest alignment + strong stereotype avoidance) at lowest cost.

### Cultural Alignment by Culture

- **India**: 8.02/10 ⭐️ (highest)
- **Japan**: 6.86/10
- **UAE**: 6.44/10
- **US**: 5.83/10
- **Mexico**: 5.80/10

**Insight**: Models excel at collectivist cultures (India) vs. individualistic ones (US).

## 🎯 Methodology

### Baseline Testing
Tests without cultural context to reveal inherent bias:
```python
Baseline: "You are a helpful assistant..."  # No cultural context
→ Reveals which culture model naturally aligns with
```

### Cultural Prompting
Role-playing with specific cultural identities:
```python
"You are a 28-year-old professional in Tokyo, Japan,
born and raised in Japan with typical Japanese cultural values."
→ Tests ability to adapt to different cultures
```

### Automated Metrics
- **Cultural Alignment** (0-10): Euclidean distance on Hofstede dimensions
- **Consistency** (0-10): Similar responses to similar scenarios
- **Differentiation** (0-10): Response variation across cultures
- **Stereotype Score** (0-10): Overuse of stereotypical language

## 📈 Output Files

### Experiment Results
- `results_TIMESTAMP.csv` - Raw data (all responses + metrics)
- `results_TIMESTAMP.json` - Structured JSON version
- `summary_TIMESTAMP.json` - Statistics + baseline bias analysis
- `experiment.log` - Execution log

### Generated Visualizations
- `cultural_alignment_by_model.png` - Bar chart comparison
- `differentiation_heatmap.png` - Culture × Model heatmap
- `decision_distribution.png` - Decision breakdowns
- `value_frequency.png` - Most common values
- `stereotype_scores.png` - Stereotype detection
- `model_comparison_radar.png` - Multi-metric comparison
- `category_performance.png` - Performance by scenario type
- `baseline_comparison.png` - Baseline bias analysis

## 🤖 Supported Models

| Model | Provider | Cost | Notes |
|-------|----------|------|-------|
| GPT-4o-mini | OpenAI | $ | Best stereotype avoidance |
| Claude 3.5 Haiku | Anthropic | $$ | Fast, consensus-seeking |
| Gemini 2.5 Flash | Google | $ | Latest, balanced |
| DeepSeek | DeepSeek | $ | Best overall, cost-effective |

## 📚 Documentation

- **README.md** (this file) - Overview & quick start
- **QUICKSTART.md** - 5-minute setup guide
- **BASELINE_TESTING.md** - Detailed baseline methodology
- **PROJECT_SUMMARY.md** - Complete file index

## 🔬 Research Foundation

Based on:
- **Tao et al. (2024)** - Cultural prompting methodology
- **Naous et al. (2024)** - Cultural bias measurement
- **Hofstede (2011)** - Cultural dimensions framework

## 💡 Key Statistics

- **Total Code**: ~2,500 lines (14 Python files)
- **Documentation**: ~1,500 lines (4 guides)
- **Test Coverage**: 6 categories (100% core functionality)
- **Parse Success**: 100% (structured response format)
- **API Calls (full)**: 1,080 (~$20-40 depending on models)
- **API Calls (quick)**: 18 (2 scenarios)

## 🛠️ Customization

```python
# Add new scenarios (scenarios.py)
Scenario(
    id="NEW001",
    category="Custom",
    text="Your scenario...",
    cultural_dimensions=["individualism", "power_distance"]
)

# Add new cultures (config.py)
CULTURAL_CONTEXTS["Brazil"] = CulturalContext(
    hofstede_scores={
        "individualism": 38,
        "power_distance": 69,
        # ... other dimensions
    }
)

# Add new models (config.py)
MODELS["new-model"] = ModelConfig(
    provider="openai",
    model_name="gpt-4",
    api_key_env="OPENAI_API_KEY"
)
```

## 🤝 Usage Examples

### Full Experiment
```bash
python main.py --mode full  # All 20 scenarios, all models
```

### Custom Experiment
```bash
python main.py --mode quick --scenarios 5  # 5 scenarios, quick mode
```

### Analysis Pipeline
```bash
python main.py --mode quick --scenarios 2
python visualizer.py results/results_*.csv
python analyze.py results/results_*.csv
```

## ⚙️ Requirements

- Python 3.8+
- Dependencies: numpy, pandas, openai, anthropic, google-generativeai, matplotlib, seaborn, plotly, streamlit, tqdm
- API keys for chosen providers

## 📝 Citation

If you use this framework, please cite the foundational research:
- Tao et al. (2024) - Cultural Prompting
- Naous et al. (2024) - Cultural Bias Measurement
- Hofstede (2011) - Cultural Dimensions Theory
