import customtkinter as ctk


class AegisOverlay:

    def __init__(self, on_command, on_voice_command=None):
        self.on_command = on_command
        self.on_voice_command = on_voice_command

        self.root = ctk.CTk()

        self.root.title("Aegis")

        width = 600
        height = 300

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)

        self.create_ui()

    def create_ui(self):

        title = ctk.CTkLabel(
            self.root,
            text="AEGIS",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=(30, 10))

        subtitle = ctk.CTkLabel(
            self.root,
            text="Your AI operating system assistant"
        )

        subtitle.pack(pady=(0, 20))

        self.input_box = ctk.CTkEntry(
            self.root,
            width=450,
            height=45,
            placeholder_text="Type your command..."
        )

        self.input_box.pack(pady=10)

        button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        button_frame.pack(pady=10)

        send_button = ctk.CTkButton(
            button_frame,
            text="Send",
            command=self.handle_command
        )
        send_button.pack(side="left", padx=5)

        voice_button = ctk.CTkButton(
            button_frame,
            text="🎤 Voice",
            command=self.handle_voice_command
        )
        voice_button.pack(side="left", padx=5)

        self.status_label = ctk.CTkLabel(
            self.root,
            text="",
            text_color="gray"
        )
        self.status_label.pack(pady=5)

        self.input_box.bind(
            "<Return>",
            lambda event: self.handle_command()
        )

    def handle_command(self):

        command = self.input_box.get().strip()

        if not command:
            return

        self.input_box.delete(0, "end")

        # Send command to Aegis core
        self.on_command(command)

    def handle_voice_command(self):
        if self.on_voice_command:
            self.on_voice_command()

    def set_status(self, text: str):
        self.root.after(0, lambda: self.status_label.configure(text=text))

    def toggle(self):

        if self.root.state() == "withdrawn":
            self.show()
        else:
            self.hide()

    def show(self):

        self.root.deiconify()
        self.root.attributes("-topmost", True)
        self.root.lift()

        self.input_box.focus_set()

    def hide(self):

        self.root.withdraw()

    def run(self):

        self.root.mainloop()