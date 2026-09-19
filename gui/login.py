import customtkinter as ctk
from tkinter import messagebox


class LoginWindow(ctk.CTk):
    """Modern Dark Full-Screen Login Window."""

    def __init__(self, auth_manager, on_login_success, switch_to_register):
        super().__init__()

        self.auth_manager = auth_manager
        self.on_login_success = on_login_success
        self.switch_to_register = switch_to_register

        self.title("PC Smart - Authentication")

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
            height=570
        )

        self.card.grid(row=0, column=0)
        self.card.grid_propagate(False)

        self.logo_label = ctk.CTkLabel(
            self.card,
            text="⚡ PC SMART",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#60a5fa"
        )
        self.logo_label.pack(pady=(45, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.card,
            text="Sign in to monitor & protect your system",
            font=ctk.CTkFont(size=14),
            text_color="#94a3b8"
        )
        self.subtitle_label.pack(pady=(0, 35))

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
        self.email_entry.pack(pady=12)

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
        self.password_entry.pack(pady=12)

        self.login_btn = ctk.CTkButton(
            self.card,
            text="Login to Dashboard",
            command=self.handle_login,
            width=350,
            height=48,
            corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8"
        )
        self.login_btn.pack(pady=(28, 15))

        self.switch_btn = ctk.CTkButton(
            self.card,
            text="Don't have an account? Register now",
            command=self.switch_to_register,
            fg_color="transparent",
            text_color="#60a5fa",
            hover=False,
            font=ctk.CTkFont(size=13)
        )
        self.switch_btn.pack(pady=5)

    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showerror(
                "Error",
                "Please fill in all fields."
            )
            return

        success, message = self.auth_manager.login_user(
            email,
            password
        )

        if success:
            messagebox.showinfo(
                "Success",
                message
            )
            self.destroy()
            self.on_login_success()
        else:
            messagebox.showerror(
                "Login Failed",
                message
            )