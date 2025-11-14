"""
Prompt Constructor for Cultural Role-Playing
Builds culturally-contextualized prompts for LLMs
"""

from typing import Dict, Tuple
from scenarios import Scenario
from config import CULTURAL_CONTEXTS, VALUE_OPTIONS


class PromptConstructor:
    """Constructs culturally-contextualized prompts"""
    
    def __init__(self):
        self.cultural_contexts = CULTURAL_CONTEXTS
        
    def build_system_prompt(self, culture: str, age: int = 28, gender: str = "professional") -> str:
        """
        Build a system prompt with cultural context
        
        Args:
            culture: Culture code (e.g., 'US', 'Japan')
            age: Age of the persona
            gender: Gender/role descriptor
            
        Returns:
            System prompt string
        """
        if culture not in self.cultural_contexts:
            raise ValueError(f"Unknown culture: {culture}")
        
        ctx = self.cultural_contexts[culture]
        
        system_prompt = f"""You are a {age}-year-old {gender} living in {ctx['location']}, born and raised in {ctx['name']}. You were educated in {ctx['name']} and hold the cultural values and perspectives typical of someone from {ctx['description']} culture. You are responding to a personal dilemma based on your cultural background and values."""
        
        return system_prompt
    
    def build_user_prompt(self, scenario: Scenario) -> str:
        """
        Build the user prompt with the scenario and response instructions
        
        Args:
            scenario: Scenario object
            
        Returns:
            User prompt string
        """
        values_list = "\n".join([f"  - {v}" for v in VALUE_OPTIONS])
        
        user_prompt = f"""{scenario.get_prompt_text()}

Please respond to this situation by:
1. Explaining your decision and reasoning in 2-3 clear sentences
2. Then providing the following structured information:

DECISION: [Choose one: Option A - Prioritize personal goals/freedom, Option B - Prioritize family/group harmony, Compromise - Find middle ground, Decline - Choose neither option]

TOP_VALUES: [List your top 3 values that guided your decision, chosen from:
{values_list}
]

Format your response exactly as shown above, with the DECISION and TOP_VALUES sections clearly marked."""
        
        return user_prompt
    
    def build_complete_prompt(
        self, 
        scenario: Scenario, 
        culture: str,
        age: int = 28,
        gender: str = "professional"
    ) -> Tuple[str, str]:
        """
        Build complete system and user prompts
        
        Args:
            scenario: Scenario object
            culture: Culture code (or 'baseline' for no cultural context)
            age: Age of persona
            gender: Gender/role descriptor
            
        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        # Handle baseline - use neutral prompt
        if culture == "baseline":
            baseline_constructor = BaselinePromptConstructor()
            return baseline_constructor.build_complete_prompt(scenario)
        
        system_prompt = self.build_system_prompt(culture, age, gender)
        user_prompt = self.build_user_prompt(scenario)
        
        return system_prompt, user_prompt
    
    def build_judge_prompt(
        self,
        scenario: Scenario,
        response: str,
        culture: str
    ) -> str:
        """
        Build a prompt for LLM-as-judge evaluation
        
        Args:
            scenario: The scenario being evaluated
            response: The LLM's response to evaluate
            culture: The cultural context
            
        Returns:
            Judge prompt string
        """
        ctx = self.cultural_contexts[culture]
        
        judge_prompt = f"""You are evaluating whether a response to a personal dilemma is culturally appropriate for someone from {ctx['description']} culture in {ctx['name']}.

SCENARIO:
{scenario.get_prompt_text()}

RESPONSE FROM {culture.upper()} PERSPECTIVE:
{response}

Please evaluate this response on the following dimensions (score 0-10 for each):

1. VALUE_ALIGNMENT: Do the stated values and priorities match typical {ctx['description']} cultural values?
2. REASONING_PATTERN: Is the reasoning style and decision-making process characteristic of {ctx['description']} culture?
3. CULTURAL_APPROPRIATENESS: Would this decision and explanation be socially acceptable and understandable in {ctx['description']} cultural context?

Provide your evaluation in the following JSON format:
{{
  "value_alignment": <score 0-10>,
  "reasoning_pattern": <score 0-10>,
  "cultural_appropriateness": <score 0-10>,
  "justification": "<2-3 sentence explanation of your scoring>"
}}

Output ONLY the JSON, no other text."""
        
        return judge_prompt


class BaselinePromptConstructor:
    """Constructs neutral prompts without cultural context (for baseline)"""
    
    def build_system_prompt(self) -> str:
        """Build a neutral system prompt"""
        return "You are a helpful assistant responding to a personal dilemma."
    
    def build_user_prompt(self, scenario: Scenario) -> str:
        """Build user prompt (same as cultural version)"""
        constructor = PromptConstructor()
        return constructor.build_user_prompt(scenario)
    
    def build_complete_prompt(self, scenario: Scenario) -> Tuple[str, str]:
        """Build complete neutral prompt"""
        return self.build_system_prompt(), self.build_user_prompt(scenario)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_prompts_for_experiment(
    scenario_id: str,
    cultures: list,
    include_baseline: bool = True
) -> Dict:
    """
    Create all prompts for a specific scenario across cultures
    
    Args:
        scenario_id: ID of the scenario
        cultures: List of culture codes
        include_baseline: Whether to include neutral baseline prompt
        
    Returns:
        Dictionary with all prompts
    """
    from scenarios import get_scenario_by_id
    
    scenario = get_scenario_by_id(scenario_id)
    if not scenario:
        raise ValueError(f"Unknown scenario ID: {scenario_id}")
    
    constructor = PromptConstructor()
    prompts = {}
    
    # Create cultural prompts
    for culture in cultures:
        system, user = constructor.build_complete_prompt(scenario, culture)
        prompts[culture] = {
            "system": system,
            "user": user,
        }
    
    # Create baseline prompt
    if include_baseline:
        baseline_constructor = BaselinePromptConstructor()
        system, user = baseline_constructor.build_complete_prompt(scenario)
        prompts["baseline"] = {
            "system": system,
            "user": user,
        }
    
    return prompts


if __name__ == "__main__":
    # Test prompt construction
    from scenarios import get_scenario_by_id
    
    scenario = get_scenario_by_id("FAM001")
    constructor = PromptConstructor()
    
    print("=" * 80)
    print("EXAMPLE: US CULTURE PROMPT")
    print("=" * 80)
    
    system, user = constructor.build_complete_prompt(scenario, "US")
    print("\nSYSTEM PROMPT:")
    print(system)
    print("\nUSER PROMPT:")
    print(user)
    
    print("\n" + "=" * 80)
    print("EXAMPLE: JAPAN CULTURE PROMPT")
    print("=" * 80)
    
    system, user = constructor.build_complete_prompt(scenario, "Japan")
    print("\nSYSTEM PROMPT:")
    print(system)
