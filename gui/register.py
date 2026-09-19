import customtkinter as ctk
from tkinter import messagebox


class RegisterWindow(ctk.CTk):
    """Modern Dark Full-Screen Registration Window."""

    def __init__(self, auth_manager, switch_to_login):
        super().__init__()

        self.auth_manager = auth_manager
        self.switch_to_login = switch_to_login

        self.title("PC Smart - Create Account")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        self.overrideredirect(True)

        self.bind("<Escape>", lambda e: self.destroy())

        self.configure(fg_color="#0f172a")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.card = ctk.CTkFrame(
            self,
            fg_color="#1e293b",
            corner_radius=20,
            border_width=1,
            border_color="#334155",
            width=470,
            height=650
        )

        self.card.grid(row=0, column=0)
        self.card.grid_propagate(False)

        self.logo_label = ctk.CTkLabel(
            self.card,
            text="⚡ PC SMART",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#60a5fa"
        )
        self.logo_label.pack(pady=(35, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.card,
            text="Create your account to get started",
            font=ctk.CTkFont(size=14),
            text_color="#94a3b8"
        )
        self.subtitle_label.pack(pady=(0, 25))

        self.name_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Full Name",
            width=350,
            height=48,
            fg_color="#0f172a",
            text_color="#ffffff",
            placeholder_text_color="#64748b",
            border_color="#475569",
            border_width=1,
            corner_radius=10,
            font=ctk.CTkFont(size=14)
        )
        self.name_entry.pack(pady=10)

        self.email_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Email Address",
            width=350,
            height=48,
            fg_color="#0f172a",
            text_color="#ffffff",
            placeholder_text_color="#64748b",
            border_color="#475569",
            border_width=1,
            corner_radius=10,
            font=ctk.CTkFont(size=14)
        )
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Password",
            show="•",
            width=350,
            height=48,
            fg_color="#0f172a",
            text_color="#ffffff",
            placeholder_text_color="#64748b",
            border_color="#475569",
            border_width=1,
            corner_radius=10,
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.pack(pady=10)

        self.register_btn = ctk.CTkButton(
            self.card,
            text="Create Account",
            command=self.handle_register,
            width=350,
            height=48,
            corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8"
        )
        self.register_btn.pack(pady=(25, 15))

        self.switch_btn = ctk.CTkButton(
            self.card,
            text="Already have an account? Login",
            command=self.switch_to_login,
            fg_color="transparent",
            text_color="#60a5fa",
            hover=False,
            font=ctk.CTkFont(size=13)
        )
        self.switch_btn.pack(pady=5)

    def handle_register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not name or not email or not password:
            messagebox.showerror(
                "Error",
                "Please fill in all fields."
            )
            return

        success, message = self.auth_manager.register_user(
            name,
            email,
            password
        )

        if success:
            messagebox.showinfo(
                "Success",
                message
            )
            self.destroy()
            self.switch_to_login()
        else:
            messagebox.showerror(
                "Registration Failed",
                message
            )