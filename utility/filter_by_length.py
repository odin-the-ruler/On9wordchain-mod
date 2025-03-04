
import random


def filter_words_by_length(start_word, min_length, spam_word=None):
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
        filtered_words = [word for word in words if len(word) >= int(min_length) and word not in used_words]

        # Debugging
        # print("Used words:", used_words)
        # print("Filtered words:", filtered_words)

        if not filtered_words:
            return None  # Return None if no words are available
        
        if spam_word:
            spam_filtered = [word for word in filtered_words if word.endswith(spam_word)]
            if spam_filtered:
                return random.choice(spam_filtered)  # Return a random word ending with spam_word
        
        selected_word = random.choice(filtered_words)
        return selected_word  # Return any other random filtered word
    
    except FileNotFoundError:
        print(f"File for start word '{start_word}' not found.")
        return None
    
    except ValueError:
        print("Please enter a valid number for length.")
        return None
