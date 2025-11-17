"""
Test Script
Verifies that all components are working correctly
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        import config
        print("✓ config")
        
        import scenarios
        print("✓ scenarios")
        
        import prompt_constructor
        print("✓ prompt_constructor")
        
        import llm_interface
        print("✓ llm_interface")
        
        import response_parser
        print("✓ response_parser")
        
        import evaluator
        print("✓ evaluator")
        
        import visualizer
        print("✓ visualizer")
        
        print("\n✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import error: {e}")
        return False


def test_scenarios():
    """Test scenario loading"""
    print("\nTesting scenarios...")
    
    try:
        from scenarios import ALL_SCENARIOS, get_scenario_by_id, get_scenario_stats
        
        assert len(ALL_SCENARIOS) > 0, "No scenarios loaded"
        print(f"✓ Loaded {len(ALL_SCENARIOS)} scenarios")
        
        # Test getting a scenario
        scenario = get_scenario_by_id("FAM001")
        assert scenario is not None, "Failed to get scenario FAM001"
        print(f"✓ Retrieved scenario: {scenario.id}")
        
        # Test stats
        stats = get_scenario_stats()
        print(f"✓ Scenario stats: {stats}")
        
        print("\n✅ Scenario tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Scenario test error: {e}")
        return False


def test_prompt_construction():
    """Test prompt construction"""
    print("\nTesting prompt construction...")
    
    try:
        from scenarios import get_scenario_by_id
        from prompt_constructor import PromptConstructor
        
        scenario = get_scenario_by_id("FAM001")
        constructor = PromptConstructor()
        
        system, user = constructor.build_complete_prompt(scenario, "US")
        assert "United States" in system or "Austin" in system, "System prompt missing US context"
        assert len(user) > 100, "User prompt too short"
        print("✓ Prompt construction for US culture")
        
        system, user = constructor.build_complete_prompt(scenario, "Japan")
        assert "Japan" in system or "Tokyo" in system, "System prompt missing Japan context"
        print("✓ Prompt construction for Japan culture")
        
        # Test baseline
        system, user = constructor.build_complete_prompt(scenario, "baseline")
        assert "helpful assistant" in system.lower(), "Baseline should use neutral prompt"
        assert "born" not in system.lower(), "Baseline should not have cultural context"
        print("✓ Prompt construction for baseline (no cultural context)")
        
        print("\n✅ Prompt construction tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Prompt construction test error: {e}")
        return False


def test_response_parsing():
    """Test response parsing"""
    print("\nTesting response parsing...")
    
    try:
        from response_parser import ResponseParser
        
        parser = ResponseParser()
        
        test_response = """
        Given my cultural background, I would prioritize family harmony.
        
        DECISION: Option B - Prioritize family/group harmony
        
        TOP_VALUES:
        1. Family Harmony
        2. Duty/Obligation
        3. Group Consensus
        """
        
        parsed = parser.parse_response(test_response)
        
        assert parsed.parse_success, "Failed to parse valid response"
        assert parsed.decision == "Option B", f"Wrong decision: {parsed.decision}"
        assert len(parsed.top_values) == 3, f"Wrong number of values: {len(parsed.top_values)}"
        
        print("✓ Parsed test response successfully")
        print(f"  Decision: {parsed.decision}")
        print(f"  Values: {parsed.top_values}")
        
        print("\n✅ Response parsing tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Response parsing test error: {e}")
        return False


def test_evaluation():
    """Test evaluation metrics"""
    print("\nTesting evaluation...")
    
    try:
        from response_parser import ParsedResponse
        from evaluator import CulturalEvaluator
        
        evaluator = CulturalEvaluator()
        
        # Create test response
        test_response = ParsedResponse(
            raw_text="Test response",
            explanation="I prioritize family harmony",
            decision="Option B",
            top_values=["Family Harmony", "Duty/Obligation"],
            parse_success=True,
            parse_errors=[]
        )
        
        # Test cultural alignment
        alignment = evaluator.calculate_cultural_alignment(
            test_response,
            "Japan",
            ["individualism", "power_distance"]
        )
        
        assert 0 <= alignment <= 10, f"Alignment score out of range: {alignment}"
        print(f"✓ Cultural alignment score: {alignment:.2f}/10")

        # Test baseline alignment (should return None - not applicable)
        baseline_alignment = evaluator.calculate_cultural_alignment(
            test_response,
            "baseline",
            ["individualism", "power_distance"]
        )
        assert baseline_alignment is None, f"Baseline should return None, got {baseline_alignment}"
        print(f"✓ Baseline alignment score: None (not applicable)")
        
        # Test stereotype detection
        stereotype = evaluator.calculate_stereotype_score(test_response)
        assert 0 <= stereotype <= 10, f"Stereotype score out of range: {stereotype}"
        print(f"✓ Stereotype score: {stereotype:.2f}/10")
        
        print("\n✅ Evaluation tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Evaluation test error: {e}")
        return False


def test_api_keys():
    """Test if API keys are configured"""
    print("\nChecking API keys...")
    
    import config
    
    keys_found = []
    keys_missing = []
    
    if config.OPENAI_API_KEY:
        keys_found.append("OpenAI")
    else:
        keys_missing.append("OpenAI (OPENAI_API_KEY)")
    
    if config.ANTHROPIC_API_KEY:
        keys_found.append("Anthropic")
    else:
        keys_missing.append("Anthropic (ANTHROPIC_API_KEY)")
    
    if config.GOOGLE_API_KEY:
        keys_found.append("Google")
    else:
        keys_missing.append("Google (GOOGLE_API_KEY)")
    
    if keys_found:
        print(f"✓ Found keys for: {', '.join(keys_found)}")
    
    if keys_missing:
        print(f"⚠️  Missing keys for: {', '.join(keys_missing)}")
        print("\nTo set API keys, run:")
        for key in keys_missing:
            if "OpenAI" in key:
                print(f"  export OPENAI_API_KEY='your-key'")
            elif "Anthropic" in key:
                print(f"  export ANTHROPIC_API_KEY='your-key'")
            elif "Google" in key:
                print(f"  export GOOGLE_API_KEY='your-key'")
    
    return len(keys_found) > 0


def run_all_tests():
    """Run all tests"""
    print("=" * 80)
    print("RUNNING SYSTEM TESTS")
    print("=" * 80)
    
    results = {
        "Imports": test_imports(),
        "Scenarios": test_scenarios(),
        "Prompt Construction": test_prompt_construction(),
        "Response Parsing": test_response_parsing(),
        "Evaluation": test_evaluation(),
        "API Keys": test_api_keys()
    }
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\nYou're ready to run experiments:")
        print("  python main.py --mode quick --scenarios 2")
        print("\nOr launch the demo:")
        print("  streamlit run demo.py")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("\nPlease fix the issues above before running experiments.")
    print("=" * 80)
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
