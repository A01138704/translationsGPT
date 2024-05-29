import os
from openai import OpenAI

# ANSI escape sequences for colors
def blue(text):
    return f"\033[94m{text}\033[0m"

def green(text):
    return f"\033[92m{text}\033[0m"

# Configure the API client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def read_and_chunk_input_file(file_path, chunk_size=5000, encodings=['utf-8', 'ISO-8859-1']):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                text = file.read()
            print(f"File read successfully with {encoding} encoding.")
            break
        except UnicodeDecodeError:
            print(f"Failed to decode file with {encoding} encoding. Trying next.")
    else:
        raise ValueError("Could not decode the file with any of the provided encodings.")
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def translate_text_chunks_and_save(chunks, output_file_path):
    print(f"Total chunks to process: {len(chunks)}")
    for index, chunk in enumerate(chunks):
        print(f"Processing chunk {index + 1}/{len(chunks)}")
        messages = [{"role": "system", "content": "You are a translation assistant. You always translate the provided text to English only."},
                    {"role": "user", "content": chunk}]
        try:
            completion = client.chat.completions.create(
                model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
                messages=messages,
                temperature=0.7,
                stream=False
            )
            print("API call completed, processing response...")
            # Correctly accessing the translated message
            translated_chunk = completion.choices[0].message.content.strip()  # Use dot notation for accessing properties
            print(f"Translation of chunk {index + 1} completed.")
        except Exception as e:
            print(f"Error during translation of chunk {index + 1}: {e}")
            translated_chunk = ""  # Ensure even errors result in some output
            continue

        print(blue(chunk))
        print(green(translated_chunk))
        with open(output_file_path, 'a', encoding='utf-8') as file:
            file.write(translated_chunk + "\n")
            print(f"Written chunk {index + 1} to file.")

# Main execution
input_file_path = "fisica.txt"
output_file_path = "translated_text_file.txt"

# Ensure the file is empty before starting
if os.path.exists(output_file_path):
    os.remove(output_file_path)

chunks = read_and_chunk_input_file(input_file_path)
translate_text_chunks_and_save(chunks, output_file_path)

