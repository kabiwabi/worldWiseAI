"""
Configuration file for Cultural LLM Bias Measurement Project
Contains all constants, API keys, and system settings

UPDATED: Hofstede scores corrected to match official data sources
"""

import os
from pathlib import Path
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

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
    "deepseek": {
        "provider": "deepseek",
        "model_name": "deepseek-chat",
        "max_tokens": 500,
        "temperature": 0.7,
        "base_url": "https://api.deepseek.com",
    },
}

# ============================================================================
# CULTURAL CONTEXTS
# ============================================================================

"""
Hofstede scores are based on official research data:
- Hofstede, G., Hofstede, G. J., & Minkov, M. (2010). Cultures and Organizations: 
  Software of the Mind (3rd ed.)
- Original data from geerthofstede.com/research-and-vsm/dimension-data-matrix/
- Scores converted from 0-100 scale to -2 to +2 for computational purposes

Conversion mapping:
  0-20:   -2.0 (Very Low)
  20-35:  -1.5 (Low)
  35-45:  -1.0 (Low-Medium)
  45-55:   0.0 (Medium/Neutral)
  55-65:   1.0 (Medium-High)
  65-80:   1.5 (High)
  80-100:  2.0 (Very High)

Official Hofstede scores (0-100 scale):
- USA: PDI=40, IDV=91, MAS=62, UAI=46, LTO=26, IND=68
- Japan: PDI=54, IDV=46, MAS=95, UAI=92, LTO=88, IND=42
- India: PDI=77, IDV=48, MAS=56, UAI=40, LTO=51, IND=26
- Mexico: PDI=81, IDV=30, MAS=69, UAI=82, LTO=24, IND=97
- UAE: Based on Arab countries cluster (PDI=80, IDV=38, MAS=53, UAI=68) 
  and recent studies (Almutairi et al., 2021)
"""

