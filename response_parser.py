"""
Response Parser Module
Extracts structured data from LLM responses
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class ParsedResponse:
    """Structured representation of an LLM response"""
    raw_text: str
    explanation: str
    decision: Optional[str] = None
    top_values: List[str] = None
    parse_success: bool = False
    parse_errors: List[str] = None
    
    def __post_init__(self):
        if self.top_values is None:
            self.top_values = []
        if self.parse_errors is None:
            self.parse_errors = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)


class ResponseParser:
    """Parses LLM responses to extract structured information"""
    
    def __init__(self):
        # Patterns for extracting structured data
        self.decision_pattern = re.compile(
            r'DECISION:\s*(.+?)(?:\n|$)',
            re.IGNORECASE | re.MULTILINE
        )
        self.values_pattern = re.compile(
            r'TOP_VALUES:\s*(.+?)(?=\n\n|\Z)',
            re.IGNORECASE | re.MULTILINE | re.DOTALL
        )
        self.explanation_pattern = re.compile(
            r'EXPLANATION:\s*(.+)$',
            re.IGNORECASE | re.DOTALL
        )
    
    def parse_response(self, response_text: str) -> ParsedResponse:
        """
        Parse an LLM response into structured format
        
        Args:
            response_text: Raw response from LLM
            
        Returns:
            ParsedResponse object
        """
        errors = []
        
        # Extract explanation (text before structured sections)
        explanation = self._extract_explanation(response_text)
        
        # Extract decision
        decision = self._extract_decision(response_text)
        if not decision:
            errors.append("Could not extract DECISION")
        
        # Extract top values
        top_values = self._extract_values(response_text)
        if not top_values:
            errors.append("Could not extract TOP_VALUES")
        
        parse_success = len(errors) == 0
        
        return ParsedResponse(
            raw_text=response_text,
            explanation=explanation,
            decision=decision,
            top_values=top_values,
            parse_success=parse_success,
            parse_errors=errors
        )
    
    def _extract_explanation(self, text: str) -> str:
        """Extract the explanation text from EXPLANATION: section."""
        match = self.explanation_pattern.search(text)
        if not match:
            return ""

        explanation = match.group(1).strip()
        # Normalize whitespace
        explanation = re.sub(r'\s+', ' ', explanation)
        return explanation
    
    def _extract_decision(self, text: str) -> Optional[str]:
        """Extract the decision from response"""
        match = self.decision_pattern.search(text)
        if match:
            decision = match.group(1).strip()
            # Normalize decision
            decision_lower = decision.lower()
            
            if any(x in decision_lower for x in ['option a', 'prioritize personal', 'personal goal', 'freedom']):
                return "Option A"
            elif any(x in decision_lower for x in ['option b', 'prioritize family', 'family harmony', 'group']):
                return "Option B"
            elif 'compromise' in decision_lower or 'middle ground' in decision_lower:
                return "Compromise"
            elif 'decline' in decision_lower or 'neither' in decision_lower:
                return "Decline"
            else:
                return decision  # Return as-is if can't categorize
        return None
    
    def _extract_values(self, text: str) -> List[str]:
        """Extract top values from response"""
        match = self.values_pattern.search(text)
        if not match:
            return []
        
        values_text = match.group(1)
        
        # Extract values (handle various formats)
        # Format 1: Numbered list - handle indentation and whitespace
        numbered_pattern = re.compile(r'\d+\.\s*(.+?)(?=\s*\n\s*\d+\.|\s*\n\s*-|\s*\n\s*\n|\Z)', re.MULTILINE | re.DOTALL)
        numbered_matches = numbered_pattern.findall(values_text)
        if numbered_matches:
            # Clean up each value - remove newlines and extra spaces
            cleaned = [v.strip().strip('[]').replace('\n', ' ').strip() for v in numbered_matches[:3]]
            return cleaned

        # Format 2: Bullet points (handles indentation and various spacing)
        bullet_pattern = re.compile(r'[-•*]\s*(.+?)(?=\s*\n\s*[-•*]|\s*\Z)', re.MULTILINE | re.DOTALL)
        bullet_matches = bullet_pattern.findall(values_text)
        if bullet_matches:
            # Clean each value: remove newlines, extra spaces, brackets
            cleaned = [re.sub(r'\s+', ' ', v.strip().strip('[]').strip()) for v in bullet_matches[:3]]
            return cleaned
        
        # Format 3: Comma-separated
        if ',' in values_text:
            values = [v.strip().strip('[]').strip() for v in values_text.split(',')]
            return values[:3]
        
        # Format 4: Line-separated
        lines = [l.strip().strip('[]').strip() for l in values_text.split('\n') if l.strip()]
        return lines[:3]

    def batch_parse(self, responses: List[str]) -> List[ParsedResponse]:
        """Parse multiple responses"""
        return [self.parse_response(r) for r in responses]


def calculate_parse_success_rate(parsed_responses: List[ParsedResponse]) -> float:
    """Calculate success rate of parsing"""
    if not parsed_responses:
        return 0.0
    successful = sum(1 for pr in parsed_responses if pr.parse_success)
    return successful / len(parsed_responses)


def get_decision_distribution(parsed_responses: List[ParsedResponse]) -> Dict[str, int]:
    """Get distribution of decisions"""
    distribution = {}
    for pr in parsed_responses:
        if pr.decision:
            distribution[pr.decision] = distribution.get(pr.decision, 0) + 1
    return distribution


def get_value_frequency(parsed_responses: List[ParsedResponse]) -> Dict[str, int]:
    """Get frequency of each value mentioned"""
    frequency = {}
    for pr in parsed_responses:
        for value in pr.top_values:
            frequency[value] = frequency.get(value, 0) + 1
    return frequency


if __name__ == "__main__":
    # Test the parser
    parser = ResponseParser()
    
    # Test response 1
    test_response_1 = """
    Given my cultural background, I would prioritize family harmony in this situation. 
    While career advancement is important, maintaining close relationships with elderly 
    parents is a fundamental value. I would try to find a compromise that honors both.
    
    DECISION: Option B - Prioritize family/group harmony
    
    TOP_VALUES:
    1. Family Harmony
    2. Duty/Obligation
    3. Long-term Relationships
    """
    
    print("Testing Parser...")
    print("=" * 80)
    
    parsed = parser.parse_response(test_response_1)
    print(f"\nParse Success: {parsed.parse_success}")
    print(f"Decision: {parsed.decision}")
    print(f"Top Values: {parsed.top_values}")
    print(f"Explanation: {parsed.explanation[:100]}...")
    
    if parsed.parse_errors:
        print(f"Errors: {parsed.parse_errors}")
