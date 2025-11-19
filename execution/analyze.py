"""
Analysis Script
Analyzes experiment results and generates insights
"""

import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter
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
        from core.evaluator import calculate_baseline_bias
        from core.response_parser import ParsedResponse
        from core import config

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
            from core.scenarios import get_scenario_by_id
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


def analyze_cultural_shift_magnitude(df: pd.DataFrame):
    """
    Analyze the magnitude of cultural shift from baseline to prompted responses

    This reveals how effective cultural prompting is at overcoming inherent bias
    """
    print("\n" + "=" * 80)
    print("CULTURAL SHIFT MAGNITUDE ANALYSIS")
    print("=" * 80)
    print("Measures how much cultural prompting changes responses vs. baseline\n")

    if 'baseline' not in df['culture'].unique():
        print("⚠️  No baseline data available for shift analysis")
        return

    # Get baseline value distribution
    baseline_values = []
    for values_list in df[df['culture'] == 'baseline']['top_values']:
        if isinstance(values_list, str):
            values_list = eval(values_list)
        if isinstance(values_list, list):
            baseline_values.extend(values_list)

    baseline_counter = Counter(baseline_values)
    baseline_total = len(baseline_values)

    # Calculate shift for each culture
    shift_results = {}

    for culture in df['culture'].unique():
        if culture == 'baseline':
            continue

        culture_values = []
        culture_data = df[df['culture'] == culture]

        for values_list in culture_data['top_values']:
            if isinstance(values_list, str):
                values_list = eval(values_list)
            if isinstance(values_list, list):
                culture_values.extend(values_list)

        culture_counter = Counter(culture_values)
        culture_total = len(culture_values)

        # Calculate total variation distance
        all_values = set(list(baseline_counter.keys()) + list(culture_counter.keys()))

        shift_magnitude = 0
        value_shifts = {}

        for value in all_values:
            baseline_pct = (baseline_counter.get(value, 0) / baseline_total * 100) if baseline_total > 0 else 0
            culture_pct = (culture_counter.get(value, 0) / culture_total * 100) if culture_total > 0 else 0
            shift = culture_pct - baseline_pct
            shift_magnitude += abs(shift)
            value_shifts[value] = shift

        # Total variation distance (TVD) = sum of absolute differences / 2
        tvd = shift_magnitude / 2

        shift_results[culture] = {
            'tvd': tvd,
            'value_shifts': value_shifts
        }

        print(f"\n{culture}:")
        print(f"  Total Variation Distance: {tvd:.2f}%")
        print(f"  (Higher = more shift from baseline)")

        # Show top positive and negative shifts
        sorted_shifts = sorted(value_shifts.items(), key=lambda x: abs(x[1]), reverse=True)

        print(f"\n  Largest Shifts:")
        for value, shift in sorted_shifts[:5]:
            direction = "↑" if shift > 0 else "↓"
            print(f"    {direction} {value:.<30} {shift:+.1f}%")

    # Summary
    print(f"\n{'─' * 80}")
    print("SHIFT MAGNITUDE SUMMARY:")
    sorted_cultures = sorted(shift_results.items(), key=lambda x: x[1]['tvd'], reverse=True)

    print("\nCultures Ranked by Shift Magnitude:")
    for i, (culture, data) in enumerate(sorted_cultures, 1):
        print(f"  {i}. {culture:.<20} {data['tvd']:.2f}% shift from baseline")

    # Interpretation
    avg_shift = np.mean([data['tvd'] for data in shift_results.values()])
    print(f"\nAverage shift magnitude: {avg_shift:.2f}%")

    if avg_shift > 20:
        print("✅ Strong cultural adaptation - prompting highly effective")
    elif avg_shift > 10:
        print("✅ Moderate cultural adaptation - prompting is working")
    else:
        print("⚠️  Weak cultural adaptation - limited impact of prompting")

    return shift_results


