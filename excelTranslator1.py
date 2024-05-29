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
    # Prepare output file: clear if exists or create new one
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    with open(input_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames

        for index, row in enumerate(reader):
            print(f"Processing row {index + 1}")
            translated_row = {}
            for header in headers:
                original_text = row[header]
                print(f"Original text: {blue(original_text)}")
                translated_text = translate_text(original_text)
                print(f"Translated text: {green(translated_text)}")
                translated_row[header] = translated_text

            # Write the translated row to the output CSV immediately
            with open(output_file_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                if index == 0:  # Write header only for the first row
                    writer.writeheader()
                writer.writerow(translated_row)

            print(f"Row {index + 1} has been translated and saved.")

# Main execution
input_file_path = "sabanaSim.csv"
output_file_path = "translated_data.csv"

read_csv_translate_all_columns(input_file_path, output_file_path)
