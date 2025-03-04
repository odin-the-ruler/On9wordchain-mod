import asyncio
import re
from telethon import TelegramClient, events
import os
import dotenv
import sys

import random
from utility.filter_by_length import filter_words_by_length
from utility.fillter_by_req import filter_words_by_req_word

# Set the default encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

dotenv.load_dotenv()

# Load API credentials from environment variables
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

# Variable to store the spam word
spam_word = None
mode = 'hard'
# Your Telegram user ID (replace with your actual ID)
MY_USER_ID = int(os.getenv("MY_USER_ID"))  # Replace with your real user ID

# Variable to store the bot ID to track
tracked_bot_id = 'on9wordchainbot'

# Variable to store the spam word
spam_word = None

# Variable to store the custom delay time
custom_delay = 10
SORTED_DIR = 'sorted_words'
client = TelegramClient("session_name", api_id, api_hash)
# Dictionary to track active chats and file names
active_chats = {}

def update_word_set(file_path, w1):
    # Read existing words from the file into a set
    try:
        with open(file_path, "r") as file:
            word_set = set(file.read().splitlines())
    except FileNotFoundError:
        word_set = set()

    # Check if w1 is in the set
    if w1 not in word_set:
        word_set.add(w1)
        print(f"Word '{w1}' added to the dictionary")
        # Save the updated set back to the file
        with open(file_path, "w") as file:
            file.write("\n".join(sorted(word_set)))
    print(f"Word '{w1}' already exists in the dictionary")


@client.on(
    events.NewMessage(pattern='/pw', outgoing=True, from_users=MY_USER_ID))
async def start_game(event):
    chat_id = event.chat_id
    chat_name = (await event.get_chat()).title or "Private Chat"
    active_chats[chat_id] = chat_name
    async with client.action('me', 'typing'):
        await asyncio.sleep(2)
        await client.send_message(
            'me', f"Game started in {chat_name}. Tracking words...")
    await event.delete()  # Delete the /play command message

@client.on(events.NewMessage(pattern='/mode (.*)', outgoing=True))
async def set_mode(event):
    global mode
    mode_input = event.pattern_match.group(1).strip().lower()

    # Check if the mode is valid
    if mode_input not in ["hard", "class", "req" ,"cfl"]:
        async with client.action('me', 'typing'):
            await asyncio.sleep(2)
            await client.send_message('me', "❌ Invalid mode! Please use either 'hard', 'class' ,'cfl', or 'req'.")
            await event.delete()
            return  # Exit the function without changing the mode

    mode = mode_input  # Assign mode only if it's valid
    async with client.action('me', 'typing'):
        await asyncio.sleep(2)
        await client.send_message('me', f"✅ Game mode set to **{mode}**")
        await event.delete()


@client.on(events.NewMessage(pattern='/spam (.*)', outgoing=True))
async def set_spam_word(event):
    global spam_word
    spam_word_input = event.pattern_match.group(1).strip()
    if spam_word_input.lower() == "default":
        spam_word = None
        async with client.action('me', 'typing'):
            await asyncio.sleep(2)
            await client.send_message('me', "Spam word reset to default.")
    else:
        spam_word = spam_word_input
        async with client.action('me', 'typing'):
            await asyncio.sleep(2)
            await client.send_message('me', f"Spam word set to '{spam_word}'.")
    await event.delete()  # Delete the /spam command message


@client.on(
    events.NewMessage(pattern='/clear', outgoing=True, from_users=MY_USER_ID))
async def clear_used_words(event):
    with open("usedword.txt", "w", encoding='utf-8') as f:
        f.truncate(0)  # Clear the file content
    async with client.action('me', 'typing'):
        await asyncio.sleep(2)
        await client.send_message(
            'me', "All words have been cleared from usedword.txt.")
        await event.delete()  # Delete the /clear command message


@client.on(
    events.NewMessage(pattern='/e', outgoing=True, from_users=MY_USER_ID))
async def stop_game(event):
    chat_id = event.chat_id
    if chat_id in active_chats:
        chat_name = active_chats.pop(chat_id)
        async with client.action('me', 'typing'):
            await asyncio.sleep(2)
            await client.send_message('me', f"Game stopped in {chat_name}.")
    else:
        async with client.action('me', 'typing'):
            await asyncio.sleep(2)
            await client.send_message('me', "No active game found in this chat.")
    await event.delete()  # Delete the /e command message

@client.on(events.NewMessage(pattern ='/myword (.*)',outgoing=True))
async def checkifwordexist(event):
    word = event.pattern_match.group(1)
    first_letter = word[0].lower()
    file_path = os.path.join(SORTED_DIR, f"{first_letter}.txt")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            words = file.read().splitlines()
        
        if word in words:
            await event.reply(f"✅ Word '{word.lower()}' exists in `{first_letter}.txt`")
        else:
            await event.reply(f"❌ Word '{word.lower()}' is NOT found in `{first_letter}.txt`")
    else:
        await event.reply(f"❌ No file found for `{first_letter}.txt`")


