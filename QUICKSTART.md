# 🚀 Quick Start Guide

Get up and running with the Cultural Bias Measurement System in **5 minutes**!

---

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies

```bash
cd cultural_llm_bias
pip install -r requirements.txt
```

**Packages installed:**
- Core: `numpy`, `pandas`, `scipy`
- API clients: `openai`, `anthropic`, `google-generativeai`
- Visualization: `matplotlib`, `seaborn`, `plotly`
- Interactive: `streamlit`
- Utilities: `tqdm`, `python-dotenv`

---

### Step 2: Set API Keys

```bash
# Required: At least one model
export OPENAI_API_KEY="sk-..."              # For GPT-4o-mini
export ANTHROPIC_API_KEY="sk-ant-..."      # For Claude 3.5 Haiku
export GOOGLE_API_KEY="..."                # For Gemini 2.5 Flash
export DEEPSEEK_API_KEY="..."             # For DeepSeek (recommended)
```

**💡 Pro Tip**: Add to `~/.bashrc` or `~/.zshrc` to persist:

```bash
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.bashrc
source ~/.bashrc
```

**Cost Comparison** (per 1M tokens):
- DeepSeek: $0.14 / $0.28 (🏆 Best value)
- Gemini: $0.075 / $0.30 (💰 Cheapest)
- GPT-4o-mini: $0.15 / $0.60 (🥇 Best stereotypes)
- Claude: $3.00 / $15.00 (Premium)

---

### Step 3: Verify Installation

```bash
python test.py
```

**Expected output:**

```
🧪 Running Cultural LLM Bias Framework Tests

Testing Core Components...
✅ PASS: Configuration loading
✅ PASS: Scenario definitions (20 scenarios loaded)
✅ PASS: Prompt construction (baseline and cultural)
✅ PASS: Response parsing
✅ PASS: Evaluation metrics
✅ PASS: LLM interface initialization

Testing API Keys...
✅ OpenAI API key configured
✅ Anthropic API key configured
✅ Google API key configured
✅ DeepSeek API key configured

All tests passed! ✨
```

---

### Step 4: Run Quick Test (2 Scenarios)

```bash
python main.py --mode quick --scenarios 2
```

**What this does:**
- Tests **2 scenarios** (FAM001, CAR001)
- Uses **all models** with API keys set
- Tests **baseline + US + Japan** cultures
- Completes in **~2 minutes**
- Costs **~$0.10**

**Output files:**
```
results/
├── results_20251117_150802.csv      # Raw data
├── results_20251117_150802.json     # Structured results
├── summary_20251117_150802.json     # Statistics + baseline bias
└── experiment.log                    # Execution log
```

---

### Step 5: View Results

```bash
# Quick peek at summary
cat results/summary_*.json

# View baseline bias detection
grep -A 10 "baseline_bias" results/summary_*.json
```

**Example output:**

```json
{
  "baseline_bias": {
    "closest_culture": "India",
    "distance": 1.066,
    "interpretation": "Baseline responses are closest to Indian cultural values",
    "all_distances": {
      "India": 1.066,
      "Japan": 1.389,
      "US": 1.413,
      "UAE": 1.583,
      "Mexico": 1.909
    }
  }
}
```

---

## 📊 Generate Visualizations

```bash
python visualizer.py results/results_*.csv
```

**Creates 11 visualizations in `results/visualizations/`:**

1. ✅ `cultural_alignment_by_model.png` - Model comparison
2. ✅ `differentiation_heatmap.png` - Culture × Model heatmap
3. ✅ `decision_distribution.png` - Decision breakdowns
4. ✅ `value_frequency.png` - Most common values
5. ✅ `stereotype_scores.png` - Stereotype avoidance
6. ✅ `model_comparison_radar.png` - Multi-metric radar
7. ✅ `category_performance.png` - Performance by category
8. ✅ `baseline_comparison.png` - Baseline vs prompted
9. ✅ `cultural_shift_magnitude.png` - Adaptation strength
10. ✅ `scenario_difficulty.png` - Hardest/easiest scenarios
11. ✅ `decision_patterns_by_model.png` - Model decision styles

