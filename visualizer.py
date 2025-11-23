"""
Visualization Module
Generates plots and charts for experiment results
"""
import matplotlib
matplotlib.use('Agg')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging
import ast
from collections import Counter

import config

logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = config.FIGURE_DPI


class Visualizer:
    """Creates visualizations for experiment results"""
    
    def __init__(self, output_dir: Path = config.VISUALIZATIONS_DIR):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.colors = config.COLORS
    
    def plot_cultural_alignment_by_model(self, df: pd.DataFrame):
        """Plot cultural alignment scores by model"""
        fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)
        
        # Exclude baseline from this plot (alignment score is always 5.0 for baseline)
        df_filtered = df[df['culture'] != 'baseline'].copy()
        
        # Calculate means and std
        stats = df_filtered.groupby(['model', 'culture'])['cultural_alignment'].agg(['mean', 'std']).reset_index()
        
        # Create grouped bar plot
        models = df_filtered['model'].unique()
        cultures = df_filtered['culture'].unique()
        x = np.arange(len(cultures))
        width = 0.8 / len(models)
        
        for i, model in enumerate(models):
            model_data = stats[stats['model'] == model]
            offset = (i - len(models)/2) * width + width/2
            ax.bar(
                x + offset,
                model_data['mean'],
                width,
                label=model,
                yerr=model_data['std'],
                capsize=5
            )
        
        ax.set_xlabel('Culture', fontsize=12)
        ax.set_ylabel('Cultural Alignment Score', fontsize=12)
        ax.set_title('Cultural Alignment by Model and Culture (With Cultural Prompting)', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(cultures, rotation=45)
        ax.legend()
        ax.set_ylim(0, 10)
        
        plt.tight_layout()
        self._save_figure(fig, 'cultural_alignment_by_model.png')
        plt.close()

    def plot_decision_distribution(self, df: pd.DataFrame):
        """Plot distribution of decisions by culture"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        cultures = df['culture'].unique()
        
        for idx, culture in enumerate(cultures):
            if idx >= len(axes):
                break
                
            culture_data = df[df['culture'] == culture]
            decision_counts = culture_data['decision'].value_counts()
            
            axes[idx].bar(
                range(len(decision_counts)),
                decision_counts.values,
                color=self.colors.get(culture, 'gray')
            )
            axes[idx].set_xticks(range(len(decision_counts)))
            axes[idx].set_xticklabels(decision_counts.index, rotation=45, ha='right')
            axes[idx].set_title(f'{culture}', fontweight='bold')
            axes[idx].set_ylabel('Count')
        
        # Hide unused subplots
        for idx in range(len(cultures), len(axes)):
            axes[idx].axis('off')
        
        fig.suptitle('Decision Distribution by Culture', fontsize=16, fontweight='bold')
        plt.tight_layout()
        self._save_figure(fig, 'decision_distribution.png')
        plt.close()
    
    def plot_value_frequency(self, df: pd.DataFrame, top_n: int = 10):
        """Plot most frequent values by culture"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Explode top_values lists and count
        all_values = []
        for _, row in df.iterrows():
            if isinstance(row['top_values'], list):
                for value in row['top_values']:
                    all_values.append({
                        'culture': row['culture'],
                        'value': value
                    })
        
        values_df = pd.DataFrame(all_values)
        
        # Get top N values overall
        top_values = values_df['value'].value_counts().head(top_n).index
        
        # Count by culture
        plot_data = values_df[values_df['value'].isin(top_values)]
        
        # Create grouped bar plot
        value_culture_counts = plot_data.groupby(['value', 'culture']).size().unstack(fill_value=0)
        
        value_culture_counts.plot(
            kind='bar',
            ax=ax,
            color=[self.colors.get(c, 'gray') for c in value_culture_counts.columns]
        )
        
        ax.set_xlabel('Values', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title(f'Top {top_n} Values by Culture', fontsize=14, fontweight='bold')
        ax.legend(title='Culture')
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        self._save_figure(fig, 'value_frequency.png')
        plt.close()
    
    def plot_stereotype_scores(self, df: pd.DataFrame):
        """Plot stereotype scores by model and culture"""
        fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)
        
        # Box plot
        sns.boxplot(
            data=df,
            x='culture',
            y='stereotype',
            hue='model',
            ax=ax
        )
        
        ax.set_xlabel('Culture', fontsize=12)
        ax.set_ylabel('Stereotype Score', fontsize=12)
        ax.set_title('Stereotype Scores by Model and Culture', fontsize=14, fontweight='bold')
        ax.legend(title='Model')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        self._save_figure(fig, 'stereotype_scores.png')
        plt.close()
    
    def plot_model_comparison_radar(self, df: pd.DataFrame):
        """Create radar chart comparing models across metrics"""

        # Aggregate metrics by model
        metrics = ['cultural_alignment', 'stereotype']
        model_scores = df.groupby('model')[metrics].mean()
        
        # Number of variables
        num_vars = len(metrics)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        for model in model_scores.index:
            values = model_scores.loc[model].tolist()
            values += values[:1]
            
            ax.plot(angles, values, 'o-', linewidth=2, label=model)
            ax.fill(angles, values, alpha=0.25)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([m.replace('_', ' ').title() for m in metrics])
        ax.set_ylim(0, 10)
        ax.set_title('Model Comparison Across Metrics', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        ax.grid(True)
        
        plt.tight_layout()
        self._save_figure(fig, 'model_comparison_radar.png')
        plt.close()
    
    def plot_category_performance(self, df: pd.DataFrame):
        """Plot performance by scenario category"""
        fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)
        
        # Exclude baseline for this metric
        df_filtered = df[df['culture'] != 'baseline'].copy()
        
        category_scores = df_filtered.groupby('scenario_category')['cultural_alignment'].mean().sort_values()
        
        ax.barh(range(len(category_scores)), category_scores.values)
        ax.set_yticks(range(len(category_scores)))
        ax.set_yticklabels(category_scores.index)
        ax.set_xlabel('Mean Cultural Alignment Score', fontsize=12)
        ax.set_title('Performance by Scenario Category', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 10)
        
        plt.tight_layout()
        self._save_figure(fig, 'category_performance.png')
        plt.close()
    
    def plot_baseline_comparison(self, df: pd.DataFrame):
        """Plot baseline vs cultural prompting comparison"""
        if 'baseline' not in df['culture'].unique():
            return  # Skip if no baseline data
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot 1: Decision distribution comparison
        baseline_decisions = df[df['culture'] == 'baseline']['decision'].value_counts()
        
        # Get most common decision in each non-baseline culture
        cultures = [c for c in df['culture'].unique() if c != 'baseline']
        culture_decisions = {}
        for culture in cultures:
            culture_data = df[df['culture'] == culture]
            if len(culture_data) > 0:
                most_common = culture_data['decision'].value_counts()
                if len(most_common) > 0:
                    culture_decisions[culture] = most_common
        
        # Plot baseline decisions
        if len(baseline_decisions) > 0:
            ax1.bar(range(len(baseline_decisions)), baseline_decisions.values, 
                   color=self.colors.get('baseline', 'gray'), alpha=0.7, label='Baseline')
            ax1.set_xticks(range(len(baseline_decisions)))
            ax1.set_xticklabels(baseline_decisions.index, rotation=45, ha='right')
            ax1.set_ylabel('Count')
            ax1.set_title('Baseline Decision Distribution\n(No Cultural Context)', fontweight='bold')
            ax1.legend()
        
        # Plot 2: Value frequency comparison
        baseline_values = []
        for values_list in df[df['culture'] == 'baseline']['top_values']:
            if isinstance(values_list, list):
                baseline_values.extend(values_list)
        
        from collections import Counter
        baseline_value_counts = Counter(baseline_values)
        
        if baseline_value_counts:
            top_baseline = dict(baseline_value_counts.most_common(5))
            ax2.barh(range(len(top_baseline)), list(top_baseline.values()), 
                    color=self.colors.get('baseline', 'gray'), alpha=0.7)
            ax2.set_yticks(range(len(top_baseline)))
            ax2.set_yticklabels(list(top_baseline.keys()))
            ax2.set_xlabel('Frequency')
            ax2.set_title('Top Values in Baseline Responses\n(Reveals Inherent Bias)', fontweight='bold')
        
        plt.tight_layout()
        self._save_figure(fig, 'baseline_comparison.png')
        plt.close()

    def plot_cultural_shift_magnitude(self, df: pd.DataFrame):
        """Bar chart of shift magnitude (TVD) by culture"""
        if 'baseline' not in df['culture'].unique():
            return

        # --- compute TVD per culture, same as analyze_cultural_shift_magnitude ---
        # Get baseline value distribution
        baseline_values = []
        for values_list in df[df['culture'] == 'baseline']['top_values']:
            if isinstance(values_list, str):
                try:
                    values_list = ast.literal_eval(values_list)
                except Exception:
                    pass
            if isinstance(values_list, list):
                baseline_values.extend(values_list)

        baseline_counter = Counter(baseline_values)
        baseline_total = len(baseline_values)

        shifts = {}
        for culture in df['culture'].unique():
            if culture == 'baseline':
                continue

            culture_values = []
            for values_list in df[df['culture'] == culture]['top_values']:
                if isinstance(values_list, str):
                    try:
                        values_list = ast.literal_eval(values_list)
                    except Exception:
                        pass
                if isinstance(values_list, list):
                    culture_values.extend(values_list)

            culture_counter = Counter(culture_values)
            culture_total = len(culture_values)

            shift_magnitude = 0.0
            all_values = set(baseline_counter.keys()) | set(culture_counter.keys())
            for value in all_values:
                baseline_pct = (baseline_counter.get(value, 0) / baseline_total * 100) if baseline_total > 0 else 0
                culture_pct = (culture_counter.get(value, 0) / culture_total * 100) if culture_total > 0 else 0
                shift_magnitude += abs(culture_pct - baseline_pct)

            tvd = shift_magnitude / 2.0  # TVD in percentage points
            shifts[culture] = tvd

        # Sort by shift magnitude (optional)
        shifts = dict(sorted(shifts.items(), key=lambda x: x[1], reverse=True))

        # --- plotting ---
        fig, ax = plt.subplots(figsize=(10, 6))

        cultures = list(shifts.keys())
        values = list(shifts.values())

        # Color per culture (flag-ish vibes)
        color_map = {
            'Japan': '#d62728',  # red
            'India': '#ff7f0e',  # saffron / orange
            'Mexico': '#2ca02c',  # green
            'UAE': '#9467bd',  # purple accent
            'US': '#1f77b4',  # blue
        }
        colors = [color_map.get(c, '#7f7f7f') for c in cultures]

        ax.bar(cultures, values, color=colors)
        ax.set_ylabel('Shift from Baseline (TVD, %)', fontsize=12)
        ax.set_title('Cultural Shift Magnitude', fontsize=14, fontweight='bold')
        ax.axhline(y=20, color='r', linestyle='--', alpha=0.3, label='Strong shift threshold')
        ax.legend()

        plt.tight_layout()
        self._save_figure(fig, 'cultural_shift_magnitude.png')
        plt.close()

    def plot_scenario_difficulty(self, df: pd.DataFrame):
        """Bar chart of scenarios ranked by difficulty"""
        fig, ax = plt.subplots(figsize=(12, 8))

        df_filtered = df[df['culture'] != 'baseline'].copy()
        scenario_means = df_filtered.groupby('scenario_id')['cultural_alignment'].mean().sort_values()

        colors = ['red' if x < 6.5 else 'orange' if x < 7.5 else 'green' for x in scenario_means.values]

        ax.barh(range(len(scenario_means)), scenario_means.values, color=colors)
        ax.set_yticks(range(len(scenario_means)))
        ax.set_yticklabels(scenario_means.index)
        ax.set_xlabel('Mean Cultural Alignment', fontsize=12)
        ax.set_title('Scenario Difficulty Ranking', fontsize=14, fontweight='bold')
        ax.axvline(x=7.0, color='black', linestyle='--', alpha=0.3)

        plt.tight_layout()
        self._save_figure(fig, 'scenario_difficulty.png')
        plt.close()

    def plot_decision_patterns_by_model(self, df: pd.DataFrame):
        """Stacked bar of decision distribution by model"""
        fig, ax = plt.subplots(figsize=(10, 6))

        decision_data = df.groupby(['model', 'decision']).size().unstack(fill_value=0)
        decision_data_pct = decision_data.div(decision_data.sum(axis=1), axis=0) * 100

        decision_data_pct.plot(kind='bar', stacked=True, ax=ax,
                               color=['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728'])

        ax.set_ylabel('Percentage (%)', fontsize=12)
        ax.set_xlabel('Model', fontsize=12)
        ax.set_title('Decision Distribution by Model', fontsize=14, fontweight='bold')
        ax.legend(title='Decision', bbox_to_anchor=(1.05, 1))
        plt.xticks(rotation=45)

        plt.tight_layout()
        self._save_figure(fig, 'decision_patterns.png')
        plt.close()
    
    def create_all_visualizations(self, results_file: Path):
        """Create all visualizations from results file"""
        logger.info(f"Loading results from {results_file}")
        df = pd.read_csv(results_file)
        
        # Convert string lists to actual lists
        if 'top_values' in df.columns:
            def parse_top_values(x):
                if isinstance(x, list):
                    return x
                if isinstance(x, str) and x.startswith('['):
                    try:
                        return ast.literal_eval(x)
                    except (ValueError, SyntaxError):
                        return []
                return []

            df['top_values'] = df['top_values'].apply(parse_top_values)

        logger.info("Creating visualizations...")

        self.plot_cultural_alignment_by_model(df)
        self.plot_decision_distribution(df)
        self.plot_value_frequency(df)
        self.plot_stereotype_scores(df)
        self.plot_model_comparison_radar(df)
        self.plot_category_performance(df)
        self.plot_baseline_comparison(df)
        self.plot_cultural_shift_magnitude(df)
        self.plot_scenario_difficulty(df)
        self.plot_decision_patterns_by_model(df)
        
        logger.info(f"All visualizations saved to {self.output_dir}")
    
    def _save_figure(self, fig, filename: str):
        """Save figure to output directory"""
        filepath = self.output_dir / filename
        fig.savefig(filepath, dpi=config.FIGURE_DPI, bbox_inches='tight')
        logger.info(f"Saved {filename}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate visualizations")
    parser.add_argument(
        "results_file",
        type=Path,
        help="Path to results CSV file"
    )
    
    args = parser.parse_args()
    
    visualizer = Visualizer()
    visualizer.create_all_visualizations(args.results_file)