@client.on(events.NewMessage(pattern='/time (\d+)', outgoing=True))
async def set_custom_delay(event):
    global custom_delay
    delay_input = event.pattern_match.group(1).strip()
    try:
        custom_delay = int(delay_input)
        async with client.action('me', 'typing'):
            await asyncio.sleep(2)
            await client.send_message(
            'me', f"Custom delay set to {custom_delay} seconds.")
    except ValueError:
        async with client.action('me', 'typing'):
            await asyncio.sleep(2)
            await client.send_message(
                'me', "Invalid delay value. Please enter a valid number.")
    await event.delete()  # Delete the /time command message


@client.on(events.NewMessage(pattern='/status', outgoing=True))
async def show_status(event):
    active_games = "\n".join(
        [f"- {chat_name}"
         for chat_name in active_chats.values()]) or "No active games."
    spam_word_status = spam_word or "None"
    used_words_count = 0
    used_words_by_letter = {}
    total_words_count = 0

    try:
        with open('usedword.txt', 'r', encoding='utf-8') as used_file:
            used_words = used_file.readlines()
            used_words_count = len(used_words)
            for word in used_words:
                first_letter = word.strip()[0].lower()
                if first_letter in used_words_by_letter:
                    used_words_by_letter[first_letter] += 1
                else:
                    used_words_by_letter[first_letter] = 1
    except FileNotFoundError:
        used_words_count = 0

    used_words_summary = "\n".join([
        f"{letter.upper()}: {count} used"
        for letter, count in used_words_by_letter.items()
    ]) or "No words used."

    # Count total words in the sorted_words directory
    for filename in os.listdir(SORTED_DIR):
        if filename.endswith(".txt"):
            with open(os.path.join(SORTED_DIR, filename), 'r', encoding='utf-8') as file:
                total_words_count += len(file.readlines())

    status_message = (f"Active games:\n{active_games}\n\n"
                      f"Spam word: {spam_word_status}\n"
                      f"Total words used: {used_words_count}\n"
                      f"Words used by starting letter:\n{used_words_summary}\n"
                      f"Total words in dictionary: {total_words_count}\n"
                      f"Custom delay time: {custom_delay} seconds\n"
                      f"Game mode: {mode}")
    async with client.action(event.chat_id, 'typing'):
        await asyncio.sleep(2)
        await client.send_message(event.chat_id, status_message)
        await event.delete()  # Delete the /status command message


@client.on(events.NewMessage(pattern='/h', outgoing=True))
async def send_help(event):
    help_message = ("Available commands:\n"
                    "/pw - Start the game in the current chat\n"
                    "/spam <word> - Set the spam word\n"
                    "/spam default - Reset the spam word to default\n"
                    "/clear - Clear all words\n"
                    "/e - Stop the game in the current chat\n"
                    "/time <seconds> - Set custom delay between messages\n"
                    "/status - Show the status of the game\n"
                    "/h - Show this help message",
                    "`/myword <word>` - Check if a word exists in the dictionary\n"
                    "`/addword <word>` - add word to your dictionary\n"
                    "`/remword <word>` - remove word from your dictionary\n"
                    "/mode <mode> - Set the mode of the game [class,hard,req ,cfl]"
                    )
    async with client.action(event.chat_id, 'typing'):
        await asyncio.sleep(2)
        await client.send_message(event.chat_id, help_message)
        await event.delete()  # Delete the /h command message
@client.on(events.NewMessage(pattern=r"/addword (.*)", outgoing=True))
async def add_word(event):
    word = event.pattern_match.group(1).strip()
    first_letter = word[0].lower()
    file_path = f'sorted_words/{first_letter}.txt'

    # Debugging: Check the file path
    # print(f"File path: {file_path}")

    # Read existing words
    words = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            words = file.read().splitlines()

    # print(f"Before adding: {words}")

    if word not in words:
        words.append(word)
        words.sort()
        # print(f"After adding: {words}")  # Debugging

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(words))

        await asyncio.sleep(1)  # Ensure file write completes
        await event.reply(f"✅ Word '{word.lower()}' added to `{file_path}`")
    else:
        await event.reply(f"⚠️ Word '{word.lower()}' is already in `{file_path}`")
@client.on(events.NewMessage(pattern=r"/rmword (.*)", outgoing=True))
async def remove_word(event):
    word = event.pattern_match.group(1).strip().lower()
    first_letter = word[0].lower()
    file_path = f"sorted_words/{first_letter}.txt"

    # Debugging: Check file path
    # print(f"File path: {file_path}")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            words = file.read().splitlines()

        # print(f"Words before removal: {words}")  # Debugging

        words = [w.strip().lower() for w in words]  # Normalize words

        if word in words:
            words.remove(word)

            with open(file_path, "w", encoding="utf-8") as file:
                file.write("\n".join(words))

            # print(f"Words after removal: {words}")  # Debugging
            await asyncio.sleep(1)  # Ensure write completes
            await event.reply(f"✅ Word '{word}' removed from `{file_path}`")
        else:
            await event.reply(f"⚠️ Word '{word}' not found in `{file_path}`")
    else:
        await event.reply(f"⚠️ No words found under `{file_path}`")