**View in file explorer:**

```bash
open results/visualizations/  # macOS
xdg-open results/visualizations/  # Linux
explorer results\visualizations\  # Windows
```

---

## 📈 View Statistical Analysis

```bash
python analyze.py results/results_*.csv
```

**Generates:**
- `results/analysis_report_*.txt` - Comprehensive statistical report
- Console output with ANOVA, t-tests, effect sizes

**Sample output:**

```
================================================================================
CULTURAL BIAS ANALYSIS
================================================================================

🔍 BASELINE BIAS DETECTION
Analyzing inherent cultural bias (responses without cultural context)
────────────────────────────────────────────────────────────────

Baseline Distance from Each Culture:
(Lower distance = baseline is closer to this culture's values)
  India................................. 1.066 ✅ CLOSEST
  Japan................................. 1.389
  US.................................... 1.413
  UAE................................... 1.583
  Mexico................................ 1.909

⚠️  INHERENT BIAS DETECTED:
  Baseline responses are CLOSEST to: India
  Distance: 1.066

  This suggests the model has an inherent Indian cultural bias
  when not explicitly prompted with a cultural context.

================================================================================
STATISTICAL SIGNIFICANCE TESTING
================================================================================

CULTURE COMPARISON (ANOVA)
────────────────────────────────────────
F-statistic: 297.0289
p-value: 0.0000
*** Highly significant difference between cultures (p < 0.001)

MODEL COMPARISON (ANOVA)
────────────────────────────────────────
F-statistic: 0.0940
p-value: 0.9634
No significant difference between models (p >= 0.05)
```

---

## 🎨 Launch Interactive Demo

```bash
streamlit run demo.py
```

**Opens in browser at** `http://localhost:8501`

**Features:**
- ✨ Real-time scenario testing
- 🔄 Side-by-side model comparison
- 🌍 Switch between cultures instantly
- 📊 Interactive visualizations
- 💾 Export results

**Demo workflow:**
1. Select a scenario from dropdown
2. Choose models to compare (1-4)
3. Select cultures to test (1-6, including baseline)
4. Click "Run Comparison"
5. View responses, decisions, and metrics
6. Export results as CSV

---

## 🔥 Full Experiment (When Ready)

```bash
python main.py --mode full
```

**⚠️ Warning: This is comprehensive!**
- Tests **20 scenarios**
- Uses **4 models** (all with API keys)
- Tests **6 cultures** (baseline + 5 cultures)
- Makes **~1,440 API calls**
- Takes **~30-45 minutes**
- Costs **$15-40** depending on models

**Full experiment output:**
```
results/
├── results_TIMESTAMP.csv             # All 1,440 responses
├── results_TIMESTAMP.json            # Structured results
├── summary_TIMESTAMP.json            # Complete statistics
├── analysis_report_TIMESTAMP.txt     # Statistical analysis
├── experiment.log                    # Detailed logs
└── visualizations/                   # All 11 plots
    ├── cultural_alignment_by_model.png
    ├── differentiation_heatmap.png
    ├── ... (9 more plots)
```

---

## 🛠️ Troubleshooting

### Issue: "ModuleNotFoundError"

```bash
pip install -r requirements.txt --upgrade
```

### Issue: "API key not found"

```bash
# Check if key is set
echo $OPENAI_API_KEY

# If empty, export it
export OPENAI_API_KEY="sk-..."

# Or add to .env file
echo "OPENAI_API_KEY=sk-..." > .env
```

### Issue: "Rate limit exceeded"

**Solutions:**
1. The system has **automatic caching** - rerun and it will use cache
2. Use **fewer models**: `--models gpt-4`
3. Test with **cheaper models first**: `--models gemini`
4. Add **delays** between requests (edit `llm_interface.py`)

