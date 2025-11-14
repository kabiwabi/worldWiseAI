# Quick Start Guide

Get up and running with the Cultural Bias Measurement System in 5 minutes!

## ⚡ 5-Minute Setup

### 1. Install Dependencies

```bash
cd cultural_llm_bias
pip install -r requirements.txt
```

### 2. Set API Keys

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."
```

### 3. Run Tests

```bash
python test.py
```

You should see: ✅ PASS for all tests except API Keys (if you haven't set them yet)

### 4. Run a Quick Test

```bash
python main.py --mode quick --scenarios 2
```

This will:
- Test 2 scenarios
- With GPT-4 only
- Across US and Japan cultures
- Generate results in `results/`

### 5. View Results

```bash
ls -lh results/
```

You'll see:
- `results_TIMESTAMP.csv` - Raw data
- `results_TIMESTAMP.json` - Structured results  
- `summary_TIMESTAMP.json` - Summary statistics

## 📊 Generate Visualizations

```bash
python visualizer.py results/results_TIMESTAMP.csv
```

View generated plots in `results/visualizations/`

## 🎨 Launch Interactive Demo

```bash
streamlit run demo.py
```

Opens in browser at `http://localhost:8501`

## 🔥 Full Experiment

When ready to run the complete experiment:

```bash
python main.py --mode full
```

**Warning**: This will make ~900 API calls and may cost $20-40 depending on which models you use.

## 🛠️ Troubleshooting

### "ModuleNotFoundError"

```bash
pip install -r requirements.txt --upgrade
```

### "API key not found"

Make sure you've exported the environment variables:

```bash
export OPENAI_API_KEY="your-key"
# Add to ~/.bashrc or ~/.zshrc to persist
echo 'export OPENAI_API_KEY="your-key"' >> ~/.bashrc
```

### "Rate limit exceeded"

The system has caching enabled by default. If you still hit rate limits:
1. Add delays between requests
2. Use fewer models for testing
3. Test with cheaper models first (Gemini is cheapest)

## 📝 Next Steps

- Edit `scenarios.py` to add your own scenarios
- Edit `config.py` to add new cultures or models  
- Explore the codebase - every file is documented
- Check `README.md` for full documentation

## 💡 Example Workflow

```bash
# 1. Quick test with 2 scenarios
python main.py --mode quick --scenarios 2

# 2. Generate visualizations
python visualizer.py results/results_*.csv

# 3. Review results
cat results/summary_*.json

# 4. Launch demo for interactive exploration
streamlit run demo.py

# 5. When satisfied, run full experiment
python main.py --mode full
```

## 📚 Key Files

- `main.py` - Run experiments
- `demo.py` - Interactive demo
- `test.py` - Verify installation
- `scenarios.py` - Edit scenarios here
- `config.py` - Configure models/cultures
- `README.md` - Full documentation

## 🎯 Understanding Results

### Cultural Alignment Score (0-10)
- **8-10**: Excellent alignment with expected cultural values
- **5-7**: Moderate alignment
- **0-4**: Poor alignment (likely Western bias)

### Differentiation Score (0-10)
- **7-10**: Strong cultural differentiation
- **4-6**: Moderate differentiation
- **0-3**: Weak differentiation (model gives similar responses regardless of culture)

### Stereotype Score (0-10)
- **8-10**: Minimal stereotyping
- **5-7**: Moderate stereotyping
- **0-4**: Heavy reliance on stereotypes

## 🤝 Need Help?

- Check `README.md` for detailed documentation
- Run `python test.py` to diagnose issues
- Review logs in `experiment.log`

Happy experimenting! 🚀
