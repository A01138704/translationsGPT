import os
from openai import OpenAI

# Configure the API client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def read_and_chunk_input_file(file_path, chunk_size=5000, encodings=['utf-8', 'ISO-8859-1']):
    # Try different encodings if utf-8 fails
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                text = file.read()
            # If successful, break out of the loop
            break
        except UnicodeDecodeError:
            print(f"Failed to decode file with {encoding} encoding. Trying next.")
            continue
    else:
        # If all encodings fail, raise an error
        raise ValueError("Could not decode the file with any of the provided encodings.")
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def translate_text_chunks(chunks):
    history = []
    translated_text = []
    for index, chunk in enumerate(chunks):
        history = [{"role": "user", "content": chunk}]
        completion = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=history,
            temperature=0.7,
            stream=True
        )
        translated_chunk = "".join([choice.choices[0].delta.content for choice in completion if choice.choices[0].delta.content])
        translated_text.append(translated_chunk)
        # Print each translated chunk with chunk number
        print(f"Chunk {index + 1}/{len(chunks)} translated:")
        print(translated_chunk)
    return translated_text

def save_translated_text(translated_text, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(translated_text))

# Main execution
input_file_path = "fisica.txt"
output_file_path = "translated_text_file.txt"
chunks = read_and_chunk_input_file(input_file_path)
translated_text = translate_text_chunks(chunks)
save_translated_text(translated_text, output_file_path)
