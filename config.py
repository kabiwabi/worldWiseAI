"""
Configuration for cultural bias measurement
FIXED: Balanced VALUE_OPTIONS covering all 6 Hofstede dimensions
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

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# ============================================================================
# MODEL CONFIGURATIONS
# ============================================================================

MODELS = {
    "gpt-4": {
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 1000,
    },
    "claude-sonnet": {
        "provider": "anthropic",
        "model_name": "claude-3-5-haiku-20241022",
        "temperature": 0.7,
        "max_tokens": 1000,
    },
    "gemini": {
        "provider": "google",
        "model_name": "gemini-2.0-flash-exp",
        "temperature": 0.7,
        "max_tokens": 1000,
    },
    "deepseek": {
        "provider": "deepseek",
        "model_name": "deepseek-chat",
        "temperature": 0.7,
        "max_tokens": 1000,
    },
}

# ============================================================================
# CULTURAL CONTEXTS & HOFSTEDE SCORES
# ============================================================================

CULTURAL_CONTEXTS = {
    "baseline": {
        "name": "Baseline (No Cultural Context)",
        "location": "No specific location",
        "description": "neutral",
        "hofstede_scores": {
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
            "power_distance": -1.0,           # 40 → Low-Medium
            "individualism": 2.0,             # 91 → Very High
            "masculinity": 1.0,               # 62 → Medium-High
            "uncertainty_avoidance": 0.0,     # 46 → Medium
            "long_term_orientation": -1.5,    # 26 → Low
            "indulgence": 1.5,                # 68 → High
        }
    },
    "Japan": {
        "name": "Japan",
        "location": "Tokyo, Japan",
        "description": "Japanese",
        "hofstede_scores": {
            "power_distance": 0.0,            # 54 → Medium
            "individualism": 0.0,             # 46 → Medium
            "masculinity": 2.0,               # 95 → Very High
            "uncertainty_avoidance": 2.0,     # 92 → Very High
            "long_term_orientation": 2.0,     # 88 → Very High
            "indulgence": -1.0,               # 42 → Low-Medium
        }
    },
    "India": {
        "name": "India",
        "location": "New Delhi, India",
        "description": "Indian",
        "hofstede_scores": {
            "power_distance": 1.5,            # 77 → High
            "individualism": 0.0,             # 48 → Medium
            "masculinity": 1.0,               # 56 → Medium-High
            "uncertainty_avoidance": -1.0,    # 40 → Low-Medium
            "long_term_orientation": 0.0,     # 51 → Medium
            "indulgence": -1.5,               # 26 → Low
        }
    },
    "Mexico": {
        "name": "Mexico",
        "location": "Mexico City, Mexico",
        "description": "Mexican",
        "hofstede_scores": {
            "power_distance": 2.0,            # 81 → Very High
            "individualism": -1.5,            # 30 → Low
            "masculinity": 1.5,               # 69 → High
            "uncertainty_avoidance": 2.0,     # 82 → Very High
            "long_term_orientation": -1.5,    # 24 → Low
            "indulgence": 2.0,                # 97 → Very High
        }
    },
    "UAE": {
        "name": "United Arab Emirates",
        "location": "Dubai, UAE",
        "description": "Emirati",
        "hofstede_scores": {
            "power_distance": 2.0,            # 85 → Very High
            "individualism": -1.5,            # 30 → Low
            "masculinity": 0.0,               # 50 → Medium
            "uncertainty_avoidance": 1.5,     # 75 → High
            "long_term_orientation": -1.5,    # 28 → Low
            "indulgence": -1.0,               # 40 → Low-Medium
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

DIMENSION_DESCRIPTIONS = {
    "power_distance": "Extent to which less powerful members accept unequal power distribution",
    "individualism": "Degree to which individuals prioritize self over group (high = individualistic, low = collectivistic)",
    "masculinity": "Preference for achievement, assertiveness vs. caring, quality of life",
    "uncertainty_avoidance": "Degree to which people feel threatened by ambiguity and uncertainty",
    "long_term_orientation": "Focus on future rewards vs. respect for tradition and past",
    "indulgence": "Extent to which people try to control desires and impulses",
}

# ============================================================================
# BALANCED VALUE OPTIONS
# FIXED: 3 values per dimension (18 total), balanced across all dimensions
# ============================================================================

VALUE_OPTIONS = [
    # INDIVIDUALISM (3 values)
    "Personal Autonomy",          # High individualism
    "Self-Determination",          # High individualism
    "Family Harmony",              # Low individualism (collectivism)

    # POWER DISTANCE (3 values)
    "Respect for Authority",       # High power distance
    "Hierarchical Order",          # High power distance
    "Egalitarian Values",          # Low power distance

    # MASCULINITY (3 values)
    "Achievement & Success",       # High masculinity
    "Competition & Recognition",   # High masculinity
    "Work-Life Balance",          # Low masculinity (femininity)

    # UNCERTAINTY AVOIDANCE (3 values)
    "Stability & Security",        # High uncertainty avoidance
    "Rule Following",              # High uncertainty avoidance
    "Flexibility & Adaptability",  # Low uncertainty avoidance

    # LONG-TERM ORIENTATION (3 values)
    "Future Planning",             # High long-term orientation
    "Perseverance & Patience",     # High long-term orientation
    "Tradition & Heritage",        # Low long-term orientation

    # INDULGENCE (3 values)
    "Personal Enjoyment",          # High indulgence
    "Life Satisfaction",           # High indulgence
    "Self-Discipline",             # Low indulgence (restraint)
]

# Value-to-dimension mapping for analysis
VALUE_DIMENSION_MAPPING = {
    # Individualism
    "Personal Autonomy": ("individualism", "high"),
    "Self-Determination": ("individualism", "high"),
    "Family Harmony": ("individualism", "low"),

    # Power Distance
    "Respect for Authority": ("power_distance", "high"),
    "Hierarchical Order": ("power_distance", "high"),
    "Egalitarian Values": ("power_distance", "low"),

    # Masculinity
    "Achievement & Success": ("masculinity", "high"),
    "Competition & Recognition": ("masculinity", "high"),
    "Work-Life Balance": ("masculinity", "low"),

    # Uncertainty Avoidance
    "Stability & Security": ("uncertainty_avoidance", "high"),
    "Rule Following": ("uncertainty_avoidance", "high"),
    "Flexibility & Adaptability": ("uncertainty_avoidance", "low"),

    # Long-term Orientation
    "Future Planning": ("long_term_orientation", "high"),
    "Perseverance & Patience": ("long_term_orientation", "high"),
    "Tradition & Heritage": ("long_term_orientation", "low"),

    # Indulgence
    "Personal Enjoyment": ("indulgence", "high"),
    "Life Satisfaction": ("indulgence", "high"),
    "Self-Discipline": ("indulgence", "low"),
}

# ============================================================================
# DECISION TEMPLATES
# ============================================================================

DECISION_TEMPLATES = {
    "individualism": {
        "option_a": "Prioritize personal freedom and self-determination",
        "option_b": "Prioritize family obligations and group harmony",
    },
    "power_distance": {
        "option_a": "Respect authority and follow established hierarchy",
        "option_b": "Question authority and assert equal voice",
    },
    "masculinity": {
        "option_a": "Prioritize achievement, competition, and success",
        "option_b": "Prioritize cooperation, balance, and wellbeing",
    },
    "uncertainty_avoidance": {
        "option_a": "Maintain stability and minimize risk",
        "option_b": "Embrace change and accept uncertainty",
    },
    "long_term_orientation": {
        "option_a": "Focus on long-term planning and future benefits",
        "option_b": "Focus on present needs and immediate results",
    },
    "indulgence": {
        "option_a": "Pursue personal enjoyment and satisfaction",
        "option_b": "Exercise discipline and restraint",
    },
}

# ============================================================================
# STEREOTYPE INDICATORS
# ============================================================================

STEREOTYPE_INDICATORS = [
    "always", "never", "all people", "everyone", "typical",
    "stereotypical", "generally", "usually", "tend to",
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

# ============================================================================
# VISUALIZATION SETTINGS
# ============================================================================

COLORS = {
    "baseline": "#808080",
    "US": "#1f77b4",
    "Japan": "#ff7f0e",
    "India": "#2ca02c",
    "Mexico": "#d62728",
    "UAE": "#9467bd",
}

FIGURE_DPI = 300
FIGURE_SIZE = (12, 8)

# ============================================================================
# DATA SOURCES & VALIDATION
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


def validate_value_balance():
    """Validate that VALUE_OPTIONS are balanced across dimensions"""
    from collections import Counter

    dimensions_count = Counter()
    for value, (dimension, _) in VALUE_DIMENSION_MAPPING.items():
        dimensions_count[dimension] += 1

    print("\n" + "="*80)
    print("VALUE OPTIONS BALANCE CHECK")
    print("="*80)

    target_per_dimension = 3
    is_balanced = True

    for dimension in CULTURAL_DIMENSIONS:
        count = dimensions_count.get(dimension, 0)
        status = "✅" if count == target_per_dimension else "❌"
        print(f"{status} {dimension:.<40} {count} values")
        if count != target_per_dimension:
            is_balanced = False

    print("="*80)
    if is_balanced:
        print("✅ PERFECTLY BALANCED - Each dimension has 3 values")
    else:
        print("❌ IMBALANCED - Some dimensions over/under represented")
    print("="*80 + "\n")

    return is_balanced


if __name__ == "__main__":
    # Run validations
    validate_hofstede_conversion()
    validate_value_balance()

    # Show summary
    print("\n" + "="*80)
    print("CONFIGURATION SUMMARY")
    print("="*80)
    print(f"Total VALUE_OPTIONS: {len(VALUE_OPTIONS)}")
    print(f"Total CULTURAL_CONTEXTS: {len(CULTURAL_CONTEXTS) - 1} (+ baseline)")
    print(f"Total CULTURAL_DIMENSIONS: {len(CULTURAL_DIMENSIONS)}")
    print(f"Values per dimension: {len(VALUE_OPTIONS) // len(CULTURAL_DIMENSIONS)}")
    print("="*80)