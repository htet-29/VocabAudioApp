import vocab2audio

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading

# Handle imports whether running from source or as a PyInstaller binary
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


class VocabAudioGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Vocab Audio Generator")
        self.root.geometry("620x420")

        # CSV Selection
        tk.Label(root, text="CSV File:").grid(
            row=0, column=0, padx=10, pady=12, sticky="e"
        )
        self.csv_path = tk.StringVar()
        tk.Entry(root, textvariable=self.csv_path, width=45).grid(
            row=0, column=1, padx=10, pady=12
        )
        tk.Button(root, text="Browse", command=self.browse_csv).grid(
            row=0, column=2, padx=10, pady=12
        )

        # Output Folder Selection
        tk.Label(root, text="Output Directory:").grid(
            row=1, column=0, padx=10, pady=12, sticky="e"
        )
        self.out_path = tk.StringVar()
        tk.Entry(root, textvariable=self.out_path, width=45).grid(
            row=1, column=1, padx=10, pady=12
        )
        tk.Button(root, text="Browse", command=self.browse_out).grid(
            row=1, column=2, padx=10, pady=12
        )

        # Action Button
        self.generate_btn = tk.Button(
            root,
            text="Generate MP3 Files",
            command=self.start_generation,
            bg="#2e7d32",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=10,
            pady=5,
        )
        self.generate_btn.grid(row=2, column=1, pady=15)

        # Output Terminal Log Window
        self.log_area = scrolledtext.ScrolledText(
            root, width=70, height=12, state="disabled"
        )
        self.log_area.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def browse_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filename:
            self.csv_path.set(filename)

    def browse_out(self):
        dirname = filedialog.askdirectory()
        if dirname:
            self.out_path.set(dirname)

    def log_message(self, message: str):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")

    def start_generation(self):
        csv_file = self.csv_path.get()
        out_dir = self.out_path.get()

        if not os.path.exists(csv_file) or not out_dir:
            messagebox.showerror(
                "Error", "Please select a valid CSV file and Output Directory."
            )
            return

        self.log_message(f"Starting process...\nOutput path: {out_dir}\n")
        self.generate_btn.config(state="disabled")

        threading.Thread(
            target=self.run_generator, args=(csv_file, out_dir), daemon=True
        ).start()

    def run_generator(self, csv_file: str, out_dir: str):
        logger = vocab2audio.setup_logger()
        try:
            vocab2audio.generate_mp3_files(csv_file, out_dir, logger)
            self.log_message("\nStatus: Process Completed Successfully!")
        except Exception as e:
            self.log_message(f"\nStatus: Failed due to an error: {e}")
        finally:
            self.generate_btn.config(state="normal")


def main():
    root = tk.Tk()
    VocabAudioGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