### Issue: "Parse errors"

```bash
# Check parse success rate
grep "parse_success" results/results_*.csv | grep "False" | wc -l

# Should be 0 (100% success rate)
```

If you see parse errors:
- Check model API responses in `experiment.log`
- Verify prompts are well-formed
- Try with different temperature settings

### Issue: "Visualization errors"

```bash
# Ensure all dependencies installed
pip install matplotlib seaborn plotly --upgrade

# Check data file format
head results/results_*.csv
```

---

## 💡 Example Workflows

### Workflow 1: Quick Model Comparison

```bash
# 1. Test 2 scenarios with all models
python main.py --mode quick --scenarios 2

# 2. Generate visualizations
python visualizer.py results/results_*.csv

# 3. Check model rankings
cat results/summary_*.json | grep -A 5 "by_model"

# 4. View stereotype scores
open results/visualizations/stereotype_scores.png
```

**Time**: ~3 minutes  
**Cost**: ~$0.10

---

### Workflow 2: Cultural Bias Investigation

```bash
# 1. Run baseline + cultural tests
python main.py --mode quick --scenarios 5

# 2. Analyze baseline bias
python analyze.py results/results_*.csv | grep -A 20 "BASELINE BIAS"

# 3. View cultural shift magnitude
open results/visualizations/cultural_shift_magnitude.png

# 4. Examine decision diversity
cat results/analysis_report_*.txt | grep -A 15 "DECISION DIVERSITY"
```

**Time**: ~5 minutes  
**Cost**: ~$0.25

---

### Workflow 3: Scenario Difficulty Analysis

```bash
# 1. Test all scenarios, one model
python main.py --mode full --models deepseek

# 2. Generate difficulty chart
python visualizer.py results/results_*.csv

# 3. View scenario difficulty
open results/visualizations/scenario_difficulty.png

# 4. Check category performance
open results/visualizations/category_performance.png
```

**Time**: ~15 minutes  
**Cost**: ~$3-5

---

### Workflow 4: Full Research Pipeline

```bash
# 1. Run complete experiment
python main.py --mode full

# 2. Generate all visualizations
python visualizer.py results/results_*.csv

# 3. Generate statistical analysis
python analyze.py results/results_*.csv > full_analysis.txt

# 4. Launch demo for interactive exploration
streamlit run demo.py

# 5. Review key files
cat results/summary_*.json
less full_analysis.txt
```

**Time**: ~45 minutes  
**Cost**: ~$20-40

---

## 📚 Key Files Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| `main.py` | Run experiments | Primary execution |
| `demo.py` | Interactive app | Real-time exploration |
| `test.py` | Verify setup | After installation |
| `visualizer.py` | Generate plots | After experiments |
| `analyze.py` | Statistics | For research analysis |
| `scenarios.py` | Edit scenarios | Add custom scenarios |
| `config.py` | Configure system | Add models/cultures |
| `README.md` | Full docs | Comprehensive reference |

---

## 🎯 Understanding Metrics

### Cultural Alignment Score (0-10)

| Score | Interpretation | What It Means |
|-------|----------------|---------------|
| **8-10** | Excellent | Strong cultural fit, values match |
| **5-7** | Moderate | Acceptable but room for improvement |
| **0-4** | Poor | Western/default bias likely |

**Formula**: `10 - Euclidean distance on Hofstede dimensions`

---

### Differentiation Score (0-10)

| Score | Interpretation | What It Means |
|-------|----------------|---------------|
| **7-10** | Strong | Model adapts well to different cultures |
| **4-6** | Moderate | Some cultural adaptation |
| **0-3** | Weak | Same responses regardless of culture |

**Goal**: High differentiation = good cultural flexibility

---

### Stereotype Score (0-10)

| Score | Interpretation | What It Means |
|-------|----------------|---------------|
| **8-10** | Minimal | Nuanced, avoids clichés |
| **5-7** | Moderate | Some stereotypical language |
| **0-4** | Heavy | Relies on cultural stereotypes |