def analyze_scenario_difficulty(df: pd.DataFrame):
    """
    Analyze which scenarios are hardest/easiest for models to align with cultures
    """
    print("\n" + "=" * 80)
    print("SCENARIO DIFFICULTY ANALYSIS")
    print("=" * 80)

    # Exclude baseline
    df_filtered = df[df['culture'] != 'baseline'].copy()

    # Calculate mean alignment and variance per scenario
    scenario_stats = df_filtered.groupby('scenario_id').agg({
        'cultural_alignment': ['mean', 'std', 'min', 'max'],
        'parse_success': 'mean'
    }).round(2)

    scenario_stats.columns = ['_'.join(col).strip('_') for col in scenario_stats.columns.values]
    scenario_stats = scenario_stats.sort_values('cultural_alignment_mean')

    print("\nScenarios Ranked by Difficulty (Hardest First):")
    print(scenario_stats.to_string())

    # Identify hardest and easiest
    hardest = scenario_stats.index[0]
    easiest = scenario_stats.index[-1]

    print(f"\n\n🔴 HARDEST SCENARIO: {hardest}")
    print(f"   Mean Alignment: {scenario_stats.loc[hardest, 'cultural_alignment_mean']:.2f}/10")
    print(f"   Std Dev: {scenario_stats.loc[hardest, 'cultural_alignment_std']:.2f}")

    print(f"\n🟢 EASIEST SCENARIO: {easiest}")
    print(f"   Mean Alignment: {scenario_stats.loc[easiest, 'cultural_alignment_mean']:.2f}/10")
    print(f"   Std Dev: {scenario_stats.loc[easiest, 'cultural_alignment_std']:.2f}")

    # Variance analysis - which scenarios have most disagreement across cultures
    print(f"\n\n{'─' * 80}")
    print("CROSS-CULTURAL VARIANCE:")
    print("(High variance = scenario elicits very different responses across cultures)\n")

    high_variance = scenario_stats.nlargest(5, 'cultural_alignment_std')
    print(high_variance[['cultural_alignment_mean', 'cultural_alignment_std']])

    return scenario_stats


def analyze_consistency_across_runs(df: pd.DataFrame):
    """
    Analyze how consistent models are across multiple runs of the same scenario
    """
    print("\n" + "=" * 80)
    print("CONSISTENCY ACROSS RUNS ANALYSIS")
    print("=" * 80)

    if 'run_num' not in df.columns:
        print("⚠️  No run_num column - cannot analyze consistency across runs")
        return

    # Calculate variance across runs for same scenario+model+culture
    consistency_stats = []

    grouped = df.groupby(['scenario_id', 'model', 'culture'])

    for (scenario, model, culture), group in grouped:
        if len(group) > 1:
            alignment_std = group['cultural_alignment'].std()

            # Check decision consistency
            decisions = group['decision'].value_counts()
            decision_consistency = decisions.iloc[0] / len(group) if len(decisions) > 0 else 0

            consistency_stats.append({
                'scenario': scenario,
                'model': model,
                'culture': culture,
                'alignment_std': alignment_std,
                'decision_consistency': decision_consistency
            })

    consistency_df = pd.DataFrame(consistency_stats)

    # Model-level consistency
    print("\nModel Consistency (Lower std = more consistent):")
    model_consistency = consistency_df.groupby('model').agg({
        'alignment_std': 'mean',
        'decision_consistency': 'mean'
    }).round(3)
    print(model_consistency.to_string())

    # Culture-level consistency
    print("\n\nCulture Consistency:")
    culture_consistency = consistency_df.groupby('culture').agg({
        'alignment_std': 'mean',
        'decision_consistency': 'mean'
    }).round(3)
    print(culture_consistency.to_string())

    # Find most and least consistent combinations
    most_consistent = consistency_df.nsmallest(5, 'alignment_std')
    least_consistent = consistency_df.nlargest(5, 'alignment_std')

    print("\n\nMost Consistent (Stable across runs):")
    print(most_consistent[['scenario', 'model', 'culture', 'alignment_std']].to_string(index=False))

    print("\n\nLeast Consistent (Variable across runs):")
    print(least_consistent[['scenario', 'model', 'culture', 'alignment_std']].to_string(index=False))

    return consistency_df


