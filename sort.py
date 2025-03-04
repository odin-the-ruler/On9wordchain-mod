import os
from collections import defaultdict

def organize_words_by_alphabet(file_path, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Read words from file and clean them
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip().replace('-', '') for line in file if line.strip()]
    
    # Categorize words by first letter
    words_dict = defaultdict(list)
    for word in words:
        first_letter = word[0].lower()
        if first_letter.isalpha():  # Ensure it's a valid letter
            words_dict[first_letter].append(word)
    
    # Write words to separate files
    for letter, word_list in words_dict.items():
        letter_file = os.path.join(output_folder, f"{letter}.txt")
        with open(letter_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(word_list))
    
    print(f"Words organized in '{output_folder}' folder.")

# Usage
organize_words_by_alphabet('words.txt', 'sorted_words')
