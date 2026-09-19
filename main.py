import customtkinter as ctk
from database.database_manager import DatabaseManager
from database.auth_manager import AuthManager
from gui.login import LoginWindow
from gui.register import RegisterWindow
from gui.dashboard import DashboardWindow

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainApplication:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.auth_manager = AuthManager(self.db_manager)
        self.show_login()

    def show_login(self):
        """عرض شاشة تسجيل الدخول"""
        self.login_window = LoginWindow(
            self.auth_manager,
            on_login_success=self.open_dashboard,
            switch_to_register=self.show_register
        )
        self.login_window.mainloop()

    def show_register(self):
        """عرض شاشة إنشاء حساب جديد"""
        try:
            self.login_window.destroy()
        except Exception:
            pass
            
        self.register_window = RegisterWindow(
            self.auth_manager,
            switch_to_login=self.back_to_login
        )
        self.register_window.mainloop()

    def back_to_login(self):
        """العودة لشاشة تسجيل الدخول من التسجيل"""
        try:
            self.register_window.destroy()
        except Exception:
            pass
        self.show_login()

    def open_dashboard(self):
        """فتح لوحة التحكم بعد تسجيل الدخول بنجاح"""
        try:
            self.login_window.destroy()
        except Exception:
            pass
            
        self.dashboard_window = DashboardWindow(
            user=self.auth_manager.current_user,
            auth_manager=self.auth_manager,
            on_logout=self.logout_to_login
        )
        self.dashboard_window.mainloop()

    def logout_to_login(self):
        """تسجيل الخروج والرجوع لشاشة الدخول"""
        try:
            self.dashboard_window.destroy()
        except Exception:
            pass
        self.show_login()


if __name__ == "__main__":
    MainApplication()