def analyze_statistical_significance(df: pd.DataFrame):
    """
    Perform statistical significance tests between models and cultures
    """
    print("\n" + "=" * 80)
    print("STATISTICAL SIGNIFICANCE TESTING")
    print("=" * 80)

    # Exclude baseline for cultural comparisons
    df_filtered = df[df['culture'] != 'baseline'].copy()

    # 1. ANOVA: Do models differ significantly?
    print("\n1. MODEL COMPARISON (ANOVA)")
    print("─" * 40)

    model_groups = [df_filtered[df_filtered['model'] == model]['cultural_alignment'].values
                    for model in df_filtered['model'].unique()]

    f_stat, p_value = stats.f_oneway(*model_groups)

    print(f"F-statistic: {f_stat:.4f}")
    print(f"p-value: {p_value:.4f}")

    if p_value < 0.001:
        print("*** Highly significant difference between models (p < 0.001)")
    elif p_value < 0.01:
        print("** Significant difference between models (p < 0.01)")
    elif p_value < 0.05:
        print("* Significant difference between models (p < 0.05)")
    else:
        print("No significant difference between models (p >= 0.05)")

    # 2. Pairwise t-tests between models
    print("\n2. PAIRWISE MODEL COMPARISONS (t-tests with Bonferroni correction)")
    print("─" * 40)

    models = df_filtered['model'].unique()
    n_comparisons = len(models) * (len(models) - 1) / 2
    alpha_corrected = 0.05 / n_comparisons

    print(f"Bonferroni corrected alpha: {alpha_corrected:.4f}\n")

    for i, model1 in enumerate(models):
        for model2 in models[i + 1:]:
            group1 = df_filtered[df_filtered['model'] == model1]['cultural_alignment']
            group2 = df_filtered[df_filtered['model'] == model2]['cultural_alignment']

            t_stat, p_value = stats.ttest_ind(group1, group2)

            # Calculate effect size (Cohen's d)
            pooled_std = np.sqrt((group1.std() ** 2 + group2.std() ** 2) / 2)
            cohens_d = (group1.mean() - group2.mean()) / pooled_std if pooled_std > 0 else 0

            sig = ""
            if p_value < alpha_corrected:
                sig = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*"

            print(f"{model1} vs {model2}:")
            print(f"  Mean difference: {group1.mean() - group2.mean():+.3f}")
            print(f"  t-statistic: {t_stat:.3f}, p-value: {p_value:.4f} {sig}")
            print(f"  Cohen's d: {cohens_d:.3f} ", end="")

            if abs(cohens_d) < 0.2:
                print("(negligible effect)")
            elif abs(cohens_d) < 0.5:
                print("(small effect)")
            elif abs(cohens_d) < 0.8:
                print("(medium effect)")
            else:
                print("(large effect)")
            print()

    # 3. Culture comparison
    print("\n3. CULTURE COMPARISON (ANOVA)")
    print("─" * 40)

    culture_groups = [df_filtered[df_filtered['culture'] == culture]['cultural_alignment'].values
                      for culture in df_filtered['culture'].unique()]

    f_stat, p_value = stats.f_oneway(*culture_groups)

    print(f"F-statistic: {f_stat:.4f}")
    print(f"p-value: {p_value:.4f}")

    if p_value < 0.001:
        print("*** Highly significant difference between cultures (p < 0.001)")
    elif p_value < 0.01:
        print("** Significant difference between cultures (p < 0.01)")
    elif p_value < 0.05:
        print("* Significant difference between cultures (p < 0.05)")
    else:
        print("No significant difference between cultures (p >= 0.05)")


def analyze_decision_patterns(df: pd.DataFrame):
    """
    Deep dive into decision patterns across models and cultures
    """
    print("\n" + "=" * 80)
    print("DECISION PATTERN ANALYSIS")
    print("=" * 80)

    # Overall decision distribution
    print("\nOVERALL DECISION DISTRIBUTION:")
    overall_decisions = df['decision'].value_counts()
    total = len(df)

    for decision, count in overall_decisions.items():
        pct = count / total * 100
        bar = "█" * int(pct / 2)
        print(f"  {decision:.<30} {count:>4} ({pct:>5.1f}%) {bar}")

    # By culture
    print("\n\nDECISION PATTERNS BY CULTURE:")

    for culture in sorted(df['culture'].unique()):
        culture_data = df[df['culture'] == culture]
        print(f"\n{culture}:")

        decisions = culture_data['decision'].value_counts()
        culture_total = len(culture_data)

        for decision, count in decisions.head(3).items():
            pct = count / culture_total * 100
            print(f"  {decision:.<30} {pct:>5.1f}%")

    # By model
    print("\n\nDECISION PATTERNS BY MODEL:")

    for model in sorted(df['model'].unique()):
        model_data = df[df['model'] == model]
        print(f"\n{model}:")

        decisions = model_data['decision'].value_counts()
        model_total = len(model_data)

        for decision, count in decisions.head(3).items():
            pct = count / model_total * 100
            print(f"  {decision:.<30} {pct:>5.1f}%")

    # Decision diversity (entropy)
    print("\n\nDECISION DIVERSITY (Entropy):")
    print("(Higher entropy = more diverse decisions, less predictable)")

    from scipy.stats import entropy

    for culture in sorted(df['culture'].unique()):
        culture_data = df[df['culture'] == culture]
        decisions = culture_data['decision'].value_counts(normalize=True)
        ent = entropy(decisions.values)
        print(f"  {culture:.<20} {ent:.3f}")

def create_analysis_report(results_file: Path):
    """Create complete analysis report"""
    df = load_results(results_file)

    # Create output file path
    output_file = results_file.parent / f"analysis_report_{results_file.stem}.txt"

    # Save to file AND print to console
    import sys
    original_stdout = sys.stdout

    with open(output_file, 'w', encoding='utf-8') as f:
        # Duplicate output to both console and file
        sys.stdout = type('DualOutput', (), {
            'write': lambda self, text: (original_stdout.write(text), f.write(text)),
            'flush': lambda self: (original_stdout.flush(), f.flush())
        })()
    
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
        analyze_cultural_shift_magnitude(df)
        analyze_scenario_difficulty(df)
        analyze_consistency_across_runs(df)
        analyze_statistical_significance(df)
        analyze_decision_patterns(df)

    sys.stdout = original_stdout
    print(f"\n✅ Full analysis saved to: {output_file}")

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
