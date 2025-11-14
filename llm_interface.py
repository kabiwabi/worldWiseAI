"""
LLM Interface Module
Handles API calls to different LLM providers (OpenAI, Anthropic, Google)
"""

import os
import json
import time
import hashlib
from typing import Dict, Optional, Tuple
from pathlib import Path
import logging

import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LLMInterface:
    """Interface for calling different LLM APIs"""
    
    def __init__(self, cache_dir: Path = config.CACHE_DIR):
        self.cache_dir = cache_dir
        self.cache_enabled = config.ENABLE_CACHE
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize API clients (lazy loading)
        self._openai_client = None
        self._anthropic_client = None
        self._google_client = None
    
    def _get_openai_client(self):
        """Lazy load OpenAI client"""
        if self._openai_client is None:
            try:
                from openai import OpenAI
                self._openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
            except ImportError:
                logger.error("OpenAI package not installed. Run: pip install openai")
                raise
        return self._openai_client
    
    def _get_anthropic_client(self):
        """Lazy load Anthropic client"""
        if self._anthropic_client is None:
            try:
                from anthropic import Anthropic
                self._anthropic_client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
            except ImportError:
                logger.error("Anthropic package not installed. Run: pip install anthropic")
                raise
        return self._anthropic_client
    
    def _get_google_client(self):
        """Lazy load Google client"""
        if self._google_client is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=config.GOOGLE_API_KEY)
                self._google_client = genai
            except ImportError:
                logger.error("Google AI package not installed. Run: pip install google-generativeai")
                raise
        return self._google_client
    
    def _get_cache_key(self, model: str, system_prompt: str, user_prompt: str, temperature: float) -> str:
        """Generate cache key for a prompt"""
        content = f"{model}|{system_prompt}|{user_prompt}|{temperature}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cached_response(self, cache_key: str) -> Optional[str]:
        """Retrieve cached response if available"""
        if not self.cache_enabled:
            return None
        
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                logger.info(f"Cache hit for key: {cache_key[:8]}...")
                return data['response']
            except Exception as e:
                logger.warning(f"Error reading cache: {e}")
        return None
    
    def _save_to_cache(self, cache_key: str, response: str):
        """Save response to cache"""
        if not self.cache_enabled:
            return
        
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump({'response': response}, f)
        except Exception as e:
            logger.warning(f"Error saving to cache: {e}")
    
    def call_openai(
        self,
        model_name: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """Call OpenAI API"""
        client = self._get_openai_client()
        
        # Check cache
        cache_key = self._get_cache_key(model_name, system_prompt, user_prompt, temperature)
        cached = self._get_cached_response(cache_key)
        if cached:
            return cached
        
        logger.info(f"Calling OpenAI API: {model_name}")
        
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            result = response.choices[0].message.content
            self._save_to_cache(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def call_anthropic(
        self,
        model_name: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """Call Anthropic API"""
        client = self._get_anthropic_client()
        
        # Check cache
        cache_key = self._get_cache_key(model_name, system_prompt, user_prompt, temperature)
        cached = self._get_cached_response(cache_key)
        if cached:
            return cached
        
        logger.info(f"Calling Anthropic API: {model_name}")
        
        try:
            response = client.messages.create(
                model=model_name,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            result = response.content[0].text
            self._save_to_cache(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    def call_google(
        self,
        model_name: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """Call Google Gemini API"""
        genai = self._get_google_client()
        
        # Check cache
        cache_key = self._get_cache_key(model_name, system_prompt, user_prompt, temperature)
        cached = self._get_cached_response(cache_key)
        if cached:
            return cached
        
        logger.info(f"Calling Google API: {model_name}")
        
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_prompt
            )
            
            response = model.generate_content(
                user_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            
            result = response.text
            self._save_to_cache(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Google API error: {e}")
            raise
    
    def call_model(
        self,
        model_key: str,
        system_prompt: str,
        user_prompt: str
    ) -> str:
        """
        Call a model by its config key
        
        Args:
            model_key: Key from config.MODELS (e.g., 'gpt-4', 'claude-sonnet')
            system_prompt: System prompt
            user_prompt: User prompt
            
        Returns:
            Model response text
        """
        if model_key not in config.MODELS:
            raise ValueError(f"Unknown model key: {model_key}")
        
        model_config = config.MODELS[model_key]
        provider = model_config['provider']
        model_name = model_config['model_name']
        temperature = model_config['temperature']
        max_tokens = model_config['max_tokens']
        
        if provider == 'openai':
            return self.call_openai(model_name, system_prompt, user_prompt, temperature, max_tokens)
        elif provider == 'anthropic':
            return self.call_anthropic(model_name, system_prompt, user_prompt, temperature, max_tokens)
        elif provider == 'google':
            return self.call_google(model_name, system_prompt, user_prompt, temperature, max_tokens)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def batch_call(
        self,
        calls: list,
        delay: float = 1.0
    ) -> list:
        """
        Make multiple API calls with rate limiting
        
        Args:
            calls: List of dicts with keys: model_key, system_prompt, user_prompt
            delay: Delay between calls in seconds
            
        Returns:
            List of responses
        """
        responses = []
        
        for i, call in enumerate(calls):
            logger.info(f"Processing call {i+1}/{len(calls)}")
            
            try:
                response = self.call_model(
                    call['model_key'],
                    call['system_prompt'],
                    call['user_prompt']
                )
                responses.append({
                    'success': True,
                    'response': response,
                    'call_info': call
                })
            except Exception as e:
                logger.error(f"Error in batch call {i+1}: {e}")
                responses.append({
                    'success': False,
                    'error': str(e),
                    'call_info': call
                })
            
            # Rate limiting
            if i < len(calls) - 1:
                time.sleep(delay)
        
        return responses


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def query_single_scenario(
    model_key: str,
    scenario_id: str,
    culture: str
) -> str:
    """
    Query a single scenario with a specific model and culture
    
    Args:
        model_key: Model identifier
        scenario_id: Scenario ID
        culture: Culture code
        
    Returns:
        Model response
    """
    from scenarios import get_scenario_by_id
    from prompt_constructor import PromptConstructor
    
    scenario = get_scenario_by_id(scenario_id)
    constructor = PromptConstructor()
    system_prompt, user_prompt = constructor.build_complete_prompt(scenario, culture)
    
    interface = LLMInterface()
    return interface.call_model(model_key, system_prompt, user_prompt)


if __name__ == "__main__":
    # Test the interface
    print("Testing LLM Interface...")
    print("=" * 80)
    
    # Test with a simple prompt
    interface = LLMInterface()
    
    try:
        print("\nTesting with a simple scenario...")
        response = query_single_scenario("gpt-4", "FAM001", "US")
        print(f"\nResponse:\n{response}")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nNote: Make sure to set API keys as environment variables:")
        print("  export OPENAI_API_KEY='your-key'")
        print("  export ANTHROPIC_API_KEY='your-key'")
        print("  export GOOGLE_API_KEY='your-key'")
