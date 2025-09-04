# ui.py
# This file contains the GUI definition for the KryptBoard emulator.

import tkinter as tk
from tkinter import ttk
import string
import base64
from Crypto.Random import get_random_bytes

# Import functions/data from other modules
from crypto_aead import aead_encrypt
from keyboard_map import keyboard_layout

class KryptBoardGUI:
    def __init__(self, master):
        self.master = master
        master.title("KryptBoard Emulator")

        # Configure grid weights for resizing
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(4, weight=1) # Give keyboard area vertical weight

        # Encrypted Output Area
        self.encrypted_label = ttk.Label(master, text="Encrypted Output (Base64: Nonce | Ciphertext | Tag):")
        self.encrypted_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.encrypted_output = tk.Text(master, height=3, state="disabled", wrap="word")
        self.encrypted_output.grid(row=1, column=0, sticky="ew", padx=5, pady=2)

        # Plaintext Output Area
        self.plaintext_label = ttk.Label(master, text="Plaintext Output:")
        self.plaintext_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        # Change state to normal to allow insertion, but we will manage it to be visually read-only
        self.plaintext_output = tk.Text(master, height=3, state="normal", wrap="word")
        self.plaintext_output.grid(row=3, column=0, sticky="ew", padx=5, pady=2)
        # Make it visually read-only by preventing user edits
        self.plaintext_output.bind("<Key>", lambda e: "break") # Prevent direct typing
        self.plaintext_output.bind("<ButtonPress-1>", lambda e: "break") # Prevent clicking


        self.keyboard_frame = ttk.Frame(master, relief="groove", borderwidth=2)
        self.keyboard_frame.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

        self.keyboard_layout = [
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
            ['Caps Lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'Enter'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift'],
            ['Ctrl', 'Alt', ' ', 'Alt', 'Ctrl'] # Simplified bottom row
        ]

        self.key_widgets = {} # Dictionary to store key widgets for easy access

        # Build the virtual keyboard using the imported layout
        self.key_widgets = {} # Dictionary to store key widgets for easy access

        # Build the virtual keyboard with adjusted layout for the bottom row
        for row_index, row_keys in enumerate(keyboard_layout):
            self.keyboard_frame.grid_rowconfigure(row_index, weight=1)
            # Configure column weights for flexibility in this row
            for col_index, key_char in enumerate(row_keys):
                self.keyboard_frame.grid_columnconfigure(col_index, weight=1, uniform="a")

            # Special handling for the last row to adjust space bar and surrounding keys
            if row_index == len(keyboard_layout) - 1: # Check if it's the last row
                current_col = 0
                for key_char in row_keys:
                    key_button = ttk.Button(self.keyboard_frame, text=key_char, width=4)
                    self.key_widgets[key_char.lower()] = key_button

                    if key_char == ' ': # Space bar
                        # Give space bar a larger columnspan and place it
                        space_bar_column = current_col # Store the starting column for space
                        space_bar_span = 5 # Adjust this value as needed
                        key_button.grid(row=row_index, column=space_bar_column, sticky="nsew", padx=1, pady=1, columnspan=space_bar_span)
                        current_col += space_bar_span # Move the current column past the space bar
                    else:
                        # Place other keys in the last row
                        key_button.grid(row=row_index, column=current_col, sticky="nsew", padx=1, pady=1)
                        current_col += 1 # Move to the next column

            else: # Handle other rows as before
                for col_index, key_char in enumerate(row_keys):
                    key_button = ttk.Button(self.keyboard_frame, text=key_char, width=4)
                    key_button.grid(row=row_index, column=col_index, sticky="nsew", padx=1, pady=1)
                    self.key_widgets[key_char.lower()] = key_button # Store widget, use lower for case-insensitive mapping

                    # Adjust width for special keys (except space, handled in the last row logic)
                    if key_char in ['Backspace', 'Tab', 'Caps Lock', 'Enter', 'Shift']:
                        key_button.config(width=8) # Example width adjustment, can be more precise

        # Note: The previous space bar specific grid call within the general loop is removed
        # as the last row is now handled separately.

        # Buttons Area (rest of __init__ remains the same)
        self.button_frame = ttk.Frame(master)
        self.button_frame.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

        self.send_plaintext_button = ttk.Button(self.button_frame, text="Send (plaintext)", command=self.send_plaintext)
        self.send_plaintext_button.pack(side="left", padx=5, expand=True, fill="x")

        self.send_encrypted_button = ttk.Button(self.button_frame, text="Send (encrypted)", command=self.send_encrypted)
        self.send_encrypted_button.pack(side="left", padx=5, expand=True, fill="x")

        self.reset_key_button = ttk.Button(self.button_frame, text="Reset Key", command=self.reset_encryption_key)
        self.reset_key_button.pack(side="left", padx=5, expand=True, fill="x")

        # Bind real keypress events
        self.master.bind("<KeyPress>", self.on_key_press)
        self.master.bind("<KeyRelease>", self.on_key_release)

        # Generate a random 32-byte key on initialization
        self.encryption_key = get_random_bytes(32)

        # Custom style for pressed button state
        style = ttk.Style()
        style.configure("Pressed.TButton", background="lightblue") # You can choose any color

    # ... rest of the KryptBoardGUI class methods (on_key_press, on_key_release, clear_output_widgets, send_plaintext, send_encrypted, reset_encryption_key) remain the same.

        # Buttons Area
        self.button_frame = ttk.Frame(master)
        self.button_frame.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

        self.send_plaintext_button = ttk.Button(self.button_frame, text="Send (plaintext)", command=self.send_plaintext)
        self.send_plaintext_button.pack(side="left", padx=5, expand=True, fill="x")

        self.send_encrypted_button = ttk.Button(self.button_frame, text="Send (encrypted)", command=self.send_encrypted)
        self.send_encrypted_button.pack(side="left", padx=5, expand=True, fill="x")

        self.reset_key_button = ttk.Button(self.button_frame, text="Reset Key", command=self.reset_encryption_key)
        self.reset_key_button.pack(side="left", padx=5, expand=True, fill="x")

        # Bind real keypress events
        self.master.bind("<KeyPress>", self.on_key_press)
        self.master.bind("<KeyRelease>", self.on_key_release)

        # Generate a random 32-byte key on initialization
        self.encryption_key = get_random_bytes(32)

        # Custom style for pressed button state
        style = ttk.Style()
        style.configure("Pressed.TButton", background="lightblue") # You can choose any color


    def on_key_press(self, event):
        key_char = event.char
        keysym = event.keysym

        # Handle printable characters, including space, but *excluding* space for button activation
        if len(key_char) == 1 and key_char in string.printable and keysym not in ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Return', 'BackSpace', 'Tab']:
            # Insert character into plaintext
            self.plaintext_output.config(state="normal") # Enable editing temporarily
            self.plaintext_output.insert("end", key_char)
            self.plaintext_output.config(state="disabled") # Disable editing

        # Handle Backspace and update plaintext
        elif keysym == 'BackSpace':
            self.plaintext_output.config(state="normal")
            current_text = self.plaintext_output.get("1.0", "end-1c")
            if current_text:
                self.plaintext_output.delete("end-2c", "end-1c")
            self.plaintext_output.config(state="disabled")

        # Handle Enter and update plaintext
        elif keysym == 'Return':
            self.plaintext_output.config(state="normal")
            self.plaintext_output.insert("end", "\n")
            self.plaintext_output.config(state="disabled")

        # Explicitly handle Space to insert into plaintext and prevent button activation
        elif keysym == 'space':
            self.plaintext_output.config(state="normal")
            self.plaintext_output.insert("end", " ")
            self.plaintext_output.config(state="disabled")


        # After updating plaintext, encrypt and update encrypted output
        current_plaintext = self.plaintext_output.get("1.0", "end-1c")
        # Only encrypt if there is text or if backspace/enter/space resulted in changes
        if current_plaintext or keysym in ['BackSpace', 'Return', 'space']:
            try:
                plaintext_bytes = current_plaintext.encode("utf-8")
                # Use the imported aead_encrypt function
                encryption_result = aead_encrypt(plaintext_bytes, self.encryption_key)

                # Format the encrypted output string
                encrypted_display_text = f"Nonce: {encryption_result['nonce']} | Ciphertext: {encryption_result['ciphertext']} | Tag: {encryption_result['tag']}"

                # Update the encrypted output Text widget
                self.encrypted_output.config(state="normal")
                self.encrypted_output.delete("1.0", "end")
                self.encrypted_output.insert("1.0", encrypted_display_text)
                self.encrypted_output.config(state="disabled")

            except Exception as e:
                # Handle potential encryption errors
                print(f"Encryption error: {e}") # Log the error for debugging
                # Optionally update a status bar or message label in the GUI
                pass # Keep UI responsive
        elif not current_plaintext: # If plaintext is empty (e.g., after deleting all text)
            self.encrypted_output.config(state="normal")
            self.encrypted_output.delete("1.0", "end")
            self.encrypted_output.config(state="disabled")


        # Key highlighting logic
        lower_key_char = key_char.lower()
        # Handle special keys for highlighting consistently
        if keysym == 'BackSpace':
            lower_key_char = 'backspace'
        elif keysym == 'Return':
            lower_key_char = 'enter'
        elif keysym == 'Shift_L' or keysym == 'Shift_R':
            lower_key_char = 'shift'
        elif keysym == 'Control_L' or keysym == 'Control_R':
            lower_key_char = 'ctrl'
        elif keysym == 'Alt_L' or keysym == 'Alt_R':
            lower_key_char = 'alt'
        elif keysym == 'Tab':
            lower_key_char = 'tab'
        elif keysym == 'space':
            lower_key_char = ' ' # Map space key to the space character for highlighting

        if lower_key_char in self.key_widgets:
            self.key_widgets[lower_key_char].config(style="Pressed.TButton")
            # Added a temporary tag to easily find this key later for unhighlighting
            # Removed the temporary binding here to rely solely on the main KeyRelease binding
            # self.key_widgets[lower_key_char].bind("<KeyRelease>", self.on_key_release, add='+')


    def on_key_release(self, event):
        # Key unhighlighting logic
        key_char = event.char
        keysym = event.keysym

        lower_key_char = key_char.lower()
        # Handle special keys for unhighlighting consistently
        if keysym == 'BackSpace':
            lower_key_char = 'backspace'
        elif keysym == 'Return':
            lower_key_char = 'enter'
        elif keysym == 'Shift_L' or keysym == 'Shift_R':
            lower_key_char = 'shift'
        elif keysym == 'Control_L' or keysym == 'Control_R':
            lower_key_char = 'ctrl'
        elif keysym == 'Alt_L' or keysym == 'Alt_R':
            lower_key_char = 'alt'
        elif keysym == 'Tab':
            lower_key_char = 'tab'
        elif keysym == 'space':
            lower_key_char = ' ' # Map space key to the space character for unhighlighting

        # Ensure highlighting is removed for the specific key that was released
        # This check is redundant if we rely only on the main KeyRelease binding
        # if lower_key_char in self.key_widgets:
        #     self.key_widgets[lower_key_char].config(style="TButton")

        # Revert the style for ALL currently pressed buttons.
        # This is a more robust way to handle unhighlighting when multiple keys might be involved
        # (though less efficient if many keys are held down). For simplicity, we'll just try
        # to unhighlight the released key.
        if lower_key_char in self.key_widgets:
            self.key_widgets[lower_key_char].config(style="TButton")


    def clear_output_widgets(self):
        """Helper function to clear both output Text widgets."""
        self.plaintext_output.config(state="normal")
        self.plaintext_output.delete("1.0", "end")
        self.plaintext_output.config(state="disabled")

        self.encrypted_output.config(state="normal")
        self.encrypted_output.delete("1.0", "end")
        self.encrypted_output.config(state="disabled")


    def send_plaintext(self):
        """Handles the 'Send (plaintext)' button click."""
        plaintext = self.plaintext_output.get("1.0", "end-1c")
        print("Sent Plaintext:", plaintext)
        self.clear_output_widgets()

    def send_encrypted(self):
        """Handles the 'Send (encrypted)' button click."""
        encrypted_text = self.encrypted_output.get("1.0", "end-1c")
        # Parse the encrypted string to extract components
        try:
            parts = encrypted_text.split(" | ")
            if len(parts) == 3:
                nonce_b64 = parts[0].replace("Nonce: ", "")
                ciphertext_b64 = parts[1].replace("Ciphertext: ", "")
                tag_b64 = parts[2].replace("Tag: ", "")

                encrypted_data = {
                    "nonce": nonce_b64,
                    "ciphertext": ciphertext_b64,
                    "tag": tag_b64
                }
                print("Sent Encrypted Data:", encrypted_data)
            else:
                print("Error: Could not parse encrypted data string.")
        except Exception as e:
            print(f"Error parsing encrypted data: {e}")

        self.clear_output_widgets()

    def reset_encryption_key(self):
        """Generates a new encryption key and clears the output areas."""
        self.encryption_key = get_random_bytes(32)
        print("Encryption key reset.")
        self.clear_output_widgets()
