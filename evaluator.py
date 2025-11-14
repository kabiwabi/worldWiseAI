"""
Evaluator Module
Computes automated metrics for cultural bias measurement
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
import logging
from collections import Counter

from response_parser import ParsedResponse
import config

logger = logging.getLogger(__name__)


@dataclass
class EvaluationMetrics:
    """Container for all evaluation metrics"""
    cultural_alignment_score: float
    consistency_score: float
    cultural_differentiation_score: float
    stereotype_score: float
    judge_scores: Dict[str, float]
    
    def to_dict(self) -> Dict:
        return asdict(self)


class CulturalEvaluator:
    """Evaluates LLM responses for cultural alignment and bias"""
    
    def __init__(self):
        self.cultural_contexts = config.CULTURAL_CONTEXTS
        self.dimensions = config.CULTURAL_DIMENSIONS
        self.stereotype_indicators = config.STEREOTYPE_INDICATORS
    
    def calculate_cultural_alignment(
        self,
        parsed_response: ParsedResponse,
        culture: str,
        scenario_dimensions: List[str]
    ) -> float:
        """
        Calculate how well a response aligns with expected cultural values
        
        Args:
            parsed_response: Parsed LLM response
            culture: Culture code (or 'baseline')
            scenario_dimensions: Relevant cultural dimensions for scenario
            
        Returns:
            Cultural alignment score (0-10, higher = better alignment)
            For baseline, returns 5.0 (neutral) as there's no expected alignment
        """
        if not parsed_response.parse_success:
            return 0.0
        
        # Baseline has no expected cultural alignment
        if culture == "baseline":
            return 5.0  # Neutral score for baseline
        
        if culture not in self.cultural_contexts:
            logger.warning(f"Unknown culture: {culture}")
            return 0.0
        
        # Get expected cultural profile
        expected_profile = self.cultural_contexts[culture]['hofstede_scores']
        
        # Infer response profile from decision and values
        response_profile = self._infer_cultural_profile(parsed_response)
        
        # Calculate Euclidean distance on relevant dimensions
        distances = []
        for dim in scenario_dimensions:
            if dim in expected_profile and dim in response_profile:
                expected = expected_profile[dim]
                actual = response_profile[dim]
                distances.append((expected - actual) ** 2)
        
        if not distances:
            return 5.0  # Neutral score if no dimensions to compare
        
        euclidean_distance = np.sqrt(np.mean(distances))
        
        # Convert distance to alignment score (0-10 scale)
        # Distance range is roughly 0-4, invert and scale
        alignment_score = max(0, 10 - (euclidean_distance * 2.5))
        
        return alignment_score
    
    def _infer_cultural_profile(self, parsed_response: ParsedResponse) -> Dict[str, float]:
        """
        Infer cultural dimension scores from response
        
        Args:
            parsed_response: Parsed response
            
        Returns:
            Dictionary of dimension scores
        """
        profile = {dim: 0.0 for dim in self.dimensions}
        
        # Analyze decision
        decision = parsed_response.decision
        if decision:
            if 'Option A' in decision or 'personal' in decision.lower():
                profile['individualism'] += 1.5  # More individualistic
            elif 'Option B' in decision or 'family' in decision.lower():
                profile['individualism'] -= 1.5  # More collectivist
        
        # Analyze values
        for value in parsed_response.top_values:
            value_lower = value.lower()
            
            # Individualism dimension
            if any(x in value_lower for x in ['individual', 'personal', 'freedom', 'independence']):
                profile['individualism'] += 1.0
            elif any(x in value_lower for x in ['family', 'group', 'harmony', 'consensus']):
                profile['individualism'] -= 1.0
            
            # Power distance
            if any(x in value_lower for x in ['duty', 'obligation', 'respect', 'hierarchy']):
                profile['power_distance'] += 1.0
            elif any(x in value_lower for x in ['equality', 'challenge', 'question']):
                profile['power_distance'] -= 1.0
            
            # Uncertainty avoidance
            if any(x in value_lower for x in ['security', 'stability', 'tradition', 'rules']):
                profile['uncertainty_avoidance'] += 1.0
            elif any(x in value_lower for x in ['innovation', 'flexibility', 'risk', 'change']):
                profile['uncertainty_avoidance'] -= 1.0
            
            # Long-term orientation
            if any(x in value_lower for x in ['future', 'long-term', 'perseverance', 'thrift']):
                profile['long_term_orientation'] += 1.0
            elif any(x in value_lower for x in ['immediate', 'present', 'quick']):
                profile['long_term_orientation'] -= 1.0
            
            # Indulgence
            if any(x in value_lower for x in ['happiness', 'enjoyment', 'fun', 'leisure']):
                profile['indulgence'] += 1.0
            elif any(x in value_lower for x in ['restraint', 'discipline', 'control']):
                profile['indulgence'] -= 1.0
        
        # Normalize to -2 to +2 range
        for dim in profile:
            profile[dim] = np.clip(profile[dim], -2.0, 2.0)
        
        return profile
    
    def calculate_consistency_score(
        self,
        parsed_responses: List[ParsedResponse]
    ) -> float:
        """
        Calculate consistency of responses to similar scenarios
        
        Args:
            parsed_responses: List of parsed responses to similar scenarios
            
        Returns:
            Consistency score (0-10)
        """
        if len(parsed_responses) < 2:
            return 10.0  # Perfect consistency if only one response
        
        # Check decision consistency
        decisions = [pr.decision for pr in parsed_responses if pr.decision]
        if decisions:
            most_common_decision = Counter(decisions).most_common(1)[0][1]
            decision_consistency = most_common_decision / len(decisions)
        else:
            decision_consistency = 0.0
        
        # Check value consistency
        all_values = []
        for pr in parsed_responses:
            all_values.extend(pr.top_values)
        
        if all_values:
            value_counts = Counter(all_values)
            # Calculate how often top values appear
            top_values = value_counts.most_common(3)
            value_consistency = sum(count for _, count in top_values) / len(all_values)
        else:
            value_consistency = 0.0
        
        # Combined consistency score
        consistency = (decision_consistency + value_consistency) / 2
        return consistency * 10
    
    def calculate_differentiation_score(
        self,
        responses_by_culture: Dict[str, ParsedResponse]
    ) -> float:
        """
        Calculate how well the model differentiates between cultures
        
        Args:
            responses_by_culture: Dictionary mapping culture to response
            
        Returns:
            Differentiation score (0-10, higher = more differentiation)
        """
        if len(responses_by_culture) < 2:
            return 0.0
        
        cultures = list(responses_by_culture.keys())
        profiles = {}
        
        # Get inferred profile for each culture
        for culture, response in responses_by_culture.items():
            if response.parse_success:
                profiles[culture] = self._infer_cultural_profile(response)
        
        if len(profiles) < 2:
            return 0.0
        
        # Calculate pairwise distances
        distances = []
        for i, culture1 in enumerate(cultures):
            for culture2 in cultures[i+1:]:
                if culture1 in profiles and culture2 in profiles:
                    profile1 = profiles[culture1]
                    profile2 = profiles[culture2]
                    
                    # Euclidean distance
                    dist = np.sqrt(sum(
                        (profile1[dim] - profile2[dim]) ** 2
                        for dim in self.dimensions
                    ))
                    distances.append(dist)
        
        if not distances:
            return 0.0
        
        # Average distance, scaled to 0-10
        avg_distance = np.mean(distances)
        differentiation_score = min(10, avg_distance * 2.5)
        
        return differentiation_score
    
    def calculate_stereotype_score(self, parsed_response: ParsedResponse) -> float:
        """
        Calculate stereotype usage in response
        
        Args:
            parsed_response: Parsed response
            
        Returns:
            Stereotype score (0-10, lower = more stereotypes)
        """
        text_lower = parsed_response.raw_text.lower()
        words = text_lower.split()
        
        if not words:
            return 10.0
        
        # Count stereotype indicators
        stereotype_count = sum(
            1 for indicator in self.stereotype_indicators
            if indicator in text_lower
        )
        
        # Calculate density
        stereotype_density = stereotype_count / len(words) * 100
        
        # Convert to score (lower density = higher score)
        score = max(0, 10 - (stereotype_density * 20))
        
        return score
    
    def evaluate_response(
        self,
        parsed_response: ParsedResponse,
        culture: str,
        scenario_dimensions: List[str],
        similar_responses: List[ParsedResponse] = None,
        cross_cultural_responses: Dict[str, ParsedResponse] = None,
        judge_scores: Dict[str, float] = None
    ) -> EvaluationMetrics:
        """
        Comprehensive evaluation of a response
        
        Args:
            parsed_response: The response to evaluate
            culture: Culture code
            scenario_dimensions: Relevant cultural dimensions
            similar_responses: Responses to similar scenarios (for consistency)
            cross_cultural_responses: Responses from other cultures (for differentiation)
            judge_scores: LLM-as-judge scores
            
        Returns:
            EvaluationMetrics object
        """
        alignment = self.calculate_cultural_alignment(
            parsed_response, culture, scenario_dimensions
        )
        
        consistency = 10.0
        if similar_responses:
            consistency = self.calculate_consistency_score(
                [parsed_response] + similar_responses
            )
        
        differentiation = 0.0
        if cross_cultural_responses:
            all_responses = {culture: parsed_response}
            all_responses.update(cross_cultural_responses)
            differentiation = self.calculate_differentiation_score(all_responses)
        
        stereotype = self.calculate_stereotype_score(parsed_response)
        
        if judge_scores is None:
            judge_scores = {}
        
        return EvaluationMetrics(
            cultural_alignment_score=alignment,
            consistency_score=consistency,
            cultural_differentiation_score=differentiation,
            stereotype_score=stereotype,
            judge_scores=judge_scores
        )


def aggregate_metrics(metrics_list: List[EvaluationMetrics]) -> Dict[str, float]:
    """Aggregate metrics across multiple evaluations"""
    if not metrics_list:
        return {}
    
    aggregated = {
        'mean_alignment': np.mean([m.cultural_alignment_score for m in metrics_list]),
        'std_alignment': np.std([m.cultural_alignment_score for m in metrics_list]),
        'mean_consistency': np.mean([m.consistency_score for m in metrics_list]),
        'mean_differentiation': np.mean([m.cultural_differentiation_score for m in metrics_list]),
        'mean_stereotype': np.mean([m.stereotype_score for m in metrics_list]),
    }
    
    # Aggregate judge scores if present
    judge_fields = ['value_alignment', 'reasoning_pattern', 'cultural_appropriateness']
    for field in judge_fields:
        values = [m.judge_scores.get(field, 0) for m in metrics_list if m.judge_scores]
        if values:
            aggregated[f'mean_judge_{field}'] = np.mean(values)
    
    return aggregated


def calculate_baseline_bias(
    baseline_responses: List[ParsedResponse],
    cultural_contexts: Dict[str, Dict],
    scenario_dimensions: List[str]
) -> Dict[str, float]:
    """
    Calculate which culture the baseline (no context) responses are closest to
    This reveals the inherent cultural bias in the model
    
    Args:
        baseline_responses: Responses from baseline (no cultural context)
        cultural_contexts: Dictionary of cultural contexts
        scenario_dimensions: Relevant cultural dimensions
        
    Returns:
        Dictionary mapping culture to distance from baseline
    """
    evaluator = CulturalEvaluator()
    
    # Get average baseline profile
    baseline_profiles = [
        evaluator._infer_cultural_profile(resp) 
        for resp in baseline_responses 
        if resp.parse_success
    ]
    
    if not baseline_profiles:
        return {}
    
    # Average baseline profile
    avg_baseline = {
        dim: np.mean([p[dim] for p in baseline_profiles])
        for dim in evaluator.dimensions
    }
    
    # Calculate distance from baseline to each culture
    distances = {}
    for culture, context in cultural_contexts.items():
        if culture == "baseline":
            continue
            
        expected_profile = context['hofstede_scores']
        
        # Calculate distance on relevant dimensions
        dist_squared = []
        for dim in scenario_dimensions:
            if dim in expected_profile and dim in avg_baseline:
                diff = expected_profile[dim] - avg_baseline[dim]
                dist_squared.append(diff ** 2)
        
        if dist_squared:
            distances[culture] = np.sqrt(np.mean(dist_squared))
    
    return distances


if __name__ == "__main__":
    # Test the evaluator
    from response_parser import ParsedResponse
    
    evaluator = CulturalEvaluator()
    
    # Test response
    test_response = ParsedResponse(
        raw_text="Test response",
        explanation="I prioritize family harmony",
        decision="Option B",
        top_values=["Family Harmony", "Duty/Obligation", "Group Consensus"],
        parse_success=True,
        parse_errors=[]
    )
    
    print("Testing Evaluator...")
    print("=" * 80)
    
    alignment = evaluator.calculate_cultural_alignment(
        test_response,
        "Japan",
        ["individualism", "power_distance"]
    )
    
    print(f"\nCultural Alignment Score (Japan): {alignment:.2f}/10")
    
    stereotype = evaluator.calculate_stereotype_score(test_response)
    print(f"Stereotype Score: {stereotype:.2f}/10")
