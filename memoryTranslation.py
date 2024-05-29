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

# Memory to store previously translated sentences
translation_memory = {}

def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    # Initialize a matrix to store distances
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize the first row and column
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill in the rest of the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                substitution_cost = 0
            else:
                substitution_cost = 1
            dp[i][j] = min(dp[i - 1][j] + 1,  # Deletion
                           dp[i][j - 1] + 1,  # Insertion
                           dp[i - 1][j - 1] + substitution_cost)  # Substitution

    # Return the distance
    return dp[m][n]

def translate_text(text):
    if not text.strip():
        print("Received empty text, skipping translation.")
        return text

    # Check if translation is in memory
    for key, value in translation_memory.items():
        if levenshtein_distance(text, key) <= 3:  # Adjust the threshold as needed
            return value

    try:
        response = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=[
                {"role": "system", "content": "Always reply the text given translated to English.as context consider that you are a translator for the university Instituto Tecnologico de Monterrety. Consider that you are reading a format in csv that must be exaclty as provided, no notes and no bullets, respect the csv format the comas are not needed to add , you are also reading courses keys which are not necesary to translate just provide exactly the same key of the unit , its unaceptable to replay with conversations style , example user:Unidad de formacion, you: Here is the tranlsated word TRANSLATION, thats incorrect. YOU SHOULD ONLY REPLY BASED IN THE CONTEXT AND THE GIVEN TEXT example correct, user:Unidad de Formacion, you:Learning Unit , remember its always in a UNiversity context , and consider that you are not going to translate key and numbers "},
                {"role": "user", "content": text}
            ],
        )
        translated_text = response.choices[0].message.content.strip()

        # Update translation memory
        translation_memory[text] = translated_text

        print("API Response:", response)
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return text

def read_and_translate_csv(input_file_path, output_file_path, debug_file_path):
    if not os.path.exists(input_file_path):
        print(f"Input file {input_file_path} does not exist.")
        return

    with open(input_file_path, newline='', encoding='utf-8') as csvfile_in, \
         open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile_out, \
         open(debug_file_path, 'w', encoding='utf-8') as debug_file:
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

                # Write debug information to file
                debug_file.write(f"Original text: {original_text}\n")
                debug_file.write(f"Translated text: {translated_text}\n\n")

            writer.writerow(translated_row)
            print(f"Row {index + 1} has been translated and saved.")

# Main execution
input_file_path = "sabanaSim.csv"  # The input CSV file path
output_file_path = "translated_data_memory.csv"  # The output CSV file path where the translations will be saved
debug_file_path = "translation_debug.txt"  # The debug file path to store debug information

read_and_translate_csv(input_file_path, output_file_path, debug_file_path)
