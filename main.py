"""
null-Encrypter - A Kivy-based application for secure text and file encryption/decryption.
Author: el_tio_null <encryternull@gmail.com>
"""
import os
from pathlib import Path
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

import null_Encrypter_encryption as encryption_logic
from plyer import filechooser

class NullEncrypterApp(App):
    """The main application class for null-Encrypter."""
    input_text_widget = ObjectProperty(None)
    output_text_widget = ObjectProperty(None)
    status_log_widget = ObjectProperty(None)
    current_mode = "Null"
    secondary_key_input = ObjectProperty(None)
    log_file_path = None

    def build(self):
        """Build the user interface."""
        self.title = "null-Encrypter"

        import platform
        system = platform.system()
        
        if system == "Windows":
            encryption_logic.APP_DATA_DIR = Path("C:/null/EncryptorApp")
        else:
            encryption_logic.APP_DATA_DIR = Path(self.user_data_dir)
            
        encryption_logic.KEY_FILE = encryption_logic.APP_DATA_DIR / "key.key"
        encryption_logic.CLAVE = encryption_logic.get_or_generate_key()
        
        # Setup log file and null-txt folder in Downloads
        try:
            # Try to use Downloads folder (works on most platforms)
            import platform
            system = platform.system()
            
            if system == "Android":
                # On Android, use the public Downloads directory
                from android.storage import primary_external_storage_path
                downloads_path = Path(primary_external_storage_path()) / "Download"
            elif system == "Windows":
                downloads_path = Path.home() / "Downloads"
            elif system == "Darwin":  # macOS
                downloads_path = Path.home() / "Downloads"
            else:  # Linux and others
                downloads_path = Path.home() / "Downloads"
            
            # Create Downloads folder if it doesn't exist
            downloads_path.mkdir(parents=True, exist_ok=True)
            self.log_file_path = downloads_path / "null-Encrypter_log.txt"
            
            # Create null-txt folder for encrypted text files
            self.null_txt_path = downloads_path / "null-txt"
            self.null_txt_path.mkdir(exist_ok=True)
            
        except Exception as e:
            # Fallback to app data directory if Downloads is not accessible
            print(f"Could not access Downloads folder: {e}")
            self.log_file_path = encryption_logic.APP_DATA_DIR / "app_log.txt"
            self.null_txt_path = encryption_logic.APP_DATA_DIR / "null-txt"
            self.null_txt_path.mkdir(exist_ok=True)
        
        # Create log file if it doesn't exist
        if not self.log_file_path.exists():
            self.log_file_path.write_text("=== null-Encrypter Log File ===\n")

        # UI Constants - Modern Dark Theme
        self.theme_bg = (0.08, 0.08, 0.10, 1)      # Deep dark background
        self.theme_fg = (0.95, 0.95, 0.95, 1)      # Bright text
        self.accent_color = (0.2, 0.8, 0.9, 1)     # Bright cyan
        self.accent_hover = (0.3, 0.9, 1.0, 1)     # Lighter cyan
        self.button_primary = (0.15, 0.6, 0.75, 1) # Primary button
        self.button_secondary = (0.18, 0.18, 0.20, 1) # Secondary button
        self.input_bg = (0.12, 0.12, 0.14, 1)      # Input background
        self.input_border = (0.25, 0.25, 0.28, 1)  # Input border

        main_layout = BoxLayout(orientation="vertical", padding=25, spacing=18)
        
        # Header Section
        header_box = BoxLayout(orientation="vertical", size_hint_y=None, height=70, spacing=5)
        title_label = Label(
            text="[b]null-Encrypter[/b]", 
            markup=True,
            font_size='28sp',
            color=self.accent_color,
            size_hint_y=0.7
        )
        subtitle_label = Label(
            text="by el_tio_null | Secure Encryption",
            font_size='13sp',
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.3
        )
        header_box.add_widget(title_label)
        header_box.add_widget(subtitle_label)
        main_layout.add_widget(header_box)
        
        # Separator
        from kivy.uix.widget import Widget
        # Separator line
        separator = Widget(size_hint_y=None, height=1)
        main_layout.add_widget(separator)

        # --- Mode Selector (Tabs) ---
        mode_selector_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=45, spacing=8)
        self.modes = ["Null", "Base64", "Caesar", "Vigenere", "Morse", "Hex"]
        self.mode_buttons = {}

        for mode in self.modes:
            btn = Button(
                text=mode,
                size_hint_x=1/len(self.modes),
                background_color=self.accent_color if mode == self.current_mode else self.button_secondary,
                color=(1, 1, 1, 1) if mode == self.current_mode else self.accent_color,
                font_size='12sp',
                bold=(mode == self.current_mode)
            )
            btn.bind(on_press=self.change_mode)
            self.mode_buttons[mode] = btn
            mode_selector_box.add_widget(btn)
        
        main_layout.add_widget(mode_selector_box)

        # Secondary Key Input (Dynamic)
        self.secondary_key_container = BoxLayout(orientation="horizontal", size_hint_y=None, height=0, opacity=0, spacing=10)
        self.secondary_key_container.add_widget(Label(text="Key/Shift:", size_hint_x=0.3, color=self.accent_color))
        self.secondary_key_input = TextInput(
            multiline=False,
            background_color=self.input_bg,
            foreground_color=self.theme_fg,
            cursor_color=self.accent_color,
            padding=[10, 10, 10, 10],
            font_size='14sp'
        )
        self.secondary_key_container.add_widget(self.secondary_key_input)
        main_layout.add_widget(self.secondary_key_container)

        # Input Section with Card Style
        input_card = BoxLayout(orientation="vertical", size_hint_y=None, height=200, spacing=8)
        
        input_header = BoxLayout(orientation="horizontal", size_hint_y=None, height=35)
        input_header.add_widget(Label(
            text="[b]Input Message[/b]",
            markup=True,
            color=self.theme_fg,
            halign='left',
            size_hint_x=0.65,
            font_size='15sp'
        ))
        input_header.add_widget(Button(
            text="📋 Paste",
            size_hint_x=0.175,
            on_press=self.paste_input,
            background_color=self.button_secondary,
            color=self.accent_color,
            font_size='13sp'
        ))
        input_header.add_widget(Button(
            text="🗑️ Clear",
            size_hint_x=0.175,
            on_press=self.clear_input,
            background_color=self.button_secondary,
            color=(0.9, 0.4, 0.4, 1),
            font_size='13sp'
        ))
        input_card.add_widget(input_header)
        
        self.input_text_widget = TextInput(
            hint_text="Type or paste your message here...",
            multiline=True,
            background_color=self.input_bg,
            foreground_color=self.theme_fg,
            cursor_color=self.accent_color,
            padding=[15, 15, 15, 15],
            font_size='14sp'
        )
        input_card.add_widget(self.input_text_widget)
        main_layout.add_widget(input_card)

        # Action Buttons
        action_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=55, spacing=15)
        action_layout.add_widget(Button(
            text="🔒 Encrypt",
            on_press=self.encrypt_text,
            background_color=self.button_primary,
            color=(1, 1, 1, 1),
            bold=True,
            font_size='15sp'
        ))
        action_layout.add_widget(Button(
            text="🔓 Decrypt",
            on_press=self.decrypt_text,
            background_color=self.button_primary,
            color=(1, 1, 1, 1),
            bold=True,
            font_size='15sp'
        ))
        main_layout.add_widget(action_layout)

        # Output Section with Card Style
        output_card = BoxLayout(orientation="vertical", size_hint_y=None, height=200, spacing=8)
        
        output_header = BoxLayout(orientation="horizontal", size_hint_y=None, height=35)
        output_header.add_widget(Label(
            text="[b]Output Result[/b]",
            markup=True,
            color=self.theme_fg,
            halign='left',
            size_hint_x=0.5,
            font_size='15sp'
        ))
        output_header.add_widget(Button(
            text="📋 Copy",
            size_hint_x=0.17,
            on_press=self.copy_output,
            background_color=self.button_secondary,
            color=self.accent_color,
            font_size='12sp'
        ))
        output_header.add_widget(Button(
            text="💾 Save",
            size_hint_x=0.17,
            on_press=self.save_output_to_file,
            background_color=self.button_secondary,
            color=(0.4, 0.9, 0.4, 1),
            font_size='12sp'
        ))
        output_header.add_widget(Button(
            text="🗑️ Clear",
            size_hint_x=0.16,
            on_press=self.clear_output,
            background_color=self.button_secondary,
            color=(0.9, 0.4, 0.4, 1),
            font_size='12sp'
        ))
        output_card.add_widget(output_header)
        
        self.output_text_widget = TextInput(
            hint_text="Encrypted/Decrypted result will appear here...",
            multiline=True,
            readonly=True,
            background_color=self.input_bg,
            foreground_color=self.theme_fg,
            padding=[15, 15, 15, 15],
            font_size='14sp'
        )
        output_card.add_widget(self.output_text_widget)
        main_layout.add_widget(output_card)

        # File Actions
        file_section = BoxLayout(orientation="vertical", size_hint_y=None, height=90, spacing=8)
        file_label = Label(
            text="[b]File Operations[/b]",
            markup=True,
            color=self.theme_fg,
            size_hint_y=None,
            height=25,
            font_size='15sp',
            halign='left'
        )
        file_section.add_widget(file_label)
        
        file_button_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=50, spacing=15)
        file_button_layout.add_widget(Button(
            text="📁 Encrypt File",
            on_press=self.select_file_to_encrypt,
            background_color=self.button_secondary,
            color=self.theme_fg,
            font_size='14sp'
        ))
        file_button_layout.add_widget(Button(
            text="📂 Decrypt File",
            on_press=self.select_file_to_decrypt,
            background_color=self.button_secondary,
            color=self.theme_fg,
            font_size='14sp'
        ))
        file_section.add_widget(file_button_layout)
        main_layout.add_widget(file_section)

        # Status/Debug Panel
        status_section = BoxLayout(orientation="vertical", size_hint_y=0.25, spacing=5)
        status_label = Label(
            text="[b]System Log[/b]",
            markup=True,
            color=self.theme_fg,
            size_hint_y=None,
            height=25,
            font_size='14sp',
            halign='left'
        )
        status_section.add_widget(status_label)
        
        self.status_log_widget = TextInput(
            text="[System Ready] null-Encrypter initialized.\n",
            multiline=True,
            readonly=True,
            background_color=(0.05, 0.05, 0.06, 1),
            foreground_color=(0.2, 1.0, 0.4, 1),  # Bright green
            font_name='RobotoMono-Regular' if os.path.exists('RobotoMono-Regular.ttf') else 'Roboto',
            padding=[10, 10, 10, 10],
            font_size='12sp'
        )
        status_section.add_widget(self.status_log_widget)
        main_layout.add_widget(status_section)
        
        # Footer
        footer_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=45, spacing=10)
        footer_layout.add_widget(Label(
            text="v2.0.0.2 | Secure Encryption",
            size_hint_x=0.7,
            color=(0.5, 0.5, 0.5, 1),
            halign='left',
            font_size='11sp'
        ))
        log_button = Button(
            text="📋 Logs",
            size_hint_x=0.3,
            on_press=self.open_log_folder,
            background_color=(0.25, 0.25, 0.27, 1),
            color=self.accent_color,
            font_size='13sp'
        )
        footer_layout.add_widget(log_button)
        main_layout.add_widget(footer_layout)

        self.log("Encryption key loaded successfully")
        self.log(f"Key storage: {encryption_logic.KEY_FILE}")
        self.log(f"Log file: {self.log_file_path}")
        self.log(f"Encrypted texts folder: {self.null_txt_path}")

        return main_layout

    def log(self, message):
        """Add a message to the status log and save to file."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Update UI
        self.status_log_widget.text += log_entry
        # Auto-scroll to bottom
        self.status_log_widget.cursor = (len(self.status_log_widget.text), 0)
        
        # Write to file
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            # If logging fails, don't crash the app
            print(f"Failed to write to log file: {e}")

    def show_popup(self, title, message):
        """Display a popup window."""
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.9, 0.3))
        popup.open()

    def change_mode(self, instance):
        """Change the current encryption mode."""
        new_mode = instance.text
        self.log(f"Switching mode to: {new_mode}")
        
        # Update buttons
        for mode, btn in self.mode_buttons.items():
            btn.background_color = self.accent_color if mode == new_mode else self.button_secondary
            btn.color = (1, 1, 1, 1) if mode == new_mode else self.accent_color
            btn.bold = (mode == new_mode)
        
        self.current_mode = new_mode
        
        # Show/Hide secondary key input
        if new_mode in ["Caesar", "Vigenere"]:
            self.secondary_key_container.height = 45
            self.secondary_key_container.opacity = 1
            hint = "Enter shift number..." if new_mode == "Caesar" else "Enter keyword..."
            self.secondary_key_input.hint_text = hint
        else:
            self.secondary_key_container.height = 0
            self.secondary_key_container.opacity = 0
            self.secondary_key_input.text = ""

    def encrypt_text(self, _instance):
        """Encrypt the text from the input widget using the selected mode."""
        self.log(f"Encrypt Text ({self.current_mode}) button pressed")
        input_text = self.input_text_widget.text.strip()
        if not input_text:
            self.log("No input text provided")
            self.show_popup("Input Required", "Please enter text to encrypt.")
            return

        try:
            self.log(f"Encrypting text with {self.current_mode}...")
            if self.current_mode == "Null":
                result = encryption_logic.encrypt_text(input_text)
            elif self.current_mode == "Base64":
                result = encryption_logic.base64_encrypt(input_text)
            elif self.current_mode == "Hex":
                result = encryption_logic.hex_encrypt(input_text)
            elif self.current_mode == "Morse":
                result = encryption_logic.morse_encrypt(input_text)
            elif self.current_mode == "Caesar":
                shift_str = self.secondary_key_input.text.strip()
                if not shift_str.isdigit():
                    raise ValueError("Caesar requires a numeric shift key.")
                result = encryption_logic.caesar_encrypt(input_text, int(shift_str))
            elif self.current_mode == "Vigenere":
                v_key = self.secondary_key_input.text.strip()
                if not v_key:
                    raise ValueError("Vigenere requires a keyword.")
                result = encryption_logic.vigenere_encrypt(input_text, v_key)
            
            self.output_text_widget.text = result
            self.log(f"Text encrypted successfully via {self.current_mode}")
        except Exception as e:
            self.log(f"Encryption error: {e}")
            self.show_popup("Encryption Error", str(e))

    def decrypt_text(self, _instance):
        """Decrypt the text from the input widget using the selected mode."""
        self.log(f"Decrypt Text ({self.current_mode}) button pressed")
        input_text = self.input_text_widget.text.strip()
        if not input_text:
            self.log("No input text provided")
            self.show_popup("Input Required", "Please enter text to decrypt.")
            return

        try:
            self.log(f"Decrypting text with {self.current_mode}...")
            if self.current_mode == "Null":
                result = encryption_logic.decrypt_text(input_text)
            elif self.current_mode == "Base64":
                result = encryption_logic.base64_decrypt(input_text)
            elif self.current_mode == "Hex":
                result = encryption_logic.hex_decrypt(input_text)
            elif self.current_mode == "Morse":
                result = encryption_logic.morse_decrypt(input_text)
            elif self.current_mode == "Caesar":
                shift_str = self.secondary_key_input.text.strip()
                if not shift_str.isdigit():
                    raise ValueError("Caesar requires a numeric shift key.")
                result = encryption_logic.caesar_decrypt(input_text, int(shift_str))
            elif self.current_mode == "Vigenere":
                v_key = self.secondary_key_input.text.strip()
                if not v_key:
                    raise ValueError("Vigenere requires a keyword.")
                result = encryption_logic.vigenere_decrypt(input_text, v_key)
            
            self.output_text_widget.text = result
            self.log(f"Text decrypted successfully via {self.current_mode}")
        except Exception as e:
            self.log(f"Decryption error: {e}")
            self.show_popup("Decryption Error", str(e))

    # --- File Encryption Flow ---
    def select_file_to_encrypt(self, _instance):
        """Step 1: Open a file to be encrypted."""
        self.log("Opening file chooser for encryption...")
        filechooser.open_file(on_selection=self._process_file_to_encrypt)

    def _process_file_to_encrypt(self, selection):
        """Step 2: Read the selected file and get encrypted data."""
        if not selection:
            self.log("File selection cancelled")
            return
        
        file_path = selection[0]
        self.log(f"File selected: {os.path.basename(file_path)}")
        try:
            file_size = os.path.getsize(file_path)
            self.log(f"Encrypting file ({file_size} bytes)...")
            encrypted_data = encryption_logic.encrypt_file(file_path)
            self.log("File encrypted, opening save dialog...")
            # Add .enc to the original filename as a suggestion
            suggested_filename = os.path.basename(file_path) + ".enc"
            filechooser.save_file(
                on_selection=lambda p: self._save_file(p, encrypted_data),
                path=suggested_filename
            )
        except (IOError, ValueError) as e:
            self.log(f"File encryption error: {e}")
            self.show_popup("Encryption Error", f"Could not encrypt the file:\n{e}")

    # --- File Decryption Flow ---
    def select_file_to_decrypt(self, _instance):
        """Step 1: Open a file to be decrypted."""
        self.log("Opening file chooser for decryption...")
        filechooser.open_file(on_selection=self._process_file_to_decrypt)

    def _process_file_to_decrypt(self, selection):
        """Step 2: Read the selected file and get decrypted data."""
        if not selection:
            self.log("File selection cancelled")
            return

        file_path = selection[0]
        self.log(f"File selected: {os.path.basename(file_path)}")
        try:
            self.log("Decrypting file...")
            decrypted_data = encryption_logic.decrypt_file(file_path)
            self.log("File decrypted, opening save dialog...")
            # Suggest a decrypted filename, removing .enc if present
            base_filename = os.path.basename(file_path)
            if base_filename.lower().endswith('.enc'):
                suggested_filename = base_filename[:-4]
            else:
                suggested_filename = f"{base_filename}.dec"

            filechooser.save_file(
                on_selection=lambda p: self._save_file(p, decrypted_data),
                path=suggested_filename
            )
        except ValueError as e:
            self.log(f"File decryption error: {e}")
            self.show_popup("Decryption Error", str(e))

    # --- Common File Saving Logic ---
    def _save_file(self, selection, data_to_save):
        """Step 3: Save the processed data (encrypted/decrypted) to the chosen path."""
        if not selection:
            self.log("Save cancelled by user")
            self.show_popup("Save Cancelled", "File saving was cancelled.")
            return

        save_path = selection[0]
        try:
            self.log(f"Saving to: {os.path.basename(save_path)}")
            with open(save_path, "wb") as f:
                f.write(data_to_save)
            self.log(f"File saved successfully ({len(data_to_save)} bytes)")
            self.show_popup("Success", f"File saved successfully at:\n{save_path}")
        except IOError as e:
            self.log(f"Save error: {e}")
            self.show_popup("Save Error", f"Could not save the file:\n{e}")
    
    def paste_input(self, _instance):
        """Paste text from clipboard to input."""
        from kivy.core.clipboard import Clipboard
        clipboard_text = Clipboard.paste()
        if clipboard_text:
            self.input_text_widget.text = clipboard_text
            self.log(f"Pasted {len(clipboard_text)} characters from clipboard")
        else:
            self.log("Clipboard is empty")
    
    def clear_input(self, _instance):
        """Clear input text."""
        self.input_text_widget.text = ""
        self.log("Input cleared")
    
    
    def copy_output(self, _instance):
        """Copy output text to clipboard."""
        from kivy.core.clipboard import Clipboard
        output_text = self.output_text_widget.text
        if output_text:
            Clipboard.copy(output_text)
            self.log(f"Copied {len(output_text)} characters to clipboard")
            self.show_popup("Copied", "Text copied to clipboard!")
        else:
            self.log("No output to copy")
            self.show_popup("Nothing to Copy", "Output is empty.")
    
    def save_output_to_file(self, _instance):
        """Save output text to a file in null-txt folder."""
        output_text = self.output_text_widget.text
        if not output_text:
            self.log("No output to save")
            self.show_popup("Nothing to Save", "Output is empty.")
            return
        
        try:
            import datetime
            # Generate filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"encrypted_text_{timestamp}.txt"
            filepath = self.null_txt_path / filename
            
            # Save to file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(output_text)
            
            self.log(f"Saved {len(output_text)} characters to {filename}")
            self.show_popup("Saved!", f"Text saved to:\n{filepath}")
            
        except Exception as e:
            self.log(f"Error saving file: {e}")
            self.show_popup("Save Error", f"Could not save file:\n{e}")
    
    def clear_output(self, _instance):
        """Clear output text."""
        self.output_text_widget.text = ""
        self.log("Output cleared")
    
    def open_log_folder(self, _instance):
        """Open the folder containing the log file."""
        import subprocess
        import platform
        
        folder_path = str(encryption_logic.APP_DATA_DIR)
        self.log(f"Opening log folder: {folder_path}")
        
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(folder_path)
            elif system == "Darwin":  # macOS
                subprocess.Popen(["open", folder_path])
            elif system == "Linux":
                subprocess.Popen(["xdg-open", folder_path])
            else:  # Android or other
                # On Android, show the path in a popup
                self.log("Android detected, showing path in popup")
                self.show_popup("Log Location", f"Log file location:\n{self.log_file_path}")
        except Exception as e:
            self.log(f"Failed to open folder: {e}")
            self.show_popup("Log Location", f"Log file location:\n{self.log_file_path}")

if __name__ == '__main__':
    NullEncrypterApp().run()
