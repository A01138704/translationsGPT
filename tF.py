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

def translate_text_chunks_and_save(chunks, output_file_path):
    for index, chunk in enumerate(chunks):
        # Translate each chunk individually
        completion = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=[{"role": "user", "content": chunk}],
            temperature=0.7,
            stream=True
        )
        translated_chunk = "".join([choice.choices[0].delta.content for choice in completion if choice.choices[0].delta.content])
        
        # Print each translated chunk with chunk number for tracking
        print(f"Chunk {index + 1}/{len(chunks)} translated:")
        print(translated_chunk)
        
        # Save the translation to the file
        with open(output_file_path, 'a', encoding='utf-8') as file:
            file.write(translated_chunk + "\n")

# Main execution
input_file_path = "fisica.txt"
output_file_path = "translated_text_file.txt"

# Ensure the file is empty before starting
if os.path.exists(output_file_path):
    os.remove(output_file_path)

chunks = read_and_chunk_input_file(input_file_path)
translate_text_chunks_and_save(chunks, output_file_path)