@client.on(events.NewMessage(from_users=tracked_bot_id))
async def track_words(event):
    chat_id = event.chat_id
    if chat_id in active_chats:
        chat_name = active_chats[chat_id]
        if event.text.startswith("Turn:"):  # Checking if it's a turn message
            if f"(tg://user?id={MY_USER_ID})" in event.text:
                # print(mode)
                if mode == 'hard' or mode == 'class' or mode == 'cfl':
                    match = re.search(
                        r"Your word must start with __(.*?)__ and include \*\*at least (\d+) letters\*\*",
                        event.text)
                    if match:
                        starting_letter = match.group(1)
                        min_length = match.group(2)
                        # print(
                        #     f"Word must start with: {starting_letter}, Length: {min_length}"
                        # )

                        # Find and send a random word
                        word = filter_words_by_length(starting_letter.lower(),min_length, spam_word)
                        if word:
                            async with client.action(chat_id, 'typing'):
                                await asyncio.sleep(custom_delay)
                                await client.send_message(chat_id, word.capitalize())
                                # print(f"Sent word '{word}' to {chat_name}")
                elif mode == 'req':
                    pattern = r"start with __([A-Z])__, \*\*include\*\* __([A-Z])__ and \*\*at least (\d+) letters\*\*"
                    match = re.search(pattern, event.text)
                    if match:
                        start_letter = match.group(1).upper()
                        include_letter = match.group(2).upper()
                        min_length = int(match.group(3))
                        # print(start_letter, include_letter, min_length)
                        word = filter_words_by_req_word(start_word=start_letter.lower(),min_length=min_length,req_word=include_letter,spam_word=spam_word)
                        # print("word",word)  
                        if word:
                            async with client.action(chat_id, 'typing'):
                                await asyncio.sleep(custom_delay)
                                await client.send_message(chat_id, word.capitalize())
                                print(f"Sent word '{word}' to {chat_name}")
                    # print('req mode')
                else:
                    async with client.action('me', 'typing'):
                        await asyncio.sleep(2)
                        await client.send_message('me', "Invalid mode set in the game choose from [class,hard,req,cfl]")
                        print('Invalid mode set in the game choose from [class,hard,req,cfl]')
                    # print(event.text)
        elif "is accepted." in event.text:
                # Extract the word from the event text
                match = re.search(r"__(.*?)__", event.text)
                if match:
                    word = match.group(1).strip().lower()  # Remove any unwanted spaces
                    with open("usedword.txt", "a", encoding='utf-8') as f:
                        f.write(word + "\n")
                   # print(f"Word '{word}' recorded in usedword.txt")

                    first_letter = word[0].lower()
                    file_path = f"sorted_words/{first_letter}.txt"

                    # Update the word set
                    update_word_set(file_path, word)




async def main():
    await client.start()
    myinfo = await client.get_me()
    
    welcome_message = (
    f"👋 **Hello, {myinfo.first_name}!**\n\n"
    "🚀 **On9WordChain-Mod Bot v1.5.1 is now online and ready to play!**\n\n"
    "🔹 **How to Play?**\n"
    "I’m here to run a fun Word Chain game! Below are the commands you can use:\n\n"
    
    "🎮 **Game Commands:**\n"
    "➡️ `/pw` - Start the game in this chat\n"
    "➡️ `/spam <word>` - Set a custom spam word\n"
    "➡️ `/spam default` - Reset spam word to default\n"
    "➡️ `/clear` - Clear all words from the game\n"
    "➡️ `/e` - Stop the game in this chat\n"
    "➡️ `/time <seconds>` - Set custom delay between messages\n"
    "➡️ `/status` - Check the current game status\n"
    "➡️ `/h` - Show this help message\n"
    "➡️ `/mode <mode>` - Change game mode [class, hard, req, cfl]\n\n"
    
    "🔥 **Self-Learning Dictionary!** 🔥\n"
    "The bot **automatically learns new words** as users play. If a word isn't found, it gets added instantly!\n"
    "⚠️ **Warning:** Do **not** modify the dictionary manually unless necessary.\n\n"

    "☠️ **Advanced Commands (Use with Caution):**\n"
    "⚠️ **Warning:** Only modify these if you understand their impact.\n"
    "➡️ `/myword <word>` - Check if a word exists in the dictionary\n"
    "➡️ `/addword <word>` - Add a word to your dictionary\n"
    "➡️ `/rmword <word>` - Remove a word from your dictionary\n"
    "⚠️ **Misuse of these commands can break gameplay. If unsure, avoid using them!**\n\n"

    "💡 **Tip:** Try switching modes for a different challenge! 🎭\n\n"
    "⚠️ **Note:** Don't forget to use the `/clear` command before starting a game!\n\n"
    "🔥 **Let’s play and have some fun!**"
    )

    async with client.action('me', 'typing'):
        await asyncio.sleep(2)
        await client.send_message('me', welcome_message)
        print("✅ Bot v1.5.1 started successfully! Welcome message sent.")
        await client.run_until_disconnected()

client.loop.run_until_complete(main())
