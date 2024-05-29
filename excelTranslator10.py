import csv
import os
from openai import OpenAI

# ANSI escape sequences for colors
def blue(text):
    return f"\033[94m{text}\033[0m"

def green(text):
    return f"\033[92m{text}\033[0m"

# Configure the API client
client = OpenAI(api_key="your_api_key", base_url="http://localhost:1234/v1")

def translate_text(text):
    # Ensure text is not empty
    if not text.strip():
        print("Received empty text, skipping translation.")
        return text  # Return original text unchanged if it's empty or only whitespace
    
    try:
        response = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=[
                {"role": "system", "content": "Always reply the text given translated to English.as context consider that you are a translator for the university Instituto Tecnologico de Monterrety. Consider that you are reading a format in csv that must be exaclty as provided, no notes and no bullets, respect the csv format the comas are not needed to add , you are also reading courses keys which are not necesary to translate just provide exactly the same key of the unit , its unaceptable to replay with conversations style , example user:Unidad de formacion, you: Here is the tranlsated word TRANSLATION, thats incorrect. YOU SHOULD ONLY REPLY BASED IN THE CONTEXT AND THE GIVEN TEXT example correct, user:Unidad de Formacion, you:Learning Unit , remember its always in a UNiversity context , and consider that you are not going to translate key and numbers "},
                {"role": "user", "content": text}
            ],
        )
        # Properly access the translated text from the response object
        translated_text = response.choices[0].message.content.strip()
        print("API Response:", response)  # Optional: Print the response for debugging
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return text  # Return original text if translation fails

def read_and_translate_csv(input_file_path, output_file_path):
    if not os.path.exists(input_file_path):
        print(f"Input file {input_file_path} does not exist.")
        return

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
input_file_path = "sabanaSim.csv"  # The input CSV file path
output_file_path = "translated_data.csv"  # The output CSV file path where the translations will be saved

read_and_translate_csv(input_file_path, output_file_path)
