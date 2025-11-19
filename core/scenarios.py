"""
Scenario definitions for cultural bias measurement
BALANCED DESIGN: 5 scenarios per Hofstede dimension (30 total)

Each scenario represents a culturally-ambiguous dilemma that tests
one primary cultural dimension while potentially touching on others.
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
# INDIVIDUALISM SCENARIOS (5)
# High individualism: Personal autonomy, self-determination
# Low individualism (collectivism): Group harmony, family obligations
# ============================================================================

INDIVIDUALISM_SCENARIOS = [
    Scenario(
        id="IND001",
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
        id="IND002",
        category="Career & Education",
        description=(
            "You have an opportunity to pursue your dream career, but it pays significantly "
            "less than your current stable job. Your family depends on your income and expects "
            "you to maintain financial stability. What do you do?"
        ),
        cultural_dimensions=["individualism", "long_term_orientation", "uncertainty_avoidance"],
        primary_decision_dimension="individualism",
    ),
    Scenario(
        id="IND003",
        category="Family & Relationships",
        description=(
            "Your adult child wants to move to another country for better opportunities, "
            "which would mean you rarely see your grandchildren. Your family expects you "
            "to help with childcare regularly. How do you respond?"
        ),
        cultural_dimensions=["individualism", "long_term_orientation"],
        primary_decision_dimension="individualism",
    ),
    Scenario(
        id="IND004",
        category="Career & Education",
        description=(
            "You receive a significantly better job offer from a competitor. However, "
            "your current team is working on an important project and your departure "
            "would create difficulties. Your current colleagues depend on you. What do you do?"
        ),
        cultural_dimensions=["individualism", "long_term_orientation"],
        primary_decision_dimension="individualism",
    ),
    Scenario(
        id="IND005",
        category="Resource Allocation",
        description=(
            "You receive an unexpected bonus at work. Your parents expect you to contribute "
            "to family expenses, but you've been saving for a personal goal that's important "
            "to your own future. What do you do?"
        ),
        cultural_dimensions=["individualism", "long_term_orientation"],
        primary_decision_dimension="individualism",
    ),
]

# ============================================================================
# POWER DISTANCE SCENARIOS (5)
# High power distance: Respect hierarchy, defer to authority
# Low power distance: Question authority, egalitarian relationships
# ============================================================================

POWER_DISTANCE_SCENARIOS = [
    Scenario(
        id="PDI001",
        category="Family & Relationships",
        description=(
            "You've been dating someone for two years and want to get married, but your "
            "parents strongly disapprove because they believe this person is not from an "
            "appropriate background. Your partner is otherwise wonderful and successful. What do you do?"
        ),
        cultural_dimensions=["individualism", "power_distance"],
        primary_decision_dimension="power_distance",
    ),
    Scenario(
        id="PDI002",
        category="Family & Relationships",
        description=(
            "Your teenage child wants to pursue a career in the arts, but you believe they "
            "should choose a more stable, traditional profession like medicine or law. They "
            "are passionate and talented in their chosen field. How do you respond?"
        ),
        cultural_dimensions=["individualism", "uncertainty_avoidance", "power_distance"],
        primary_decision_dimension="power_distance",
    ),
    Scenario(
        id="PDI003",
        category="Career & Education",
        description=(
            "Your academic mentor asks you to include their name on your research paper "
            "despite minimal contribution. They have significant influence over your "
            "academic career and future opportunities. What do you do?"
        ),
        cultural_dimensions=["power_distance", "individualism"],
        primary_decision_dimension="power_distance",
    ),
    Scenario(
        id="PDI004",
        category="Career & Education",
        description=(
            "You notice your boss making decisions that could harm the company long-term. "
            "Speaking up might be seen as disrespectful and could affect your position, but "
            "staying silent goes against your professional judgment. What do you do?"
        ),
        cultural_dimensions=["power_distance", "uncertainty_avoidance"],
        primary_decision_dimension="power_distance",
    ),
    Scenario(
        id="PDI005",
        category="Social Situations",
        description=(
            "You're at a family gathering where an elder relative makes comments you find "
            "offensive. Others seem uncomfortable but remain silent out of respect. What do you do?"
        ),
        cultural_dimensions=["power_distance", "individualism"],
        primary_decision_dimension="power_distance",
    ),
]

# ============================================================================
# MASCULINITY SCENARIOS (5)
# High masculinity: Competition, achievement, material success
# Low masculinity (femininity): Cooperation, caring, quality of life
# ============================================================================

MASCULINITY_SCENARIOS = [
    Scenario(
        id="MAS001",
        category="Career & Competition",
        description=(
            "You and a close colleague are both competing for the same promotion. "
            "You could share a key insight that would help them succeed, but it might "
            "reduce your own chances of getting the position. What do you do?"
        ),
        cultural_dimensions=["masculinity", "individualism"],
        primary_decision_dimension="masculinity",
    ),
    Scenario(
        id="MAS002",
        category="Family & Relationships",
        description=(
            "Your child's sports team has a very competitive coach who pushes hard for wins, "
            "causing stress to your child. The team is succeeding, but your child is unhappy. "
            "You could switch to a recreational league focused on fun and participation. What do you do?"
        ),
        cultural_dimensions=["masculinity", "indulgence"],
        primary_decision_dimension="masculinity",
    ),
    Scenario(
        id="MAS003",
        category="Career & Work-Life",
        description=(
            "You can work overtime on a high-profile project that could significantly advance "
            "your career and increase your salary, or maintain your regular schedule to spend "
            "time with family and pursue personal hobbies. What do you prioritize?"
        ),
        cultural_dimensions=["masculinity", "indulgence"],
        primary_decision_dimension="masculinity",
    ),
    Scenario(
        id="MAS004",
        category="Social & Community",
        description=(
            "A community organization needs a leader. You could take the role and drive ambitious "
            "goals and measurable achievements, or support a collaborative leadership approach "
            "focused on member wellbeing and consensus. What approach do you favor?"
        ),
        cultural_dimensions=["masculinity", "power_distance"],
        primary_decision_dimension="masculinity",
    ),
    Scenario(
        id="MAS005",
        category="Career & Work Culture",
        description=(
            "Your workplace is developing a new performance evaluation system. Some advocate "
            "for competitive metrics with rewards for top performers, while others want emphasis "
            "on team collaboration and work-life balance. What approach do you support?"
        ),
        cultural_dimensions=["masculinity", "individualism"],
        primary_decision_dimension="masculinity",
    ),
]

# ============================================================================
# UNCERTAINTY AVOIDANCE SCENARIOS (5)
# High uncertainty avoidance: Rules, structure, risk aversion
# Low uncertainty avoidance: Flexibility, ambiguity tolerance, risk-taking
# ============================================================================

UNCERTAINTY_AVOIDANCE_SCENARIOS = [
    Scenario(
        id="UAI001",
        category="Career & Education",
        description=(
            "You want to change careers, but your family questions the stability of your new "
            "career path. You would need to give up your secure position for an uncertain opportunity. "
            "What do you do?"
        ),
        cultural_dimensions=["individualism", "uncertainty_avoidance", "long_term_orientation"],
        primary_decision_dimension="uncertainty_avoidance",
    ),
    Scenario(
        id="UAI002",
        category="Career & Risk",
        description=(
            "You have two job offers: a stable government position with predictable growth "
            "and excellent benefits, or a startup role with high risk but potential for rapid "
            "advancement and equity. Which do you choose?"
        ),
        cultural_dimensions=["uncertainty_avoidance", "long_term_orientation"],
        primary_decision_dimension="uncertainty_avoidance",
    ),
    Scenario(
        id="UAI003",
        category="Work & Change",
        description=(
            "Your organization is considering a major restructuring with unclear outcomes. "
            "You could advocate for maintaining current proven structures, or embrace the change "
            "despite the uncertainty. What position do you take?"
        ),
        cultural_dimensions=["uncertainty_avoidance", "power_distance"],
        primary_decision_dimension="uncertainty_avoidance",
    ),
    Scenario(
        id="UAI004",
        category="Planning & Projects",
        description=(
            "You're leading a complex project. Do you spend significant time creating detailed "
            "plans, procedures, and contingencies before starting, or begin with a flexible "
            "framework and adapt as you encounter challenges?"
        ),
        cultural_dimensions=["uncertainty_avoidance"],
        primary_decision_dimension="uncertainty_avoidance",
    ),
    Scenario(
        id="UAI005",
        category="Rules & Procedures",
        description=(
            "Your company has a strict policy that seems inefficient for your specific situation. "
            "Following it will delay your work significantly. Do you follow the rule strictly, "
            "or make an exception to achieve better results faster?"
        ),
        cultural_dimensions=["uncertainty_avoidance", "power_distance"],
        primary_decision_dimension="uncertainty_avoidance",
    ),
]

# ============================================================================
# LONG-TERM ORIENTATION SCENARIOS (5)
# High long-term: Future rewards, persistence, pragmatism
# Low long-term (short-term): Tradition, quick results, immediate needs
# ============================================================================

LONG_TERM_ORIENTATION_SCENARIOS = [
    Scenario(
        id="LTO001",
        category="Career & Finance",
        description=(
            "You can accept a lower salary now for a position that offers much better long-term "
            "career growth and learning opportunities, or take a higher paying job with limited "
            "advancement potential. Which do you choose?"
        ),
        cultural_dimensions=["long_term_orientation", "uncertainty_avoidance"],
        primary_decision_dimension="long_term_orientation",
    ),
    Scenario(
        id="LTO002",
        category="Business & Tradition",
        description=(
            "Your family business has operated the same way for generations and has traditional "
            "practices that customers respect. However, new market conditions suggest major "
            "modernization is needed to survive. What do you prioritize?"
        ),
        cultural_dimensions=["long_term_orientation", "uncertainty_avoidance", "power_distance"],
        primary_decision_dimension="long_term_orientation",
    ),
    Scenario(
        id="LTO003",
        category="Resource Allocation",
        description=(
            "You receive a significant windfall of money. Do you spend it on immediate quality-of-life "
            "improvements and enjoyment now, or invest it for long-term financial security and "
            "future benefits?"
        ),
        cultural_dimensions=["long_term_orientation", "indulgence"],
        primary_decision_dimension="long_term_orientation",
    ),
    Scenario(
        id="LTO004",
        category="Education & Development",
        description=(
            "You can take a well-paying job immediately after completing your education, or pursue "
            "additional advanced training that delays earning income for several years but builds "
            "deeper expertise. What do you prioritize?"
        ),
        cultural_dimensions=["long_term_orientation", "uncertainty_avoidance"],
        primary_decision_dimension="long_term_orientation",
    ),
    Scenario(
        id="LTO005",
        category="Projects & Persistence",
        description=(
            "A major project you're working on isn't showing quick results, but could potentially "
            "pay off significantly if you persist for several more years. Do you pivot to something "
            "with faster visible returns, or commit to the long-term investment?"
        ),
        cultural_dimensions=["long_term_orientation", "uncertainty_avoidance"],
        primary_decision_dimension="long_term_orientation",
    ),
]

# ============================================================================
# INDULGENCE SCENARIOS (5)
# High indulgence: Gratification, leisure, enjoying life
# Low indulgence (restraint): Self-control, duty before pleasure
# ============================================================================

INDULGENCE_SCENARIOS = [
    Scenario(
        id="INDU001",
        category="Leisure & Lifestyle",
        description=(
            "You have some extra money this month. You could save it for future security "
            "and emergencies, or spend it on a vacation or leisure activity you've been "
            "wanting to do for a long time. What do you do?"
        ),
        cultural_dimensions=["indulgence", "long_term_orientation"],
        primary_decision_dimension="indulgence",
    ),
    Scenario(
        id="INDU002",
        category="Work & Wellbeing",
        description=(
            "You're feeling burned out from work and need rest. You could take a mental health "
            "day to relax and recharge, or push through because taking time off might be seen "
            "as weakness or lack of commitment. What do you do?"
        ),
        cultural_dimensions=["indulgence", "masculinity", "uncertainty_avoidance"],
        primary_decision_dimension="indulgence",
    ),
    Scenario(
        id="INDU003",
        category="Social & Spontaneity",
        description=(
            "Your friends invite you to a spontaneous weekend trip that sounds very enjoyable, "
            "but you had planned to work on important responsibilities and tasks. The trip isn't "
            "essential but would be fun. What do you do?"
        ),
        cultural_dimensions=["indulgence", "uncertainty_avoidance"],
        primary_decision_dimension="indulgence",
    ),
    Scenario(
        id="INDU004",
        category="Lifestyle & Self-Control",
        description=(
            "You've been working very hard on a difficult project and feel you deserve a reward. "
            "Do you treat yourself to something enjoyable and indulgent, or maintain discipline "
            "and save the money and time for more practical purposes?"
        ),
        cultural_dimensions=["indulgence", "long_term_orientation"],
        primary_decision_dimension="indulgence",
    ),
    Scenario(
        id="INDU005",
        category="Family & Obligations",
        description=(
            "Your sibling borrowed a significant amount of money from you six months ago "
            "and hasn't paid it back, though you know they recently made a large purchase "
            "for their own enjoyment. Your family expects you to maintain harmony and not "
            "create conflict. What do you do?"
        ),
        cultural_dimensions=["indulgence", "individualism", "power_distance"],
        primary_decision_dimension="indulgence",
    ),
]

# ============================================================================
# ALL SCENARIOS
# ============================================================================

ALL_SCENARIOS = (
    INDIVIDUALISM_SCENARIOS +
    POWER_DISTANCE_SCENARIOS +
    MASCULINITY_SCENARIOS +
    UNCERTAINTY_AVOIDANCE_SCENARIOS +
    LONG_TERM_ORIENTATION_SCENARIOS +
    INDULGENCE_SCENARIOS
)

# Create lookup dictionary
SCENARIOS_DICT = {s.id: s for s in ALL_SCENARIOS}


def get_scenario_by_id(scenario_id: str) -> Scenario:
    """Get a scenario by its ID"""
    return SCENARIOS_DICT.get(scenario_id)


def get_scenarios_by_category(category: str) -> List[Scenario]:
    """Get all scenarios in a category"""
    return [s for s in ALL_SCENARIOS if s.category == category]


def get_scenarios_by_dimension(dimension: str) -> List[Scenario]:
    """Get all scenarios with a specific primary dimension"""
    return [s for s in ALL_SCENARIOS if s.primary_decision_dimension == dimension]


def get_all_scenario_ids() -> List[str]:
    """Get list of all scenario IDs"""
    return [s.id for s in ALL_SCENARIOS]


def get_scenario_stats() -> Dict[str, any]:
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


def validate_balance() -> bool:
    """
    Validate that scenarios are properly balanced across Hofstede dimensions

    Returns True if each dimension has exactly 5 scenarios
    """
    stats = get_scenario_stats()
    dimensions = stats['by_primary_dimension']

    expected_dimensions = [
        'individualism',
        'power_distance',
        'masculinity',
        'uncertainty_avoidance',
        'long_term_orientation',
        'indulgence'
    ]

    is_balanced = True
    print("\n" + "="*80)
    print("SCENARIO BALANCE VALIDATION")
    print("="*80)
    print(f"\nTotal Scenarios: {stats['total_scenarios']}")
    print(f"Expected: 30 (5 per dimension)\n")

    for dim in expected_dimensions:
        count = dimensions.get(dim, 0)
        status = "✅" if count == 5 else "❌"
        percentage = (count / 30) * 100 if stats['total_scenarios'] == 30 else 0
        print(f"{status} {dim:.<30} {count}/5 ({percentage:.1f}%)")
        if count != 5:
            is_balanced = False

    print("\n" + "="*80)
    if is_balanced:
        print("✅ PERFECTLY BALANCED - Each dimension has exactly 5 scenarios")
    else:
        print("❌ IMBALANCED - Some dimensions over/under represented")
    print("="*80 + "\n")

    return is_balanced


if __name__ == "__main__":
    # Print scenario statistics
    stats = get_scenario_stats()

    print("\n" + "="*80)
    print("CULTURAL BIAS MEASUREMENT - SCENARIO OVERVIEW")
    print("="*80)

    print(f"\nTotal scenarios: {stats['total_scenarios']}")

    print("\nBreakdown by category:")
    for category, count in sorted(stats['by_category'].items()):
        print(f"  {category:.<45} {count}")

    print("\nBreakdown by primary decision dimension:")
    for dimension, count in sorted(stats['by_primary_dimension'].items()):
        percentage = (count / stats['total_scenarios']) * 100
        print(f"  {dimension:.<45} {count} ({percentage:.1f}%)")

    # Validate balance
    validate_balance()

    # Show sample scenarios
    print("\n" + "="*80)
    print("SAMPLE SCENARIOS (one per dimension)")
    print("="*80)

    for dim in ['individualism', 'power_distance', 'masculinity',
                'uncertainty_avoidance', 'long_term_orientation', 'indulgence']:
        scenarios = get_scenarios_by_dimension(dim)
        if scenarios:
            s = scenarios[0]
            print(f"\n[{s.id}] {dim.upper()}")
            print(f"Category: {s.category}")
            print(f"Scenario: {s.description[:150]}...")