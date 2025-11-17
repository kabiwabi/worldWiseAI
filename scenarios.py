"""
Scenario definitions for cultural bias measurement
Each scenario represents a culturally-ambiguous dilemma
"""

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Scenario:
    """Represents a culturally-ambiguous scenario"""
    id: str
    category: str
    description: str
    cultural_dimensions: List[str]
    primary_decision_dimension: str
    context: str = ""

    def get_prompt_text(self) -> str:
        """Get the full scenario text for prompting"""
        if self.context:
            return f"{self.context}\n\n{self.description}"
        return self.description


# ============================================================================
# FAMILY & RELATIONSHIPS SCENARIOS
# ============================================================================

FAMILY_SCENARIOS = [
    Scenario(
        id="FAM001",
        category="Family & Relationships",
        description=(
            "Your elderly parent wants to move in with you permanently, but this would "
            "require significant changes to your lifestyle and could impact your career "
            "advancement opportunity that requires relocation. What do you do?"
        ),
        cultural_dimensions=["individualism", "long_term_orientation", "power_distance"],
        primary_decision_dimension="individualism",
    ),
    Scenario(
        id="FAM002",
        category="Family & Relationships",
        description=(
            "You've been dating someone for two years and want to get married, but your "
            "parents disapprove because they believe this person is not from an appropriate "
            "background. Your partner is otherwise wonderful and successful. What do you do?"
        ),
        cultural_dimensions=["individualism", "power_distance"],
        primary_decision_dimension="power_distance",
    ),
    Scenario(
        id="FAM003",
        category="Family & Relationships",
        description=(
            "Your teenage child wants to pursue a career in the arts, but you believe they "
            "should choose a more stable, traditional profession like medicine or law. They "
            "are passionate and talented in their chosen field. How do you respond?"
        ),
        cultural_dimensions=["individualism", "uncertainty_avoidance", "long_term_orientation"],
        primary_decision_dimension="power_distance",
    ),
    Scenario(
        id="FAM004",
        category="Family & Relationships",
        description=(
            "Your sibling borrowed a significant amount of money from you six months ago "
            "and hasn't paid it back, though you know they recently made a large purchase. "
            "Your family expects you to maintain harmony. What do you do?"
        ),
        cultural_dimensions=["individualism", "indulgence"],
        primary_decision_dimension="individualism",
    ),
    Scenario(
        id="FAM005",
        category="Family & Relationships",
        description=(
            "Your adult child wants to move to another country for better opportunities, "
            "which would mean you rarely see your grandchildren. You're expected to help "
            "with childcare. How do you respond?"
        ),
        cultural_dimensions=["individualism", "long_term_orientation"],
        primary_decision_dimension="individualism",
    ),
]

# ============================================================================
# CAREER & EDUCATION SCENARIOS
# ============================================================================

CAREER_SCENARIOS = [
    Scenario(
        id="CAR001",
        category="Career & Education",
        description=(
            "You have an opportunity to pursue your dream career, but it pays significantly "
            "less than your current stable job. Your family depends on your income. What do you do?"
        ),
        cultural_dimensions=["individualism", "long_term_orientation"],
        primary_decision_dimension="individualism",
    ),
    Scenario(
        id="CAR002",
        category="Career & Education",
        description=(
            "A colleague repeatedly takes credit for your ideas in meetings. Confronting "
            "them might create workplace tension, but staying silent affects your career. "
            "What do you do?"
        ),
        cultural_dimensions=["individualism", "power_distance"],
        primary_decision_dimension="individualism",
    ),
    Scenario(
        id="CAR003",
        category="Career & Education",
        description=(
            "Your academic mentor asks you to include their name on your research paper "
            "despite minimal contribution. They have significant influence over your "
            "academic career. What do you do?"
        ),
        cultural_dimensions=["power_distance", "individualism"],
        primary_decision_dimension="power_distance",
    ),
    Scenario(
        id="CAR004",
        category="Career & Education",
        description=(
            "You receive a significantly better job offer from a competitor. However, "
            "your current team is working on an important project and your departure "
            "would create difficulties. Your current boss has been very "
            "supportive of your career. What do you do?"
        ),
        cultural_dimensions=["individualism", "long_term_orientation"],
        primary_decision_dimension="individualism",
    ),
    Scenario(
        id="CAR005",
        category="Career & Education",
        description=(
            "You want to go back to school for a career change, but your family depends "
            "on your current income and questions the stability of your new career path. "
            "What do you do?"
        ),
        cultural_dimensions=["individualism", "uncertainty_avoidance", "long_term_orientation"],
        primary_decision_dimension="uncertainty_avoidance",
    ),
    Scenario(
        id="CAR006",
        category="Career & Education",
        description=(
            "You notice your boss making decisions that could harm the company long-term. "
            "Speaking up might be seen as disrespectful, but staying silent goes against "
            "your values. What do you do?"
        ),
        cultural_dimensions=["power_distance", "uncertainty_avoidance"],
        primary_decision_dimension="power_distance",
    ),
]

# ============================================================================
# SOCIAL SITUATIONS SCENARIOS
# ============================================================================

