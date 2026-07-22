# 🎧 Vocab Audio Generator

A native Linux desktop application that converts CSV vocabulary lists into individual MP3 audio files using Google Text-to-Speech (gTTS).

---

## 🚀 Features

- **GUI Interface:** No command line needed. Select files and folders with a single click.
- **CSV Support:** Automatically targets the `word` column from any CSV file.
- **Smart Caching:** Skips already generated files to save time and API calls.
- **Detailed Logs:** Generates a `generation.log` inside your target folder.

---

# Installation

## Download from the Release tab

## 🛠️ Build & Install from Source

### Prerequisites

- Python 3.10+
- `pip`

```bash
# 1. Clone the repository
git clone [https://github.com/YOUR_USERNAME/VocabAudioApp.git](https://github.com/YOUR_USERNAME/VocabAudioApp.git)
cd VocabAudioApp

# 2. Set up virtual environment and dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Build standalone binary
pyinstaller --onefile --windowed --name="vocab-audio" src/gui_app.py

# 4. Run the automated installer
chmod +x install.sh
./install.sh
```