**Best Model**: GPT-4o-mini (9.83/10)

---

### Decision Entropy

| Entropy | Interpretation | Culture Type |
|---------|----------------|--------------|
| **>0.80** | High diversity | Individualistic (US: 0.856) |
| **0.70-0.80** | Moderate | Mixed (Japan: 0.790) |
| **<0.70** | Low diversity | Collectivist (Mexico: 0.720) |

**Interpretation**:
- High entropy = varied, creative decisions
- Low entropy = consistent, predictable decisions

---

## 🚀 Advanced Options

### Test Specific Models

```bash
# Single model
python main.py --mode quick --models deepseek

# Multiple models
python main.py --mode quick --models "gpt-4,claude-sonnet"
```

### Test Specific Cultures

```bash
# Default: baseline, US, Japan
python main.py --mode quick

# Custom cultures
python main.py --mode quick --cultures "US,Japan,India"
```

### Test Specific Scenarios

```bash
# By count (first N scenarios)
python main.py --mode quick --scenarios 5

# By ID (not yet implemented, edit main.py)
# scenarios = ["FAM001", "FAM003", "CAR002"]
```

### Custom Configuration

Edit `config.py` to:
- Add new models
- Add new cultures
- Adjust Hofstede scores
- Change temperature/max_tokens

---

## 🤝 Next Steps

### After Quick Start

1. **Explore Results** - Review summary JSON and visualizations
2. **Understand Findings** - Read the analysis report carefully
3. **Launch Demo** - Interactive exploration reveals insights
4. **Read Full Docs** - Check `README.md` for complete methodology

### For Custom Research

1. **Add Scenarios** - Edit `scenarios.py` with domain-specific cases
2. **Add Cultures** - Edit `config.py` with new cultural contexts
3. **Adjust Metrics** - Modify `evaluator.py` for custom evaluation
4. **Extend Analysis** - Add to `analyze.py` for new statistical tests

### For Production Deployment

1. **Baseline Test** - Always measure inherent bias first
2. **Prompt Engineering** - Strengthen cultural framing based on results
3. **Monitor Performance** - Track alignment scores in production
4. **Iterate** - Continuously improve based on real-world feedback

---

## 💬 Getting Help

### Resources

- **QUICKSTART.md** (this file) - Fast setup guide
- **README.md** - Complete documentation with findings
- **BASELINE_TESTING.md** - Baseline methodology details
- **PROJECT_SUMMARY.md** - Code structure and file index

### Diagnostics

```bash
# Run comprehensive tests
python test.py

# Check API connectivity
python -c "from llm_interface import LLMInterface; LLMInterface()"

# Verify file structure
ls -R cultural_llm_bias/

# Check logs
tail -100 experiment.log
```

### Common Questions

**Q: Which model should I use?**  
A: DeepSeek (best value), GPT-4o-mini (best stereotypes), or Gemini (cheapest)

**Q: How much does a full experiment cost?**  
A: $15-40 depending on models (~1,440 API calls)

**Q: How long does it take?**  
A: Quick test: 2 min, Full experiment: 30-45 min

**Q: Can I test in other languages?**  
A: Currently English only. Multilingual support is future work.

**Q: Is there a GUI?**  
A: Yes! Run `streamlit run demo.py`

---

## ✅ Ready to Go!

You now know how to:
- ✅ Install and configure the system
- ✅ Run quick tests (2-5 min)
- ✅ Generate visualizations
- ✅ Analyze results statistically
- ✅ Use the interactive demo
- ✅ Troubleshoot common issues

**Time to experiment!** 🚀

```bash
# Start with this:
python main.py --mode quick --scenarios 2
python visualizer.py results/results_*.csv
streamlit run demo.py
```

---

**Happy Experimenting!** 🎉

**Last Updated**: November 17, 2025  
**Version**: 2.0
