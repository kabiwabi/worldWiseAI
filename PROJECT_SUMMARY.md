# Project File Index

## 📁 Complete Python Codebase for Cultural Bias Measurement in LLMs

This document provides an overview of all files in the project.

---

## 🔧 Core System Files

### `config.py` (5.4 KB)
- Central configuration file
- Contains API keys, model configurations, cultural contexts
- Hofstede dimension scores for each culture
- All system constants and settings
- **Key contents**: MODELS dict, CULTURAL_CONTEXTS dict, evaluation settings

### `scenarios.py` (11 KB)
- Defines all 20 culturally-ambiguous scenarios
- Organized into 4 categories:
  - Family & Relationships (5 scenarios)
  - Career & Education (6 scenarios)
  - Social Situations (5 scenarios)
  - Resource Allocation (4 scenarios)
- Each scenario specifies relevant cultural dimensions
- **Key class**: `Scenario` dataclass

### `prompt_constructor.py` (7.2 KB)
- Builds culturally-contextualized prompts
- Creates system prompts with cultural identity
- Creates user prompts with structured response instructions
- Generates LLM-as-judge evaluation prompts
- **Key classes**: `PromptConstructor`, `BaselinePromptConstructor`

### `llm_interface.py` (12 KB)
- Handles all API calls to different LLM providers
- Supports OpenAI, Anthropic, and Google
- Implements caching to avoid duplicate API calls
- Includes rate limiting and error handling
- **Key class**: `LLMInterface`

### `response_parser.py` (10 KB)
- Extracts structured data from LLM responses
- Parses decisions, top values, and explanations
- Handles multiple response formats
- Includes judge response parsing
- **Key classes**: `ResponseParser`, `ParsedResponse` dataclass

### `evaluator.py` (13 KB)
- Computes all automated evaluation metrics
- **Metrics**:
  - Cultural alignment (Euclidean distance on Hofstede dimensions)
  - Consistency (across similar scenarios)
  - Differentiation (across cultures)
  - Stereotype detection
- **Key class**: `CulturalEvaluator`

---

## 🚀 Execution Files

### `main.py` (9.2 KB)
- Main experiment pipeline
- Orchestrates complete experiment workflow
- Handles progress tracking and error logging
- Saves results to JSON and CSV
- Generates summary statistics
- **Usage**: `python main.py --mode [quick|full]`

### `demo.py` (9.5 KB)
- Interactive Streamlit web application
- Real-time scenario testing
- Side-by-side response comparison
- Interactive visualizations
- **Usage**: `streamlit run demo.py`

### `visualizer.py` (11 KB)
- Generates all plots and charts
- Creates 7 different visualization types:
  - Cultural alignment comparison
  - Differentiation heatmaps
  - Decision distributions
  - Value frequency analysis
  - Stereotype scores
  - Radar charts
  - Category performance
- **Usage**: `python visualizer.py results/results_*.csv`

### `analyze.py` (8.2 KB)
- Comprehensive statistical analysis
- Generates insights and recommendations
- Performs ANOVA tests
- Identifies patterns and biases
- **Usage**: `python analyze.py results/results_*.csv`

### `test.py` (7.7 KB)
- Complete system verification
- Tests all modules
- Validates installation
- Checks API key configuration
- **Usage**: `python test.py`

---

## 📚 Documentation Files

### `README.md` (8.8 KB)
- Complete project documentation
- Setup instructions
- Methodology explanation
- Usage examples
- Sample results and findings
- Customization guide

### `QUICKSTART.md` (3.4 KB)
- 5-minute getting started guide
- Essential commands
- Quick troubleshooting
- Example workflow

### `requirements.txt` (365 bytes)
- All Python dependencies
- Includes: numpy, pandas, openai, anthropic, google-generativeai, matplotlib, seaborn, plotly, streamlit, tqdm

### `.gitignore`
- Standard Python gitignore
- Excludes cache, results, API keys

---

## 📊 Data Structure