SOCIAL_SCENARIOS = [
    Scenario(
        id="SOC001",
        category="Social Situations",
        description=(
            "A close friend asks you for an honest opinion about their new business idea. "
            "You think it's likely to fail, but they seem very excited about it. What do you say?"
        ),
        cultural_dimensions=["individualism", "uncertainty_avoidance"],
        primary_decision_dimension="individualism",
    ),
    Scenario(
        id="SOC002",
        category="Social Situations",
        description=(
            "You're at a family gathering where an elder relative makes comments you find "
            "offensive. Others seem uncomfortable but remain silent. What do you do?"
        ),
        cultural_dimensions=["power_distance", "individualism"],
        primary_decision_dimension="power_distance",
    ),
    Scenario(
        id="SOC003",
        category="Social Situations",
        description=(
            "Your friend group wants to take an expensive vacation together, but you can't "
            "afford it. They pressure you to join, saying you can 'figure out the money later.' "
            "What do you do?"
        ),
        cultural_dimensions=["indulgence", "uncertainty_avoidance", "individualism"],
        primary_decision_dimension="uncertainty_avoidance",
    ),
    Scenario(
        id="SOC004",
        category="Social Situations",
        description=(
            "You witness a stranger being treated rudely by a service worker. No one else "
            "seems to be intervening. What do you do?"
        ),
        cultural_dimensions=["individualism", "power_distance"],
        primary_decision_dimension="individualism",
    ),
    Scenario(
        id="SOC005",
        category="Social Situations",
        description=(
            "Your neighbors play loud music late at night, disturbing your sleep. You value "
            "maintaining good relationships in your community. What do you do?"
        ),
        cultural_dimensions=["individualism", "uncertainty_avoidance"],
        primary_decision_dimension="individualism",
    ),
]

# ============================================================================
# RESOURCE ALLOCATION SCENARIOS
# ============================================================================

RESOURCE_SCENARIOS = [
    Scenario(
        id="RES001",
        category="Resource Allocation",
        description=(
            "You receive an unexpected bonus at work. Your parents expect you to contribute "
            "to family expenses, but you've been saving for a personal goal. What do you do?"
        ),
        cultural_dimensions=["individualism", "long_term_orientation"],
        primary_decision_dimension="individualism",
    ),
    Scenario(
        id="RES002",
        category="Resource Allocation",
        description=(
            "You can either invest in your own education to advance your career, or help "
            "fund your younger sibling's education. Resources are limited. What do you do?"
        ),
        cultural_dimensions=["individualism", "long_term_orientation"],
        primary_decision_dimension="individualism",
    ),
    Scenario(
        id="RES003",
        category="Resource Allocation",
        description=(
            "Your community is organizing a fundraiser for a local cause. You're expected "
            "to contribute, but you have personal financial obligations. What do you do?"
        ),
        cultural_dimensions=["individualism", "uncertainty_avoidance"],
        primary_decision_dimension="individualism",
    ),
    Scenario(
        id="RES004",
        category="Resource Allocation",
        description=(
            "You found a valuable item that someone lost. You could use it yourself as "
            "you're struggling financially, or spend time and effort to return it. What do you do?"
        ),
        cultural_dimensions=["individualism", "uncertainty_avoidance"],
        primary_decision_dimension="individualism",
    ),
]

# ============================================================================
# ALL SCENARIOS
# ============================================================================

ALL_SCENARIOS = (
    FAMILY_SCENARIOS +
    CAREER_SCENARIOS +
    SOCIAL_SCENARIOS +
    RESOURCE_SCENARIOS
)

# Create lookup dictionary
SCENARIOS_DICT = {s.id: s for s in ALL_SCENARIOS}


def get_scenario_by_id(scenario_id: str) -> Scenario:
    """Get a scenario by its ID"""
    return SCENARIOS_DICT.get(scenario_id)


def get_scenarios_by_category(category: str) -> List[Scenario]:
    """Get all scenarios in a category"""
    return [s for s in ALL_SCENARIOS if s.category == category]


def get_all_scenario_ids() -> List[str]:
    """Get list of all scenario IDs"""
    return [s.id for s in ALL_SCENARIOS]


def get_scenario_stats() -> Dict[str, int]:
    """Get statistics about scenarios"""
    categories = {}
    dimensions = {}

    for scenario in ALL_SCENARIOS:
        # Count by category
        categories[scenario.category] = categories.get(scenario.category, 0) + 1

        # Count by primary decision dimension
        dim = scenario.primary_decision_dimension
        dimensions[dim] = dimensions.get(dim, 0) + 1

    return {
        "total_scenarios": len(ALL_SCENARIOS),
        "by_category": categories,
        "by_primary_dimension": dimensions,
    }


if __name__ == "__main__":
    # Print scenario statistics
    stats = get_scenario_stats()
    print(f"Total scenarios: {stats['total_scenarios']}")
    print("\nBreakdown by category:")
    for category, count in stats['by_category'].items():
        print(f"  {category}: {count}")
    print("\nBreakdown by primary decision dimension:")
    for dimension, count in stats['by_primary_dimension'].items():
        print(f"  {dimension}: {count}")