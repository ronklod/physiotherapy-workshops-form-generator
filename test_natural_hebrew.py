#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to demonstrate the improved Hebrew text extraction
Shows the difference between regex-only and AI-powered extraction
"""

import sys
sys.path.append('backend')

from backend.hebrew_form_processor import HebrewFormProcessor

def test_natural_hebrew():
    """Test natural Hebrew text processing."""
    
    # Natural Hebrew text (the kind that would fail with old regex)
    natural_text = """
התעמלות הריון - יוני 2024

שרה כהן השתתפה בקורס התעמלות הריון במהלך החודש. תעודת הזהות של שרה היא 123456789. היא שילמה 280 שקלים עבור הקורס וקיבלה קבלה מספר 12345.

גם רחל לוי הגיעה לקורסים. המספר זהות שלה 987654321, והיא שילמה 300 ש״ח. הקבלה שלה מספר 67890.

בנוסף, מיכל דוד (ת.ז 456789123) השתתפה גם היא. היא שילמה סכום של 250 שקלים וקבלה חשבונית 11111.
    """
    
    # Structured text (the kind that works well with regex)
    structured_text = """
התעמלות לאחר לידה - יוני 2024

שם: ליאת ישראלי
תעודת זהות: 321654987
מספר קבלה: 98765
סכום ששולם: 200 ש״ח

שם: נועה גולדברג
תעודת זהות: 147258369
מספר קבלה: 55555
סכום ששולם: 225 ₪
    """
    
    print("Hebrew Text Processing Test")
    print("=" * 50)
    
    # Test without Grok API (regex only)
    print("\n1. Testing Natural Text with Regex-Only Processing:")
    print("-" * 50)
    processor_regex = HebrewFormProcessor(grok_api_key=None)
    result_natural_regex = processor_regex.process_text(natural_text)
    
    print(f"Activity Type: {result_natural_regex['activity_type']}")
    print(f"Participants Found: {result_natural_regex['total_participants']}")
    for i, participant in enumerate(result_natural_regex['participants'], 1):
        print(f"  Participant {i}: {participant}")
    
    print("\n2. Testing Structured Text with Regex-Only Processing:")
    print("-" * 50)
    result_structured_regex = processor_regex.process_text(structured_text)
    
    print(f"Activity Type: {result_structured_regex['activity_type']}")
    print(f"Participants Found: {result_structured_regex['total_participants']}")
    for i, participant in enumerate(result_structured_regex['participants'], 1):
        print(f"  Participant {i}: {participant}")
    
    # Test with Grok API (if available)
    print("\n3. Testing with Grok AI (if API key is set):")
    print("-" * 50)
    processor_ai = HebrewFormProcessor()  # Will use GROK_API_KEY from environment
    
    import os
    if os.getenv('GROK_API_KEY'):
        print("Grok API key found - testing AI extraction...")
        result_natural_ai = processor_ai.process_text(natural_text)
        
        print(f"Activity Type: {result_natural_ai['activity_type']}")
        print(f"Participants Found: {result_natural_ai['total_participants']}")
        for i, participant in enumerate(result_natural_ai['participants'], 1):
            print(f"  Participant {i}: {participant}")
    else:
        print("No Grok API key found (GROK_API_KEY environment variable not set)")
        print("The system will fall back to regex extraction.")
        print("To test AI extraction, set your Grok API key:")
        print("export GROK_API_KEY='your-api-key-here'")
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("\nExpected Results:")
    print("- Structured text should work well with regex")
    print("- Natural text should work much better with AI")
    print("- Both should identify the activity type correctly")

if __name__ == "__main__":
    test_natural_hebrew() 