#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Groq API Client for Hebrew Text Processing
Extracts structured participant information from unstructured Hebrew text using Groq's fast inference
"""

import json
import logging
import os
from typing import Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GroqClient:
    """Client for interacting with Groq API to extract information from Hebrew text."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq client.
        
        Args:
            api_key: Groq API key. If not provided, will try to get from environment
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1"
        
        # Set up requests session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        if not self.api_key:
            logger.warning("No Groq API key provided. Set GROQ_API_KEY environment variable or pass api_key parameter.")
    
    def extract_participant_info(self, hebrew_text: str) -> List[Dict[str, str]]:
        """
        Extract participant information from Hebrew text using Groq API.
        
        Args:
            hebrew_text: The Hebrew text containing participant information
            
        Returns:
            List of dictionaries with participant information
        """
        if not self.api_key:
            logger.error("No Groq API key available")
            return []
        
        try:
            # Create the prompt for extracting participant information
            prompt = self._create_extraction_prompt(hebrew_text)
            
            # Make API request
            response = self._make_api_request(prompt)
            
            if not response:
                return []
            
            # Parse the response
            participants = self._parse_extraction_response(response)
            
            logger.info(f"Successfully extracted information for {len(participants)} participants")
            return participants
            
        except Exception as e:
            logger.error(f"Error extracting participant info: {str(e)}")
            return []
    
    def identify_activity_type(self, hebrew_text: str) -> Optional[str]:
        """
        Identify the activity type from Hebrew text using Groq API.
        
        Args:
            hebrew_text: The Hebrew text
            
        Returns:
            Activity type or None if not identified
        """
        if not self.api_key:
            return None
        
        try:
            prompt = f"""
Analyze this Hebrew text and identify if it's about one of these physiotherapy activities:
1. "התעמלות לאחר לידה" (post-birth exercise)
2. "התעמלות הריון" (pregnancy exercise)

Text: {hebrew_text}

Respond with ONLY one of these exact phrases:
- התעמלות לאחר לידה
- התעמלות הריון
- UNKNOWN

Response:"""

            response = self._make_api_request(prompt)
            
            if response and response.strip() in ['התעמלות לאחר לידה', 'התעמלות הריון']:
                return response.strip()
            
            return None
            
        except Exception as e:
            logger.error(f"Error identifying activity type: {str(e)}")
            return None
    
    def _create_extraction_prompt(self, hebrew_text: str) -> str:
        """Create a prompt for extracting participant information."""
        return f"""
You are an expert Hebrew text processor specializing in extracting participant information from physiotherapy workshop texts.

Extract all participant information from this Hebrew text. Look for:
- שם (Name): Hebrew names (first name, last name)
- תעודת זהות (ID): 9-digit Israeli ID numbers
- מספר קבלה (Receipt number): Any receipt/bill numbers mentioned
- סכום ששולם (Amount paid): Money amounts with currency (שקל, ש״ח, ₪)

Hebrew Text:
{hebrew_text}

Instructions:
1. Extract information for each participant mentioned
2. Be flexible with Hebrew text variations and natural language
3. Look for names that are clearly people's names (not activity names)
4. Find all 9-digit numbers that could be ID numbers
5. Find receipt/bill numbers (might be called קבלה, חשבונית, מספר, etc.)
6. Find amounts with currency symbols or Hebrew currency words
7. If information is missing, leave that field empty

Return the results as a JSON array where each object has these exact fields:
- "name": the person's name in Hebrew
- "id": the 9-digit ID number
- "receipt_number": the receipt/bill number
- "amount": the amount paid (numbers only, no currency symbols)

Example output format:
[
  {{
    "name": "שרה כהן",
    "id": "123456789",
    "receipt_number": "12345",
    "amount": "250"
  }}
]

JSON Response:"""

    def _make_api_request(self, prompt: str) -> Optional[str]:
        """Make API request to Groq."""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that processes Hebrew text and extracts structured information. Always respond with valid JSON when requested."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "model": "llama-3.3-70b-versatile",
                "temperature": 0.1,
                "max_tokens": 1000
            }
            
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content'].strip()
            
            logger.error("Unexpected API response format")
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse API response: {str(e)}")
            return None
    
    def _parse_extraction_response(self, response: str) -> List[Dict[str, str]]:
        """Parse the extraction response from Groq API."""
        try:
            # Try to find JSON in the response
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end]
                participants = json.loads(json_str)
                
                # Validate and clean the data
                cleaned_participants = []
                for participant in participants:
                    if isinstance(participant, dict):
                        cleaned_participant = {
                            'name': str(participant.get('name', '')).strip(),
                            'id': str(participant.get('id', '')).strip(),
                            'receipt_number': str(participant.get('receipt_number', '')).strip(),
                            'amount': str(participant.get('amount', '')).strip()
                        }
                        
                        # Only add if at least name is present
                        if cleaned_participant['name']:
                            cleaned_participants.append(cleaned_participant)
                
                return cleaned_participants
            
            logger.error("No valid JSON found in response")
            return []
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from response: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error parsing extraction response: {str(e)}")
            return [] 