```
cultural_llm_bias/
│
├── Core System
│   ├── config.py              # Configuration
│   ├── scenarios.py           # Scenario definitions
│   ├── prompt_constructor.py  # Prompt generation
│   ├── llm_interface.py       # API interface
│   ├── response_parser.py     # Response parsing
│   └── evaluator.py           # Metrics calculation
│
├── Execution
│   ├── main.py                # Experiment runner
│   ├── demo.py                # Interactive demo
│   ├── visualizer.py          # Chart generation
│   ├── analyze.py             # Statistical analysis
│   └── test.py                # System verification
│
├── Documentation
│   ├── README.md              # Full documentation
│   ├── QUICKSTART.md          # Quick start guide
│   ├── requirements.txt       # Dependencies
│   └── .gitignore             # Git ignore rules
│
└── Output Directories
    ├── data/                  # Input data
    ├── cache/                 # API response cache
    └── results/               # Experiment outputs
        └── visualizations/    # Generated plots
```

---

## 🔄 Typical Workflow

1. **Setup**: Install dependencies, set API keys
   ```bash
   pip install -r requirements.txt
   export OPENAI_API_KEY="..."
   ```

2. **Verify**: Run tests
   ```bash
   python test.py
   ```

3. **Quick Test**: Test with 2 scenarios
   ```bash
   python main.py --mode quick --scenarios 2
   ```

4. **Visualize**: Generate plots
   ```bash
   python visualizer.py results/results_*.csv
   ```

5. **Analyze**: Get insights
   ```bash
   python analyze.py results/results_*.csv
   ```

6. **Explore**: Launch demo
   ```bash
   streamlit run demo.py
   ```

7. **Full Run**: Complete experiment
   ```bash
   python main.py --mode full
   ```

---

## 📈 Output Files

### Experiment Results
- `results_TIMESTAMP.csv` - Raw experimental data (all responses and metrics)
- `results_TIMESTAMP.json` - Structured JSON version
- `summary_TIMESTAMP.json` - Aggregated statistics
- `experiment.log` - Detailed execution log

### Visualizations (in `results/visualizations/`)
- `cultural_alignment_by_model.png` - Bar chart comparison
- `differentiation_heatmap.png` - Culture × Model heatmap
- `decision_distribution.png` - Decision breakdowns
- `value_frequency.png` - Most common values
- `stereotype_scores.png` - Stereotype detection results
- `model_comparison_radar.png` - Multi-metric comparison
- `category_performance.png` - Performance by scenario type

---

## 🎯 Key Features

✅ **Fully Automated** - No manual evaluation required
✅ **Multi-Model** - Supports GPT-4, Claude, Gemini, and more
✅ **Multi-Cultural** - Tests across 5+ cultural contexts
✅ **Comprehensive Metrics** - 4 automated evaluation dimensions
✅ **Interactive Demo** - Real-time exploration via web app
✅ **Rich Visualizations** - 7 chart types automatically generated
✅ **Statistical Analysis** - ANOVA, effect sizes, significance tests
✅ **Reproducible** - Caching and consistent methodology
✅ **Extensible** - Easy to add scenarios, cultures, or models
✅ **Well-Documented** - Comprehensive guides and examples

---

## 💡 Code Statistics

- **Total Files**: 14 Python files + 4 documentation files
- **Total Lines of Code**: ~2,500 lines
- **Total Documentation**: ~1,500 lines
- **Test Coverage**: 6 test categories
- **Scenarios**: 20 predefined, easily extensible
- **Cultures**: 5 configured (US, Japan, India, Mexico, UAE)
- **Models**: 3 configured (GPT-4, Claude, Gemini)
- **Metrics**: 4 automated evaluation dimensions

---

## 🔬 Research Methodology

Based on published research:
1. **Cultural Prompting** (Tao et al., 2024)
2. **Cultural Bias Measurement** (Naous et al., 2024)
3. **Hofstede's Cultural Dimensions** (Hofstede, 2011)
4. **LLM-as-Judge** (Zheng et al., 2024)

---

## 📦 Ready to Use

All files are production-ready:
- ✅ Error handling
- ✅ Logging
- ✅ Type hints
- ✅ Docstrings
- ✅ Configuration management
- ✅ Caching
- ✅ Progress tracking
- ✅ Modular design

---

**Created**: November 2024
**Author**: Kabin Wang (WorldWise AI)
**Purpose**: Automated cultural bias measurement in LLMs for academic research
