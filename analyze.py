"""
Analysis Script
Analyzes experiment results and generates insights
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from scipy import stats
import sys


def load_results(results_file: Path) -> pd.DataFrame:
    """Load results from CSV"""
    print(f"Loading results from {results_file}")
    df = pd.read_csv(results_file)
    
    # Convert string lists to actual lists
    if 'top_values' in df.columns:
        df['top_values'] = df['top_values'].apply(
            lambda x: eval(x) if isinstance(x, str) and x.startswith('[') else []
        )
    
    return df


def analyze_cultural_bias(df: pd.DataFrame):
    """Analyze overall cultural bias in models"""
    print("\n" + "=" * 80)
    print("CULTURAL BIAS ANALYSIS")
    print("=" * 80)
    
    # Check if baseline exists
    has_baseline = 'baseline' in df['culture'].unique()
    
    if has_baseline:
        print("\n🔍 BASELINE BIAS DETECTION")
        print("Analyzing inherent cultural bias (responses without cultural context)")
        print("-" * 80)
        
        baseline_data = df[df['culture'] == 'baseline']
        non_baseline_data = df[df['culture'] != 'baseline']
        
        # Calculate baseline profile and compare to each culture
        from evaluator import calculate_baseline_bias
        from response_parser import ParsedResponse
        import config
        
        baseline_responses = []
        for _, row in baseline_data.iterrows():
            baseline_responses.append(ParsedResponse(
                raw_text=row['raw_response'],
                explanation=row['explanation'],
                decision=row.get('decision'),
                top_values=eval(row.get('top_values', '[]')) if isinstance(row.get('top_values'), str) else row.get('top_values', []),
                parse_success=row['parse_success'],
                parse_errors=[]
            ))
        
        if baseline_responses:
            # Get dimensions
            from scenarios import get_scenario_by_id
            all_dimensions = set()
            for sid in df['scenario_id'].unique():
                scenario = get_scenario_by_id(sid)
                if scenario:
                    all_dimensions.update(scenario.cultural_dimensions)
            
            baseline_distances = calculate_baseline_bias(
                baseline_responses,
                config.CULTURAL_CONTEXTS,
                list(all_dimensions)
            )
            
            if baseline_distances:
                # Sort by distance (ascending)
                sorted_distances = sorted(baseline_distances.items(), key=lambda x: x[1])
                
                print("\nBaseline Distance from Each Culture:")
                print("(Lower distance = baseline is closer to this culture's values)")
                for culture, distance in sorted_distances:
                    print(f"  {culture:.<30} {distance:.3f}")
                
                closest = sorted_distances[0]
                print(f"\n⚠️  INHERENT BIAS DETECTED:")
                print(f"  Baseline responses are CLOSEST to: {closest[0]}")
                print(f"  Distance: {closest[1]:.3f}")
                print(f"\n  This suggests the model has an inherent {closest[0]} cultural bias")
                print(f"  when not explicitly prompted with a cultural context.")
    
    # Calculate mean alignment per culture (excluding baseline)
    culture_data = df[df['culture'] != 'baseline'] if has_baseline else df
    culture_alignment = culture_data.groupby('culture')['cultural_alignment'].mean().sort_values(ascending=False)
    
    print("\n\nCultural Alignment by Culture (WITH cultural prompting):")
    for culture, score in culture_alignment.items():
        print(f"  {culture:.<30} {score:.2f}/10")
    
    # Identify Western bias
    western_cultures = ['US']
    western_score = culture_data[culture_data['culture'].isin(western_cultures)]['cultural_alignment'].mean()
    non_western_score = culture_data[~culture_data['culture'].isin(western_cultures)]['cultural_alignment'].mean()
    
    print(f"\nWestern vs Non-Western (WITH prompting):")
    print(f"  Western (US):................... {western_score:.2f}/10")
    print(f"  Non-Western:.................... {non_western_score:.2f}/10")
    print(f"  Gap:............................ {western_score - non_western_score:.2f}")
    
    if western_score - non_western_score > 1.0:
        print("  ⚠️  Significant Western bias persists even with cultural prompting!")
    else:
        print("  ✓ Relatively balanced with cultural prompting")


def analyze_model_performance(df: pd.DataFrame):
    """Analyze performance differences between models"""
    print("\n" + "=" * 80)
    print("MODEL PERFORMANCE ANALYSIS")
    print("=" * 80)
    
    metrics = ['cultural_alignment', 'consistency', 'differentiation', 'stereotype']
    
    model_scores = df.groupby('model')[metrics].mean()
    
    print("\nModel Performance Summary:")
    print(model_scores.to_string())
    
    # Find best model
    model_scores['overall'] = model_scores.mean(axis=1)
    best_model = model_scores['overall'].idxmax()
    
    print(f"\n🏆 Best Overall Model: {best_model}")
    print(f"   Overall Score: {model_scores.loc[best_model, 'overall']:.2f}/10")
    
    # Statistical comparison (ANOVA)
    print("\n Statistical Significance Tests (ANOVA):")
    
    for metric in metrics:
        groups = [df[df['model'] == model][metric].values for model in df['model'].unique()]
        f_stat, p_value = stats.f_oneway(*groups)
        
        sig = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
        print(f"  {metric:.<30} F={f_stat:.2f}, p={p_value:.4f} {sig}")


def analyze_scenario_categories(df: pd.DataFrame):
    """Analyze performance by scenario category"""
    print("\n" + "=" * 80)
    print("SCENARIO CATEGORY ANALYSIS")
    print("=" * 80)
    
    category_stats = df.groupby('scenario_category').agg({
        'cultural_alignment': ['mean', 'std'],
        'parse_success': 'mean'
    })
    
    print("\nPerformance by Category:")
    print(category_stats.to_string())
    
    # Find hardest and easiest categories
    cat_means = df.groupby('scenario_category')['cultural_alignment'].mean()
    hardest = cat_means.idxmin()
    easiest = cat_means.idxmax()
    
    print(f"\n📉 Hardest Category: {hardest}")
    print(f"   Mean Alignment: {cat_means[hardest]:.2f}/10")
    
    print(f"\n📈 Easiest Category: {easiest}")
    print(f"   Mean Alignment: {cat_means[easiest]:.2f}/10")


def analyze_value_patterns(df: pd.DataFrame):
    """Analyze patterns in value priorities"""
    print("\n" + "=" * 80)
    print("VALUE PATTERN ANALYSIS")
    print("=" * 80)
    
    # Extract all values by culture
    value_counts = {}
    for culture in df['culture'].unique():
        culture_data = df[df['culture'] == culture]
        all_values = []
        for values_list in culture_data['top_values']:
            if isinstance(values_list, list):
                all_values.extend(values_list)
        
        from collections import Counter
        counts = Counter(all_values)
        value_counts[culture] = counts
    
    print("\nTop 3 Values by Culture:")
    for culture, counts in value_counts.items():
        print(f"\n{culture}:")
        for value, count in counts.most_common(3):
            print(f"  {value:.<35} {count}")


def analyze_consistency(df: pd.DataFrame):
    """Analyze response consistency"""
    print("\n" + "=" * 80)
    print("CONSISTENCY ANALYSIS")
    print("=" * 80)
    
    # Check consistency across runs
    if 'run_num' in df.columns:
        consistency_by_model = df.groupby('model').agg({
            'decision': lambda x: x.value_counts().iloc[0] / len(x) if len(x) > 0 else 0,
            'cultural_alignment': 'std'
        })
        
        print("\nModel Consistency:")
        print("  (Higher decision consistency = more consistent)")
        print("  (Lower alignment std = more stable scores)")
        print("\n" + consistency_by_model.to_string())


def generate_insights(df: pd.DataFrame):
    """Generate key insights and recommendations"""
    print("\n" + "=" * 80)
    print("KEY INSIGHTS & RECOMMENDATIONS")
    print("=" * 80)
    
    insights = []
    
    # Overall performance
    overall_alignment = df['cultural_alignment'].mean()
    if overall_alignment > 7:
        insights.append("✅ Strong overall cultural alignment across models")
    elif overall_alignment > 5:
        insights.append("⚠️  Moderate cultural alignment - room for improvement")
    else:
        insights.append("❌ Poor cultural alignment - significant bias present")
    
    # Differentiation
    overall_diff = df['differentiation'].mean()
    if overall_diff > 6:
        insights.append("✅ Good cultural differentiation - models adapt well")
    else:
        insights.append("⚠️  Weak cultural differentiation - models give similar responses")
    
    # Stereotypes
    overall_stereo = df['stereotype'].mean()
    if overall_stereo > 8:
        insights.append("✅ Minimal stereotyping in responses")
    else:
        insights.append("⚠️  Some stereotypical language detected")
    
    # Parse success
    parse_rate = df['parse_success'].mean()
    if parse_rate > 0.9:
        insights.append("✅ High parse success rate - good structured outputs")
    else:
        insights.append("⚠️  Some responses failed to follow format instructions")
    
    print("\n".join(insights))
    
    print("\n\nRecommendations:")
    print("1. Focus improvement efforts on lowest-scoring cultures")
    print("2. Consider fine-tuning or prompt engineering for low-scoring models")
    print("3. Review failure cases where parse_success = False")
    print("4. Test with additional cultural contexts for comprehensive coverage")


def create_analysis_report(results_file: Path):
    """Create complete analysis report"""
    df = load_results(results_file)
    
    print("\n" + "=" * 80)
    print("CULTURAL BIAS MEASUREMENT - ANALYSIS REPORT")
    print("=" * 80)
    print(f"\nDataset: {results_file.name}")
    print(f"Total Responses: {len(df)}")
    print(f"Models: {', '.join(df['model'].unique())}")
    print(f"Cultures: {', '.join(df['culture'].unique())}")
    print(f"Scenarios: {df['scenario_id'].nunique()}")
    
    analyze_cultural_bias(df)
    analyze_model_performance(df)
    analyze_scenario_categories(df)
    analyze_value_patterns(df)
    analyze_consistency(df)
    generate_insights(df)
    
    print("\n" + "=" * 80)
    print("END OF REPORT")
    print("=" * 80)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze experiment results")
    parser.add_argument(
        "results_file",
        type=Path,
        help="Path to results CSV file"
    )
    
    args = parser.parse_args()
    
    if not args.results_file.exists():
        print(f"Error: File not found: {args.results_file}")
        sys.exit(1)
    
    create_analysis_report(args.results_file)
