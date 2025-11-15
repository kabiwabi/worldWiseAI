"""
Configuration file for Cultural LLM Bias Measurement Project
Contains all constants, API keys, and system settings
"""

import os
from pathlib import Path
from typing import Dict, List
from dotenv import load_dotenv  # Add this import

# Load environment variables from .env file
load_dotenv()  # Add this line

# ============================================================================
# PROJECT PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
VISUALIZATIONS_DIR = RESULTS_DIR / "visualizations"
CACHE_DIR = PROJECT_ROOT / "cache"

# Create directories if they don't exist
for directory in [DATA_DIR, RESULTS_DIR, VISUALIZATIONS_DIR, CACHE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# API KEYS (Set as environment variables)
# ============================================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# ============================================================================
# MODEL CONFIGURATIONS
# ============================================================================

MODELS = {
    "gpt-4": {
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        "max_tokens": 500,
        "temperature": 0.7,
    },
    "claude-sonnet": {
        "provider": "anthropic",
        "model_name": "claude-3-5-haiku-20241022",
        "max_tokens": 500,
        "temperature": 0.7,
    },
    "gemini": {
        "provider": "google",
        "model_name": "gemini-2.5-flash-lite",
        "max_tokens": 500,
        "temperature": 0.7,
    },
}

# ============================================================================
# CULTURAL CONTEXTS
# ============================================================================

CULTURAL_CONTEXTS = {
    "baseline": {
        "name": "Baseline (No Cultural Context)",
        "location": "No specific location",
        "description": "neutral",
        "hofstede_scores": {
            "individualism": 0.0,
            "power_distance": 0.0,
            "masculinity": 0.0,
            "uncertainty_avoidance": 0.0,
            "long_term_orientation": 0.0,
            "indulgence": 0.0,
        }
    },
    "US": {
        "name": "United States",
        "location": "Austin, Texas, USA",
        "description": "American",
        "hofstede_scores": {
            "individualism": 2.0,
            "power_distance": -1.0,
            "masculinity": 1.0,
            "uncertainty_avoidance": -0.5,
            "long_term_orientation": 0.0,
            "indulgence": 1.5,
        }
    },
    "Japan": {
        "name": "Japan",
        "location": "Tokyo, Japan",
        "description": "Japanese",
        "hofstede_scores": {
            "individualism": -1.0,
            "power_distance": 1.0,
            "masculinity": 2.0,
            "uncertainty_avoidance": 2.0,
            "long_term_orientation": 2.0,
            "indulgence": -1.5,
        }
    },
    "India": {
        "name": "India",
        "location": "New Delhi, India",
        "description": "Indian",
        "hofstede_scores": {
            "individualism": -1.5,
            "power_distance": 2.0,
            "masculinity": 1.0,
            "uncertainty_avoidance": 0.5,
            "long_term_orientation": 1.0,
            "indulgence": 0.0,
        }
    },
    "Mexico": {
        "name": "Mexico",
        "location": "Mexico City, Mexico",
        "description": "Mexican",
        "hofstede_scores": {
            "individualism": -1.0,
            "power_distance": 2.0,
            "masculinity": 1.0,
            "uncertainty_avoidance": 1.5,
            "long_term_orientation": 0.0,
            "indulgence": 1.0,
        }
    },
    "UAE": {
        "name": "United Arab Emirates",
        "location": "Dubai, UAE",
        "description": "Emirati",
        "hofstede_scores": {
            "individualism": -1.0,
            "power_distance": 2.0,
            "masculinity": 1.0,
            "uncertainty_avoidance": 1.0,
            "long_term_orientation": 0.5,
            "indulgence": -1.0,
        }
    },
}

# ============================================================================
# CULTURAL DIMENSIONS
# ============================================================================

CULTURAL_DIMENSIONS = [
    "individualism",
    "power_distance",
    "masculinity",
    "uncertainty_avoidance",
    "long_term_orientation",
    "indulgence",
]

VALUE_OPTIONS = [
    "Individual Freedom",
    "Family Harmony",
    "Professional Success",
    "Social Acceptance",
    "Personal Happiness",
    "Duty/Obligation",
    "Financial Security",
    "Group Consensus",
]

DECISION_OPTIONS = [
    "Option A",
    "Option B",
    "Compromise",
    "Decline/Abstain",
]

# ============================================================================
# EXPERIMENT SETTINGS
# ============================================================================

NUM_RUNS_PER_COMBINATION = 3
ENABLE_CACHE = True

# ============================================================================
# EVALUATION SETTINGS
# ============================================================================

JUDGE_MODEL = "gpt-4"
JUDGE_TEMPERATURE = 0.3

STEREOTYPE_INDICATORS = [
    "always", "never", "all people", "everyone", "typical",
    "stereotypical", "generally", "usually", "tend to",
]

# ============================================================================
# VISUALIZATION SETTINGS
# ============================================================================

COLORS = {
    "baseline": "#808080",  # Gray for baseline
    "US": "#1f77b4",
    "Japan": "#ff7f0e",
    "India": "#2ca02c",
    "Mexico": "#d62728",
    "UAE": "#9467bd",
}

FIGURE_DPI = 300
FIGURE_SIZE = (12, 8)
