import logging
import os
import csv
import re
import argparse
from pathlib import Path
from gtts import gTTS

WORD_COLUMN_NAME = "word"


def setup_logger() -> logging.Logger:
    """Configures a logger to output to both a file and the console."""
    home_dir = Path.home()

    log_file = os.path.join(str(home_dir), ".vocab2audio.log")

    logger = logging.getLogger("vocab2audio")
    logger.setLevel(logging.INFO)

    # Prevent adding handlers multiple times if called again
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_format)

        console_handler = logging.StreamHandler()
        console_format = logging.Formatter("%(message)s")
        console_handler.setFormatter(console_format)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def load_words_from_csv(file_path: str, logger: logging.Logger) -> list[str]:
    """Reads target words from a CSV file."""
    words: list[str] = []

    if not os.path.exists(file_path):
        logger.error(f"Error: CSV file '{file_path}' not found.")
        return words

    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Check if the column exists
        if reader.fieldnames is None or WORD_COLUMN_NAME not in reader.fieldnames:
            logger.error(
                f"Error: Column '{WORD_COLUMN_NAME}' not found in {file_path}."
            )
            logger.info(f"Available columns: {reader.fieldnames}")
            return words

        for row in reader:
            val = row.get(WORD_COLUMN_NAME)
            if val:
                raw_word = val.strip()
                if raw_word:
                    words.append(raw_word)

    return words


def generate_mp3_files(csv_file: str, output_dir: str, logger: logging.Logger) -> None:
    words = load_words_from_csv(csv_file, logger)

    if not words:
        logger.warning("No words found to process.")
        return

    logger.info(f"Loaded {len(words)} words from '{csv_file}'. Generating MP3s...\n")

    for word in words:
        # Clean text for speech (e.g., handles parenthetical notes if present)
        clean_text = word.split("(")[0].strip()

        # Safe filename creation (replaces spaces with underscores, removes special chars)
        safe_filename = re.sub(
            r'[\\/*?:"<>|]', "", clean_text.lower().replace(" ", "_")
        )
        file_path = os.path.join(output_dir, f"{safe_filename}.mp3")

        if os.path.exists(file_path):
            logger.info(f"Skipping (already exists): {safe_filename}.mp3")
            continue

        try:
            tts = gTTS(text=clean_text, lang="en", slow=False)
            tts.save(file_path)
            logger.info(f"Generated: {file_path}")
        except Exception as e:
            logger.error(f"Failed to generate audio for '{word}': {e}")

    logger.info(f"\nDone! All MP3 files are saved in './{output_dir}'")


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Generate MP3 files from a CSV vocabulary list."
    )
    parser.add_argument("csv_file", type=str, help="Path to the input CSV file")
    parser.add_argument(
        "location", type=str, help="Directory to save the generated MP3 files."
    )

    args = parser.parse_args()

    os.makedirs(args.location, exist_ok=True)

    logger = setup_logger()

    generate_mp3_files(args.csv_file, args.location, logger)


if __name__ == "__main__":
    main()
