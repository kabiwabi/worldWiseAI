"""
Prompt Constructor Module
Builds culturally-contextualized prompts for LLM experiments

Uses balanced VALUE_OPTIONS (18 values, 3 per dimension)
"""

from typing import Tuple
from scenarios import Scenario
from config import CULTURAL_CONTEXTS, VALUE_OPTIONS


class PromptConstructor:
    """Constructs culturally-informed prompts for scenarios"""

    def __init__(self):
        self.cultural_contexts = CULTURAL_CONTEXTS

    def build_system_prompt(self, culture: str) -> str:
        """
        Build culturally-appropriate system prompt

        Args:
            culture: Culture code (e.g., "US", "Japan", "baseline")

        Returns:
            System prompt string
        """
        if culture == "baseline":
            return "You are a helpful assistant responding to a personal dilemma."

        if culture not in self.cultural_contexts:
            raise ValueError(f"Unknown culture: {culture}")

        context = self.cultural_contexts[culture]

        system_prompt = f"""You are a 28-year-old professional living in {context['location']}, born and raised there. You hold typical {context['description']} cultural values and perspectives.

Your cultural background influences how you approach decisions, relationships, and responsibilities. You think and make decisions based on {context['description']} cultural norms and values.

When responding to dilemmas, you naturally consider the cultural context and values that are important in your society."""

        return system_prompt

    def build_user_prompt(self, scenario: Scenario) -> str:
        """
        Build user prompt with scenario and response format

        Args:
            scenario: Scenario object

        Returns:
            User prompt string with scenario and response structure
        """
        scenario_text = scenario.get_prompt_text()

        # Format VALUE_OPTIONS nicely for display
        values_formatted = "\n".join([f"  - {value}" for value in VALUE_OPTIONS])

        user_prompt = f"""{scenario_text}

Please respond with your decision and reasoning using the following format:

DECISION: [Choose one]
  Option A - [Make your choice based on the scenario]
  Option B - [Alternative choice]
  Decline - [If you choose neither option]

TOP_VALUES: [Select exactly 3 values that most influenced your decision]
{values_formatted}

EXPLANATION: [Explain your reasoning, the trade-offs you considered, and why these values mattered to you]

Remember to:
1. Make a clear decision (Option A, Option B, or Decline)
2. Select exactly 3 values from the list that guided your thinking
3. Explain your reasoning in your own cultural context"""

        return user_prompt

    def build_complete_prompt(
        self,
        scenario: Scenario,
        culture: str
    ) -> Tuple[str, str]:
        """
        Build complete prompt (system + user)

        Args:
            scenario: Scenario object
            culture: Culture code

        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        system_prompt = self.build_system_prompt(culture)
        user_prompt = self.build_user_prompt(scenario)

        return system_prompt, user_prompt

if __name__ == "__main__":
    from scenarios import get_scenario_by_id

    scenario = get_scenario_by_id("IND001")
    constructor = PromptConstructor()

    print("=" * 80)
    print("EXAMPLE: US CULTURE PROMPT")
    print("=" * 80)

    system, user = constructor.build_complete_prompt(scenario, "US")
    print("\nSYSTEM PROMPT:")
    print(system)
    print("\nUSER PROMPT:")
    print(user[:500] + "...")

    print("\n" + "=" * 80)
    print("EXAMPLE: BASELINE PROMPT")
    print("=" * 80)

    system, user = constructor.build_complete_prompt(scenario, "baseline")  # ← USE EXISTING CONSTRUCTOR
    print("\nSYSTEM PROMPT:")
    print(system)
    print("\nUSER PROMPT:")
    print(user[:500] + "...")

    print("\n" + "=" * 80)
    print("✅ Prompt constructor test complete")