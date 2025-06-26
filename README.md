# Hebrew Physiotherapy Workshops Form Generator

An application that processes Hebrew text to extract participant information from physiotherapy workshops and generates Word documents with the extracted data.

## Features

- **Hebrew Text Processing**: Automatically identifies activity types from Hebrew text
- **Information Extraction**: Extracts participant names, ID numbers, receipt numbers, and payment amounts
- **Word Document Generation**: Creates formatted Word documents with Hebrew tables
- **Activity Type Recognition**: Supports two activity types:
  - התעמלות לאחר לידה (Post-birth exercise)
  - התעמלות הריון (Pregnancy exercise)

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Interactive Mode

Run the main application in interactive mode:

```bash
python hebrew_form_processor.py
```

Then paste your Hebrew text and press Enter twice to finish input.

### Programmatic Usage

```python
from hebrew_form_processor import HebrewFormProcessor

# Create processor instance
processor = HebrewFormProcessor()

# Your Hebrew text
hebrew_text = """
התעמלות הריון - דצמבר 2023

שם: רחל כהן
תעודת זהות: 123456789
מספר קבלה: 12345
סכום ששולם: 250 ש״ח
"""

# Process the text
result = processor.process_text(hebrew_text)

# Generate Word document
output_file = processor.create_word_document("my_output.docx")
print(f"Document created: {output_file}")
```

### Example Usage

Run the example script to see the application in action:

```bash
python example_usage.py
```

## Input Text Format

The application can handle various Hebrew text formats. Here are some examples:

### Example 1: Structured Format
```
התעמלות הריון

שם: רחל כהן
תעודת זהות: 123456789
מספר קבלה: 12345
סכום ששולם: 250 ש״ח
```

### Example 2: Free Text Format
```
התעמלות לאחר לידה

משתתפת: ליאת ישראלי מספר זהות: 321654987
קבלה: 98765 תשלום: ₪200
```

### Example 3: Mixed Format
```
התעמלות הריון - דצמבר 2023

רחל כהן
ת.ז: 123456789
receipt: 12345
שילמה: 250 שקלים

שרה לוי 987654321
קבלה מס' 67890
₪300
```

## Output

The application generates:

1. **Console Output**: Extracted information displayed in the terminal
2. **Word Document**: A formatted `.docx` file containing:
   - Title with participant name and current month in Hebrew
   - Table with columns: שם (Name), תעודת זהות (ID), מספר קבלה (Receipt Number), סכום ששולם (Amount Paid)

## Supported Text Patterns

### Activity Types
- התעמלות לאחר לידה (Post-birth exercise)
- התעמלות הריון (Pregnancy exercise)

### Information Extraction Patterns
- **Names**: Hebrew letters, spaces, and common punctuation
- **ID Numbers**: 9-digit Israeli ID numbers
- **Receipt Numbers**: Various formats including "קבלה מס׳", "מס׳ קבלה", "receipt"
- **Amounts**: Numbers with currency symbols (₪, שקל, שקלים, ש״ח)

## File Structure

```
├── hebrew_form_processor.py    # Main application
├── example_usage.py           # Usage examples
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Dependencies

- `python-docx`: For creating Word documents
- `regex`: For advanced Hebrew text pattern matching
- `python-dateutil`: For date handling

## Troubleshooting

### Common Issues

1. **Hebrew text not displaying correctly**: Ensure your terminal supports UTF-8 encoding
2. **Word document formatting issues**: The generated documents work best with Microsoft Word or LibreOffice
3. **Information not extracted**: Check that your text follows the supported patterns

### Tips for Better Results

- Include clear separators between different participants
- Use consistent formatting for each type of information
- Include the activity type (התעמלות לאחר לידה or התעמלות הריון) in your text

## License

This project is open source and available under the MIT License. 