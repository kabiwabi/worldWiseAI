"""
Main Experiment Pipeline
Orchestrates the complete cultural bias measurement experiment
"""

from scipy.stats import f_oneway
import json
import logging
from typing import Dict, List
from datetime import datetime
import pandas as pd
from tqdm import tqdm

import config
from scenarios import ALL_SCENARIOS, get_scenario_by_id
from prompt_constructor import PromptConstructor
from llm_interface import LLMInterface
from response_parser import ResponseParser
from evaluator import CulturalEvaluator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.PROJECT_ROOT / 'experiment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ExperimentRunner:
    """Runs the complete cultural bias measurement experiment"""
    
    def __init__(
        self,
        scenarios: List = None,
        models: List[str] = None,
        cultures: List[str] = None,
        num_runs: int = None,
        include_baseline: bool = True
    ):
        """
        Initialize experiment
        
        Args:
            scenarios: List of scenario IDs (default: all)
            models: List of model keys (default: all)
            cultures: List of culture codes (default: all)
            num_runs: Number of runs per combination (default: from config)
            include_baseline: Whether to include baseline (no cultural context) testing
        """
        self.scenarios = scenarios or [s.id for s in ALL_SCENARIOS]
        self.models = models or list(config.MODELS.keys())
        
        # Handle cultures
        if cultures is None:
            # Default: all cultures except baseline
            cultures = [c for c in config.CULTURAL_CONTEXTS.keys() if c != "baseline"]
        
        # Add baseline if requested
        if include_baseline and "baseline" not in cultures:
            cultures = ["baseline"] + cultures
        
        self.cultures = cultures
        self.num_runs = num_runs or config.NUM_RUNS_PER_COMBINATION
        
        self.prompt_constructor = PromptConstructor()
        self.llm_interface = LLMInterface()
        self.parser = ResponseParser()
        self.evaluator = CulturalEvaluator()
        
        # Storage for results
        self.results = []
        
        logger.info(f"Experiment initialized:")
        logger.info(f"  Scenarios: {len(self.scenarios)}")
        logger.info(f"  Models: {len(self.models)}")
        logger.info(f"  Cultures: {len(self.cultures)}")
        logger.info(f"  Including baseline: {include_baseline}")
        logger.info(f"  Runs per combination: {self.num_runs}")
        logger.info(f"  Total API calls: {len(self.scenarios) * len(self.models) * len(self.cultures) * self.num_runs}")
    
    def run_experiment(self):
        """Run the complete experiment"""
        logger.info("=" * 80)
        logger.info("STARTING EXPERIMENT")
        logger.info("=" * 80)
        
        start_time = datetime.now()
        
        total_combinations = len(self.scenarios) * len(self.models) * len(self.cultures) * self.num_runs
        
        with tqdm(total=total_combinations, desc="Running experiment") as pbar:
            for scenario_id in self.scenarios:
                scenario = get_scenario_by_id(scenario_id)
                
                for model_key in self.models:
                    for culture in self.cultures:
                        for run_num in range(self.num_runs):
                            try:
                                result = self._run_single_experiment(
                                    scenario, model_key, culture, run_num
                                )
                                self.results.append(result)
                                
                            except Exception as e:
                                logger.error(
                                    f"Error in experiment "
                                    f"({scenario_id}, {model_key}, {culture}, run {run_num}): {e}"
                                )
                                
                            pbar.update(1)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info("=" * 80)
        logger.info("EXPERIMENT COMPLETE")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Successful runs: {len(self.results)}/{total_combinations}")
        logger.info("=" * 80)
        
        # Save results
        self.save_results()
    
    def _run_single_experiment(
        self,
        scenario,
        model_key: str,
        culture: str,
        run_num: int
    ) -> Dict:
        """Run a single experiment instance"""
        
        # Build prompts
        system_prompt, user_prompt = self.prompt_constructor.build_complete_prompt(
            scenario, culture
        )
        
        # Query model
        response_text = self.llm_interface.call_model(
            model_key, system_prompt, user_prompt
        )
        
        # Parse response
        parsed_response = self.parser.parse_response(response_text)
        
        # Evaluate response
        metrics = self.evaluator.evaluate_response(
            parsed_response,
            culture,
            scenario.cultural_dimensions
        )
        
        # Compile result
        result = {
            'scenario_id': scenario.id,
            'scenario_category': scenario.category,
            'model': model_key,
            'culture': culture,
            'run_num': run_num,
            'timestamp': datetime.now().isoformat(),
            
            # Response data
            'raw_response': response_text,
            'explanation': parsed_response.explanation,
            'decision': parsed_response.decision,
            'top_values': parsed_response.top_values,
            'parse_success': parsed_response.parse_success,
            'parse_errors': parsed_response.parse_errors,
            
            # Metrics
            'cultural_alignment': metrics.cultural_alignment_score,
            'consistency': metrics.consistency_score,
            'differentiation': metrics.cultural_differentiation_score,
            'stereotype': metrics.stereotype_score,
        }
        
        return result
    
    def save_results(self):
        """Save results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON
        json_file = config.RESULTS_DIR / f"results_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        logger.info(f"Saved results to {json_file}")
        
        # Save as CSV
        df = pd.DataFrame(self.results)
        csv_file = config.RESULTS_DIR / f"results_{timestamp}.csv"
        df.to_csv(csv_file, index=False)
        logger.info(f"Saved results to {csv_file}")
        
        # Save summary statistics
        self._save_summary_stats(df, timestamp)

    def _save_summary_stats(self, df: pd.DataFrame, timestamp: str):
        """Save summary statistics"""
        summary = {}

        # Overall statistics
        summary['overall'] = {
            'total_responses': len(df),
            'parse_success_rate': float(df['parse_success'].mean()),
            'mean_cultural_alignment': float(df['cultural_alignment'].mean()),
            'mean_stereotype_score': float(df['stereotype'].mean()),
        }

        # By model - convert to JSON-serializable format
        by_model = df.groupby('model').agg({
            'cultural_alignment': ['mean', 'std'],
            'stereotype': 'mean',
            'parse_success': 'mean'
        })
        summary['by_model'] = {}
        for model in by_model.index:
            summary['by_model'][model] = {
                'cultural_alignment_mean': float(by_model.loc[model, ('cultural_alignment', 'mean')]),
                'cultural_alignment_std': float(by_model.loc[model, ('cultural_alignment', 'std')]),
                'stereotype_mean': float(by_model.loc[model, ('stereotype', 'mean')]),
                'parse_success_mean': float(by_model.loc[model, ('parse_success', 'mean')])
            }

        # By culture - convert to JSON-serializable format
        by_culture = df.groupby('culture').agg({
            'cultural_alignment': ['mean', 'std'],
            'stereotype': 'mean'
        })
        summary['by_culture'] = {}
        for culture in by_culture.index:
            summary['by_culture'][culture] = {
                'cultural_alignment_mean': float(by_culture.loc[culture, ('cultural_alignment', 'mean')]),
                'cultural_alignment_std': float(by_culture.loc[culture, ('cultural_alignment', 'std')]),
                'stereotype_mean': float(by_culture.loc[culture, 'stereotype'])
            }

        # By category - convert to JSON-serializable format
        by_category = df.groupby('scenario_category').agg({
            'cultural_alignment': 'mean',
            'stereotype': 'mean'
        })
        summary['by_category'] = {}
        for category in by_category.index:
            summary['by_category'][category] = {
                'cultural_alignment_mean': float(by_category.loc[category, 'cultural_alignment']),
                'stereotype_mean': float(by_category.loc[category, 'stereotype'])
            }
        
        # Baseline bias analysis
        if 'baseline' in df['culture'].unique():
            baseline_data = df[df['culture'] == 'baseline']
            non_baseline_data = df[df['culture'] != 'baseline']
            
            # Calculate which culture baseline is closest to
            from evaluator import calculate_baseline_bias
            from response_parser import ParsedResponse

            baseline_responses = []
            for _, row in baseline_data.iterrows():
                parsed = ParsedResponse(
                    raw_text=row['raw_response'],
                    explanation=row['explanation'],
                    decision=row.get('decision'),
                    top_values=row.get('top_values', []),
                    parse_success=row['parse_success'],
                    parse_errors=[]
                )
                baseline_responses.append((parsed, row['scenario_id']))
            
            if baseline_responses:
                # Get all scenario dimensions
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
                
                # Find closest culture
                if baseline_distances:
                    closest_culture = min(baseline_distances.items(), key=lambda x: x[1])
                    summary['baseline_bias'] = {
                        'closest_culture': closest_culture[0],
                        'distance': closest_culture[1],
                        'all_distances': baseline_distances,
                        'interpretation': f"Baseline responses are closest to {closest_culture[0]} cultural values"
                    }

        # Scenario difficulty
        scenario_stats = df[df['culture'] != 'baseline'].groupby('scenario_id')['cultural_alignment'].agg(
            ['mean', 'std'])
        summary['scenario_difficulty'] = {
            'hardest': scenario_stats['mean'].idxmin(),
            'hardest_score': float(scenario_stats['mean'].min()),
            'easiest': scenario_stats['mean'].idxmax(),
            'easiest_score': float(scenario_stats['mean'].max())
        }

        # Decision patterns
        decision_dist = df['decision'].value_counts().to_dict()
        summary['decision_distribution'] = {k: int(v) for k, v in decision_dist.items()}

        # Model comparison
        model_groups = [df[df['model'] == m]['cultural_alignment'].values for m in df['model'].unique()]
        f_stat, p_value = f_oneway(*model_groups)
        summary['model_comparison'] = {
            'f_statistic': float(f_stat),
            'p_value': float(p_value),
            'significant': bool(p_value < 0.05)  # ← ADD bool() wrapper
        }

        summary_file = config.RESULTS_DIR / f"summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Saved summary to {summary_file}")


def run_quick_test(num_scenarios: int = 2, num_runs: int = 1):
    """Run a quick test with limited scenarios"""
    logger.info("Running quick test...")
    
    # Use first N scenarios
    test_scenarios = [s.id for s in ALL_SCENARIOS[:num_scenarios]]
    test_models = ["gpt-4"]  # Just one model for testing
    test_cultures = ["baseline", "US", "Japan"]  # Include baseline
    
    runner = ExperimentRunner(
        scenarios=test_scenarios,
        models=test_models,
        cultures=test_cultures,
        num_runs=num_runs,
        include_baseline=False  # Already included in test_cultures
    )
    
    runner.run_experiment()
    
    logger.info("Quick test complete!")


def run_full_experiment():
    """Run the full experiment with all scenarios, models, and cultures"""
    logger.info("Running full experiment...")
    
    runner = ExperimentRunner()
    runner.run_experiment()
    
    logger.info("Full experiment complete!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run cultural bias measurement experiment")
    parser.add_argument(
        "--mode",
        choices=["quick", "full"],
        default="quick",
        help="Experiment mode (quick test or full run)"
    )
    parser.add_argument(
        "--scenarios",
        type=int,
        help="Number of scenarios for quick test (default: 2)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "quick":
        num_scenarios = args.scenarios or 2
        run_quick_test(num_scenarios=num_scenarios)
    else:
        run_full_experiment()
