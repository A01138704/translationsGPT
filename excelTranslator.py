import csv
import os
from openai import OpenAI

# ANSI escape sequences for colors
def blue(text):
    return f"\033[94m{text}\033[0m"

def green(text):
    return f"\033[92m{text}\033[0m"

# Configure the API client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def translate_text(text):
    messages = [{"role": "system", "content": "You are a translation assistant."},
                {"role": "user", "content": text}]
    try:
        response = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=messages,
            temperature=0.5,
            stream=False
        )
        translated_text = response.choices[0].text.strip()
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return text  # Return original text if translation fails

def read_csv_translate_all_columns(input_file_path, output_file_path):
    with open(input_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        translated_rows = []

        for index, row in enumerate(reader):
            print(f"Processing row {index + 1}")
            translated_row = {}
            for header in headers:
                original_text = row[header]
                print(f"Original text: {blue(original_text)}")
                translated_text = translate_text(original_text)
                print(f"Translated text: {green(translated_text)}")
                translated_row[header] = translated_text

            translated_rows.append(translated_row)

        # Write the translated data to a new CSV
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(translated_rows)
            print(f"All entries have been translated and saved to {output_file_path}.")

# Main execution
input_file_path = "sabanaSim.csv"
output_file_path = "translated_data.csv"

# Ensure the file is empty before starting
if os.path.exists(output_file_path):
    os.remove(output_file_path)

read_csv_translate_all_columns(input_file_path, output_file_path)

