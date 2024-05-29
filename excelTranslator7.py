import csv
import os
import datetime
from openai import OpenAI

# ANSI escape sequences for colors
def blue(text):
    return f"\033[94m{text}\033[0m"

def green(text):
    return f"\033[92m{text}\033[0m"

# Configure the API client
client = OpenAI(api_key="lm-studio", base_url="http://localhost:1234/v1")

def translate_text(text):
    # Ensure text is not empty
    if not text.strip():
        print("Received empty text, skipping translation.")
        return text  # Return original text unchanged if it's empty or only whitespace
    
    try:
        response = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=[
                {"role": "system", "content": "Always reply the text given translated to English."},
                {"role": "user", "content": text}
            ],
        )
        translated_text = response.choices[0].message['content'].strip()
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return text  # Return original text if translation fails

def update_csv_translation(input_file_path):
    # Create a new output file with a timestamp to ensure uniqueness
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_file_path = f"translated_data_{timestamp}.csv"
    
    with open(input_file_path, newline='', encoding='utf-8') as csvfile_in, \
         open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile_out:
        reader = csv.DictReader(csvfile_in)
        headers = reader.fieldnames
        writer = csv.DictWriter(csvfile_out, fieldnames=headers)
        writer.writeheader()

        for index, row in enumerate(reader):
            print(f"Processing row {index + 1}")
            translated_row = {}
            for header in headers:
                original_text = row[header]
                print(f"Original text: {blue(original_text)}")
                translated_text = translate_text(original_text)
                print(f"Translated text: {green(translated_text)}")
                translated_row[header] = translated_text

            writer.writerow(translated_row)
            print(f"Row {index + 1} has been translated and saved.")

# Main execution
csv_file_path = "sabanaSim.csv"
update_csv_translation(csv_file_path)
