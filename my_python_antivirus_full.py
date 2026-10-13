"""
MY PYTHON ANTIVIRUS — BEGINNER PROJECT
-------------------------------------
A simple educational desktop interface that scans a chosen folder for the
harmless EICAR antivirus test signature.

IMPORTANT:
- This is a learning demonstration, NOT a full antivirus.
- It does not delete, modify, or quarantine files.
- "No test signature found" does NOT mean a file is safe.
- Scan only folders you own or are authorized to inspect.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

# Harmless standard test signature used by antivirus vendors to test detection.
EICAR_TEST_STRING = (
    b"X5O!P%@AP[4\\PZX54(P^)7CC)7}"
    b"$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
)


class AntivirusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Python Antivirus")
        self.root.geometry("760x560")
        self.root.minsize(620, 440)

        self.folder = None
        self.scanning = False

        # App heading
        tk.Label(
            root,
            text="🛡 My Python Antivirus",
            font=("Arial", 21, "bold"),
            fg="#167D5A",
        ).pack(pady=(18, 3))

        tk.Label(
            root,
            text="Educational file scanner",
            font=("Arial", 10),
            fg="#555555",
        ).pack(pady=(0, 14))

        # Folder picker area
        folder_frame = tk.Frame(root)
        folder_frame.pack(fill="x", padx=18)

        self.folder_label = tk.Label(
            folder_frame,
            text="No folder selected",
            anchor="w",
            relief="groove",
            padx=8,
            pady=8,
        )
        self.folder_label.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.choose_button = tk.Button(
            folder_frame,
            text="Choose Folder",
            command=self.choose_folder,
        )
        self.choose_button.pack(side="right")

        # Scan and clear buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=12)

        self.scan_button = tk.Button(
            button_frame,
            text="Start Scan",
            command=self.scan_folder,
            bg="#167D5A",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=18,
            pady=7,
        )
        self.scan_button.pack(side="left", padx=5)

        self.clear_button = tk.Button(
            button_frame,
            text="Clear Results",
            command=self.clear_results,
            padx=12,
            pady=7,
        )
        self.clear_button.pack(side="left", padx=5)

        self.status_label = tk.Label(
            root,
            text="Status: Ready",
            anchor="w",
            font=("Arial", 10, "bold"),
        )
        self.status_label.pack(fill="x", padx=18, pady=(0, 8))

        tk.Label(
            root,
            text="Scan Results",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w", padx=18)

        # Results text box and scrollbar
        results_frame = tk.Frame(root)
        results_frame.pack(fill="both", expand=True, padx=18, pady=(5, 10))

        scrollbar = tk.Scrollbar(results_frame)
        scrollbar.pack(side="right", fill="y")

        self.results = tk.Text(
            results_frame,
            wrap="word",
            yscrollcommand=scrollbar.set,
            height=14,
            state="disabled",
        )
        self.results.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.results.yview)

        # Initial messages
        self.add_result("Welcome! Choose a folder, then click Start Scan.")
        self.add_result("This demo checks only for the harmless EICAR test signature.")
        self.add_result("It will not delete or modify your files.")

    def add_result(self, message):
        """Add one line to the results box."""
        self.results.config(state="normal")
        self.results.insert("end", message + "\n")
        self.results.see("end")
        self.results.config(state="disabled")

    def choose_folder(self):
        """Let the user select a folder to scan."""
        selected = filedialog.askdirectory(title="Choose a folder you own")
        if selected:
            self.folder = Path(selected)
            self.folder_label.config(text=str(self.folder))
            self.status_label.config(text="Status: Folder selected")
            self.add_result(f"Selected folder: {self.folder}")

    def clear_results(self):
        """Clear the text shown in the results box."""
        self.results.config(state="normal")
        self.results.delete("1.0", "end")
        self.results.config(state="disabled")
        self.status_label.config(text="Status: Results cleared")

    def scan_folder(self):
        """Scan the chosen folder for the harmless test signature."""
        if self.scanning:
            return

        if self.folder is None:
            messagebox.showinfo("Choose a folder", "Please choose a folder first.")
            return

        if not self.folder.exists() or not self.folder.is_dir():
            messagebox.showerror("Folder error", "The selected folder cannot be found.")
            return

        self.scanning = True
        self.scan_button.config(state="disabled")
        self.choose_button.config(state="disabled")
        self.clear_button.config(state="disabled")
        self.status_label.config(text="Status: Scanning...")
        self.add_result(f"\n--- Scan started: {self.folder} ---")
        self.root.update_idletasks()

        checked = 0
        detected = 0
        skipped = 0

        try:
            for path in self.folder.rglob("*"):
                if not path.is_file():
                    continue

                try:
                    contents = path.read_bytes()
                    checked += 1

                    if EICAR_TEST_STRING in contents:
                        detected += 1
                        self.add_result(f"[TEST SIGNATURE FOUND] {path}")
                    else:
                        self.add_result(f"[No test signature found] {path}")

                except (PermissionError, OSError) as error:
                    skipped += 1
                    self.add_result(f"[Skipped: cannot read file] {path} ({error})")

                # Keep the window responsive while the scan proceeds.
                self.root.update_idletasks()

        except (PermissionError, OSError) as error:
            self.add_result(f"Folder scanning issue: {error}")

        self.add_result("--- Scan finished ---")
        self.add_result(f"Files checked: {checked}")
        self.add_result(f"Test signatures found: {detected}")
        self.add_result(f"Files skipped: {skipped}")
        self.add_result("Reminder: this scanner does not detect every kind of malware.")

        self.status_label.config(
            text=f"Status: Finished — checked {checked} file(s); test signatures found: {detected}"
        )

        self.scanning = False
        self.scan_button.config(state="normal")
        self.choose_button.config(state="normal")
        self.clear_button.config(state="normal")

        messagebox.showinfo(
            "Scan complete",
            f"Files checked: {checked}\n"
            f"Test signatures found: {detected}\n"
            f"Files skipped: {skipped}\n\n"
            "This educational scanner does not detect every kind of malware.",
        )


def main():
    root = tk.Tk()
    AntivirusApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
