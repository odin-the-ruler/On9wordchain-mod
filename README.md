# On9WordChain-Mod Bot v1.5.1 🚀

![On9WordChain-Mod](asset/logo.jpg)

Welcome to **On9WordChain-Mod Bot**, the ultimate Telegram bot designed to enhance and automate your On9WordChain game! With multiple game modes and customizable settings, this bot ensures a fun, challenging, and dynamic word-chaining experience.

---

## ✨ Key Features

🔥 **Self-Learning Dictionary** – The bot expands its vocabulary as you play!  
✅ **Start & Stop** the game in any chat  
✅ **Set a Custom Spam Word**  
✅ **Clear Used Words** with ease  
✅ **Adjust Message Delay Times**  
✅ **Switch Game Modes Instantly**  
✅ **Track & Log Words in Real-Time**  
✅ **Live Game Status Updates**  
✅ **User-Friendly & Intuitive Commands**  
✅ **Easy Dictionary Management: Read, Write & Verify Words**  

### 🚀 Unique Feature: Self-Learning Dictionary
The bot automatically learns new words as users play. If a word isn’t found in the dictionary, it gets added instantly. This ensures continuous improvement and evolving gameplay. When updating the bot, remember to transfer your existing dictionary file (`sorted_words`) to retain learned words.

---

## 🧐 Installation Guide

### Running on a Local Machine 🖥️

### 🔹 Prerequisites
Before installing, ensure you have:
- **Python 3.8+** installed
- **Git** installed (for repository cloning)
- **Telegram API Credentials** (API ID & API HASH from [my.telegram.org](https://my.telegram.org))
- Your **Telegram User ID**

#### 1️⃣ Install Dependencies

🔹 **For Linux/macOS**:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git -y
pip install --upgrade pip
```

🔹 **For Windows** (Using PowerShell):
1. Install Python from [**python.org**](https://www.python.org/)
2. Install Git from [**git-scm.com**](https://git-scm.com/)
3. Install dependencies:
```bash
pip install --upgrade pip
```

#### 2️⃣ Clone the Repository
```bash
git clone https://github.com/your-repository/On9WordChain-Mod.git
cd On9WordChain-Mod
```

#### 3️⃣ Install Required Python Packages
```bash
pip install -r requirements.txt
```

#### 4️⃣ Configure Environment Variables
Create a `.env` file and add your credentials:
```env
API_ID=your_api_id
API_HASH=your_api_hash
MY_USER_ID=your_telegram_user_id
```
Replace `your_api_id`, `your_api_hash`, and `your_telegram_user_id` with your actual credentials.

---

## 📱 Running on Termux (Android)

### Perfect for On-the-Go Use! 🚀

#### 1️⃣ Install Termux
- Download **Termux** from [Google Play Store](https://play.google.com/store/apps/details?id=com.termux)
- Open Termux after installation

#### 2️⃣ Update & Upgrade Termux
```bash
pkg update && pkg upgrade -y
```

#### 3️⃣ Install Python & Required Packages
```bash
pkg install python3 -y
pkg install python-pip -y
pip install telethon
pip install python-dotenv
```

#### 4️⃣ Allow Storage Access
```bash
termux-setup-storage
```
Press **Allow** when prompted.

#### 5️⃣ Download & Extract the Project
```bash
cd ~/storage/downloads
unzip On9WordChain-Mod-master.zip
cd On9WordChain-Mod-master
```

#### 6️⃣ Create & Edit the Environment File
```bash
nano .env
```

```env
API_ID='123456789' # your api id
API_HASH='agsie86c3edfr6fbtb3r6wr' # your api hash
MY_USER_ID='987654321' # your telegram user id
```
Copy and paste your API credentials, then save the file (**CTRL + X → Y → Enter**).

#### 7️⃣ Run the Bot 🎮
```bash
python main.py
```
Your bot is now up and running! 🚀

---

## 🎮 Running the Bot

▶️ **Start the Bot**
```bash
python main.py
```

⏹ **Stop the Bot** Press **CTRL + C** in the terminal.

---

## 🤖 Bot Commands

🎲 **Game Commands:**
- `/pw` – Start the game
- `/e` – Stop the game
- `/status` – Show current game status
- `/clear` – Clear all words

⚙ **Configuration Commands:**
- `/spam <word>` – Set a custom spam word
- `/spam default` – Reset spam word
- `/time <seconds>` – Set custom message delay
- `/mode <mode>` – Change game mode (class, hard, req, cfl)
- `/h` – Show help message

☠️ **Advanced Commands (Use with Caution):**
⚠️ **Warning:** Only modify these if you understand their impact.
- `/myword <word>` – Check if a word is in your dictionary
- `/addword <word>` – Add a word to your dictionary
- `/rmword <word>` – Remove a word from your dictionary

---

## 🛠️ Troubleshooting Common Issues

❌ **ModuleNotFoundError: No module named 'telethon'**
```bash
pip install telethon
```

❌ **Bot Not Responding in Telegram**
- Ensure the bot is **running** on your machine
- Check if **API credentials** are correctly set in `.env`
- Restart the bot: (**CTRL + C**, then run `python main.py` again)

---

## 🤝 Contributing

Want to improve **On9WordChain-Mod Bot**? We'd love your help! 😃

🔹 **Fork the repository**  
🔹 **Create a new branch** for your feature or bug fix  
🔹 **Submit a pull request** with a detailed explanation  

---

## 🐝 License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute it!

---

## 📞 Contact & Support

For any issues or suggestions, feel free to reach out via Telegram or create an issue on GitHub.

📩 TG: [Telegram ID](https://t.me/drecocox)

🔥 **Happy Gaming!** 🎮🚀

