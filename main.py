# soundboard_app.py
import customtkinter as ctk
import pygame
import os
import atexit  # To run cleanup on exit

# Import our sound generation functions and cleanup utilities
from sound_generator import SOUND_EFFECTS_GENERATORS, add_temp_file, cleanup_temp_files

# --- Pygame Mixer Initialization ---
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
except pygame.error as e:
    print(f"Error initializing Pygame mixer: {e}")
    print("Sound playback will not be available. Ensure you have a working audio output.")
    # You might want to disable sound features or exit if critical


class SoundboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python Soundboard GUI")
        self.geometry("550x450")
        ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

        self.sounds = {}
        self.temp_sound_files = []

        self._prepare_sounds()
        self._create_widgets()

        # Register cleanup function to be called on exit
        atexit.register(self.on_close)

    def _prepare_sounds(self):
        print("Generating sound effects (this might take a moment)...")
        for name, generator_func in SOUND_EFFECTS_GENERATORS.items():
            try:
                print(f"  Generating {name}...")
                wav_path = generator_func()
                add_temp_file(wav_path)  # Register for cleanup
                if pygame.mixer.get_init():  # Check if mixer initialized successfully
                    self.sounds[name] = pygame.mixer.Sound(wav_path)
                else:
                    self.sounds[name] = None  # Placeholder if mixer failed
                    print(f"    Warning: Pygame mixer not initialized. Cannot load {name}.")
            except Exception as e:
                print(f"Error generating sound '{name}': {e}")
                self.sounds[name] = None
        print("Sound effects ready!")

    def _create_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        title_label = ctk.CTkLabel(main_frame, text="Soundboard GUI FX!", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)

        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(pady=10, fill="both", expand=True)

        sound_names = list(SOUND_EFFECTS_GENERATORS.keys())

        cols = 3  # Number of columns for buttons
        rows = (len(sound_names) + cols - 1) // cols  # Calculate rows needed

        for i, sound_name in enumerate(sound_names):
            row = i // cols
            col = i % cols

            button = ctk.CTkButton(
                buttons_frame,
                text=sound_name,
                command=lambda s_name=sound_name: self.play_sound(s_name),
                height=50,
                font=ctk.CTkFont(size=14)
            )
            button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            buttons_frame.grid_columnconfigure(col, weight=1)

        for r in range(rows):
            buttons_frame.grid_rowconfigure(r, weight=1)

    def play_sound(self, sound_name):
        if sound_name in self.sounds and self.sounds[sound_name]:
            print(f"Playing: {sound_name}")
            self.sounds[sound_name].play()
        else:
            print(f"Sound '{sound_name}' not loaded or mixer issue.")

    def on_close(self):
        print("Cleaning up temporary sound files...")
        cleanup_temp_files()
        pygame.mixer.quit()  # Properly shut down mixer
        print("Exiting application.")


if __name__ == "__main__":
    app = SoundboardApp()
    app.mainloop()