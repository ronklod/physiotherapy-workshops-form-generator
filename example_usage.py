#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage of the Hebrew Form Processor
"""

from hebrew_form_processor import HebrewFormProcessor


def example_usage():
    """Demonstrate how to use the Hebrew Form Processor."""
    
    # Example Hebrew text for pregnancy exercise
    sample_text_pregnancy = """
התעמלות הריון - דצמבר 2023

שם: רחל כהן
תעודת זהות: 123456789
מספר קבלה: 12345
סכום ששולם: 250 ש״ח

שם: שרה לוי  
תעודת זהות: 987654321
קבלה מס' 67890
סכום: ₪300

מירי דוד
ת.ז: 456789123
receipt: 11111
שילמה: 275 שקלים
    """
    
    # Example Hebrew text for post-birth exercise
    sample_text_post_birth = """
התעמלות לאחר לידה

משתתפת: ליאת ישראלי
מספר זהות: 321654987
קבלה: 98765  
תשלום: ₪200

נועה גולדברג
ת״ז 147258369
מס׳ קבלה: 55555
סכום ששולם: 225 ש״ח
    """
    
    print("Hebrew Physiotherapy Workshops Form Generator - Example Usage")
    print("=" * 60)
    
    # Process pregnancy exercise example
    print("\n1. Processing Pregnancy Exercise Text:")
    print("-" * 40)
    
    processor1 = HebrewFormProcessor()
    result1 = processor1.process_text(sample_text_pregnancy)
    
    print(f"Activity Type: {result1['activity_type']}")
    print(f"Total Participants: {result1['total_participants']}")
    
    for i, participant in enumerate(result1['participants'], 1):
        print(f"\nParticipant {i}:")
        for key, value in participant.items():
            print(f"  {key}: {value}")
    
    # Generate Word document for pregnancy exercise
    try:
        output_file1 = processor1.create_word_document("pregnancy_exercise_example.docx")
        print(f"\nWord document created: {output_file1}")
    except Exception as e:
        print(f"Error creating document: {e}")
    
    # Process post-birth exercise example
    print("\n\n2. Processing Post-Birth Exercise Text:")
    print("-" * 42)
    
    processor2 = HebrewFormProcessor()
    result2 = processor2.process_text(sample_text_post_birth)
    
    print(f"Activity Type: {result2['activity_type']}")
    print(f"Total Participants: {result2['total_participants']}")
    
    for i, participant in enumerate(result2['participants'], 1):
        print(f"\nParticipant {i}:")
        for key, value in participant.items():
            print(f"  {key}: {value}")
    
    # Generate Word document for post-birth exercise
    try:
        output_file2 = processor2.create_word_document("post_birth_exercise_example.docx")
        print(f"\nWord document created: {output_file2}")
    except Exception as e:
        print(f"Error creating document: {e}")


if __name__ == "__main__":
    example_usage() 