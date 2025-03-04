
import random
from telethon import TelegramClient ,events
def filter_words_by_req_word(start_word, min_length, req_word, spam_word=None):
    try:
        # Read available words from the sorted words file
        with open(f'sorted_words/{start_word}.txt', 'r', encoding='utf-8') as file:
            words = {word.strip().lower() for word in file}
        # Read used words from usedword.txt
        try:
            with open('usedword.txt', 'r', encoding='utf-8') as used_file:
                used_words = {word.strip().lower() for word in used_file}
        except FileNotFoundError:
            used_words = set()  # If the file doesn't exist, assume no words are used
        # Filter words based on length and ensure they are not in used_words
        filtered_words = [
            word for word in words
            if len(word) >= int(min_length) 
            and word not in used_words 
            and req_word.lower() in word.lower() 

        ]

        # print("Filtered words:", filtered_words)

        if not filtered_words:
            return None  # Return None if no words are available

        if spam_word:
            spam_filtered = [word for word in filtered_words if word.endswith(spam_word)]
            if spam_filtered:
                return random.choice(spam_filtered)
                
        # If no words end with spam_word, check for words ending with 'y'
        y_filtered = [word for word in filtered_words if word.endswith('y')]
        
        if y_filtered:
            return random.choice(y_filtered)
        
        return random.choice(filtered_words)  # Return any other random filtered word

    except FileNotFoundError:
        # print(f"File for start word '{start_word}' not found.")
        return None

    except ValueError:
        # print("Please enter a valid number for length.")
        return None