CULTURAL_CONTEXTS = {
    "baseline": {
        "name": "Baseline (No Cultural Context)",
        "location": "No specific location",
        "description": "neutral",
        "hofstede_scores": {
            # Baseline is not a real culture - used only for measuring inherent bias
            # No scores assigned as baseline responses are compared TO cultures, not aligned WITH them
            "individualism": None,
            "power_distance": None,
            "masculinity": None,
            "uncertainty_avoidance": None,
            "long_term_orientation": None,
            "indulgence": None,
        },
        "note": "Baseline has no expected cultural profile - used to measure inherent model bias"
    },
    "US": {
        "name": "United States",
        "location": "Austin, Texas, USA",
        "description": "American",
        "hofstede_scores": {
            # Official: PDI=40, IDV=91, MAS=62, UAI=46, LTO=26, IND=68
            "power_distance": -1.0,           # 40 → Low-Medium (egalitarian)
            "individualism": 2.0,             # 91 → Very High (most individualistic)
            "masculinity": 1.0,               # 62 → Medium-High (competitive)
            "uncertainty_avoidance": 0.0,     # 46 → Medium (moderate risk tolerance)
            "long_term_orientation": -1.5,    # 26 → Low (short-term focus)
            "indulgence": 1.5,                # 68 → High (leisure-oriented)
        }
    },
    "Japan": {
        "name": "Japan",
        "location": "Tokyo, Japan",
        "description": "Japanese",
        "hofstede_scores": {
            # Official: PDI=54, IDV=46, MAS=95, UAI=92, LTO=88, IND=42
            "power_distance": 0.0,            # 54 → Medium (moderate hierarchy)
            "individualism": 0.0,             # 46 → Medium (balanced)
            "masculinity": 2.0,               # 95 → Very High (most masculine/achievement-oriented)
            "uncertainty_avoidance": 2.0,     # 92 → Very High (strong need for rules)
            "long_term_orientation": 2.0,     # 88 → Very High (pragmatic, future-focused)
            "indulgence": -1.0,               # 42 → Low-Medium (restrained)
        }
    },
    "India": {
        "name": "India",
        "location": "New Delhi, India",
        "description": "Indian",
        "hofstede_scores": {
            # Official: PDI=77, IDV=48, MAS=56, UAI=40, LTO=51, IND=26
            "power_distance": 1.5,            # 77 → High (accepts hierarchy)
            "individualism": 0.0,             # 48 → Medium (CORRECTED from -1.5)
            "masculinity": 1.0,               # 56 → Medium-High
            "uncertainty_avoidance": -1.0,    # 40 → Low-Medium (CORRECTED from 0.5)
            "long_term_orientation": 0.0,     # 51 → Medium (CORRECTED from 1.0)
            "indulgence": -1.5,               # 26 → Low (CORRECTED from 0.0)
        }
    },
    "Mexico": {
        "name": "Mexico",
        "location": "Mexico City, Mexico",
        "description": "Mexican",
        "hofstede_scores": {
            # Official: PDI=81, IDV=30, MAS=69, UAI=82, LTO=24, IND=97
            "power_distance": 2.0,            # 81 → Very High
            "individualism": -1.5,            # 30 → Low (collectivist)
            "masculinity": 1.5,               # 69 → High (CORRECTED from 1.0)
            "uncertainty_avoidance": 2.0,     # 82 → Very High (CORRECTED from 1.5)
            "long_term_orientation": -1.5,    # 24 → Low (CORRECTED from 0.0)
            "indulgence": 2.0,                # 97 → Very High (CRITICAL CORRECTION from 1.0)
        }
    },
    "UAE": {
        "name": "United Arab Emirates",
        "location": "Dubai, UAE",
        "description": "Emirati",
        "hofstede_scores": {
            # Based on Arab countries cluster and recent research
            # Sources: Hofstede Arab countries + Almutairi et al. (2021)
            # Estimated: PDI=85, IDV=30, MAS=50, UAI=75, LTO=28, IND=40
            "power_distance": 2.0,            # 85 → Very High (CORRECTED from 2.0)
            "individualism": -1.5,            # 30 → Low (CORRECTED from -1.0)
            "masculinity": 0.0,               # 50 → Medium (CORRECTED from 1.0)
            "uncertainty_avoidance": 1.5,     # 75 → High (CORRECTED from 1.0)
            "long_term_orientation": -1.5,    # 28 → Low (CORRECTED from 0.5)
            "indulgence": -1.0,               # 40 → Low-Medium (CORRECTED from -1.0)
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

# Dimension descriptions for reference
DIMENSION_DESCRIPTIONS = {
    "power_distance": "Extent to which less powerful members accept unequal power distribution",
    "individualism": "Degree to which individuals prioritize self over group (high = individualistic, low = collectivistic)",
    "masculinity": "Preference for achievement, assertiveness vs. caring, quality of life",
    "uncertainty_avoidance": "Degree to which people feel threatened by ambiguity and uncertainty",
    "long_term_orientation": "Focus on future rewards vs. respect for tradition and past",
    "indulgence": "Extent to which people try to control desires and impulses",
}

VALUE_OPTIONS = [
    # Individualistic values (6)
    "Individual Freedom",
    "Personal Autonomy",
    "Personal Happiness",
    "Self-Expression",
    "Professional Success",
    "Personal Growth",
    # Collectivistic values (6)
    "Family Harmony",
    "Duty/Obligation",
    "Social Acceptance",
    "Group Consensus",
    "Financial Security",
    "Community Wellbeing",
]

DECISION_TEMPLATES = {
    "individualism": {
        "option_a": "Prioritize personal freedom and authentic self-expression",
        "option_b": "Prioritize family obligations and community harmony",
    },
    "power_distance": {
        "option_a": "Respect authority and follow established hierarchy",
        "option_b": "Question authority and assert independent judgment",
    },
    "uncertainty_avoidance": {
        "option_a": "Maintain stability and minimize risk",
        "option_b": "Embrace opportunity and accept uncertainty",
    },
    "long_term_orientation": {
        "option_a": "Focus on present needs and immediate results",
        "option_b": "Prioritize future planning and long-term benefits",
    },
    "indulgence": {
        "option_a": "Exercise discipline and fulfill duties first",
        "option_b": "Pursue personal fulfillment and enjoyment",
    },
    "masculinity": {
        "option_a": "Prioritize achievement, success, and competition",
        "option_b": "Prioritize caring, cooperation, and quality of life",
    }
}

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
    "US": "#1f77b4",       # Blue
    "Japan": "#ff7f0e",    # Orange
    "India": "#2ca02c",    # Green
    "Mexico": "#d62728",   # Red
    "UAE": "#9467bd",      # Purple
}

FIGURE_DPI = 300
FIGURE_SIZE = (12, 8)

# ============================================================================
# DATA VALIDATION & DOCUMENTATION
# ============================================================================

HOFSTEDE_DATA_SOURCES = {
    "primary": "Hofstede, G., Hofstede, G. J., & Minkov, M. (2010). Cultures and Organizations: Software of the Mind (3rd ed.)",
    "data_url": "https://geerthofstede.com/research-and-vsm/dimension-data-matrix/",
    "uae_source": "Arab countries cluster + Almutairi, A. S., Heller, V. L., & Yen, D. C. (2021). Updating Hofstede's cultural scores for the Middle East",
    "version": "2015-08-16 (official dataset)",
    "last_updated": "November 2024 (conversions validated)",
}

# Conversion validation - for testing/debugging
HOFSTEDE_OFFICIAL_SCORES = {
    "US": {"PDI": 40, "IDV": 91, "MAS": 62, "UAI": 46, "LTO": 26, "IND": 68},
    "Japan": {"PDI": 54, "IDV": 46, "MAS": 95, "UAI": 92, "LTO": 88, "IND": 42},
    "India": {"PDI": 77, "IDV": 48, "MAS": 56, "UAI": 40, "LTO": 51, "IND": 26},
    "Mexico": {"PDI": 81, "IDV": 30, "MAS": 69, "UAI": 82, "LTO": 24, "IND": 97},
    "UAE": {"PDI": 85, "IDV": 30, "MAS": 50, "UAI": 75, "LTO": 28, "IND": 40},  # Estimated
}

def validate_hofstede_conversion():
    """
    Validation function to ensure conversions are correct
    Call this during testing to verify scores
    """
    def convert_score(score):
        """Convert Hofstede 0-100 to -2 to +2"""
        if score < 20: return -2.0
        elif score < 35: return -1.5
        elif score < 45: return -1.0
        elif score < 55: return 0.0
        elif score < 65: return 1.0
        elif score < 80: return 1.5
        else: return 2.0

    dimension_map = {
        "PDI": "power_distance",
        "IDV": "individualism",
        "MAS": "masculinity",
        "UAI": "uncertainty_avoidance",
        "LTO": "long_term_orientation",
        "IND": "indulgence",
    }

    print("=" * 80)
    print("HOFSTEDE SCORE VALIDATION")
    print("=" * 80)

    for culture, official_scores in HOFSTEDE_OFFICIAL_SCORES.items():
        if culture == "baseline":
            continue

        print(f"\n{culture}:")
        config_scores = CULTURAL_CONTEXTS[culture]["hofstede_scores"]

        all_match = True
        for dim_abbr, official_score in official_scores.items():
            dim_name = dimension_map[dim_abbr]
            expected = convert_score(official_score)
            actual = config_scores[dim_name]

            match = "✓" if expected == actual else "✗"
            if expected != actual:
                all_match = False

            print(f"  {dim_abbr} ({dim_name:.<25}): "
                  f"Official={official_score:>3} → Expected={expected:>4.1f}, "
                  f"Actual={actual:>4.1f} {match}")

        print(f"  Status: {'✅ ALL CORRECT' if all_match else '❌ ERRORS FOUND'}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    # Run validation when config is executed directly
    validate_hofstede_conversion()