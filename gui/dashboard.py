import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from core.system_monitor import SystemMonitor


class DashboardWindow(ctk.CTk):

    def __init__(self, user, auth_manager, on_logout):
        super().__init__()

        self.user = user
        self.auth_manager = auth_manager
        self.on_logout = on_logout

        self.system_monitor = SystemMonitor()

        self.title("PC Smart - System Dashboard")

        self.geometry("1100x700")
        self.minsize(1050, 700)

        self.configure(fg_color="#0f172a")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.time_steps = list(range(20))
        self.cpu_history = [0] * 20
        self.ram_history = [0] * 20

        self.create_sidebar()
        self.create_main_content()

        self.after(100, self.set_dashboard_fullscreen)
        self.update_live_data()

    def set_dashboard_fullscreen(self):
        try:
            self.attributes("-fullscreen", True)
        except Exception:
            try:
                self.state("zoomed")
            except Exception:
                pass

    def create_sidebar(self):

        self.sidebar_frame = ctk.CTkFrame(
            self,
            fg_color="#1e293b",
            corner_radius=0,
            width=220
        )

        self.sidebar_frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="⚡ PC SMART",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            ),
            text_color="#60a5fa"
        )

        logo_label.pack(
            pady=(35, 8),
            padx=20,
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            self.sidebar_frame,
            text="Smart PC Management",
            font=ctk.CTkFont(size=11),
            text_color="#64748b"
        )

        subtitle.pack(
            padx=20,
            anchor="w"
        )

        user_label = ctk.CTkLabel(
            self.sidebar_frame,
            text=f"Welcome, {self.user.name}",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color="#cbd5e1"
        )

        user_label.pack(
            pady=(30, 30),
            padx=20,
            anchor="w"
        )

        btn_font = ctk.CTkFont(
            size=14,
            weight="bold"
        )

        dashboard_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="📊  Dashboard",
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            anchor="w",
            height=42,
            font=btn_font
        )

        dashboard_btn.pack(
            fill="x",
            padx=15,
            pady=5
        )

        file_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="📁  File Manager",
            fg_color="transparent",
            hover_color="#334155",
            text_color="#cbd5e1",
            anchor="w",
            height=42,
            font=btn_font,
            command=self.open_file_cleaner_window
        )

        file_btn.pack(
            fill="x",
            padx=15,
            pady=5
        )

        ai_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="🤖  AI Assistant",
            fg_color="transparent",
            hover_color="#334155",
            text_color="#cbd5e1",
            anchor="w",
            height=42,
            font=btn_font,
            command=self.open_ai_assistant_window
        )

        ai_btn.pack(
            fill="x",
            padx=15,
            pady=5
        )

        separator = ctk.CTkFrame(
            self.sidebar_frame,
            height=1,
            fg_color="#334155"
        )

        separator.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=(0, 75)
        )

        logout_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="🚪  Logout",
            fg_color="#ef4444",
            hover_color="#dc2626",
            anchor="w",
            height=42,
            font=btn_font,
            command=self.handle_logout
        )

        logout_btn.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=25
        )

    def create_main_content(self):

        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="#0f172a",
            corner_radius=0
        )

        self.content_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        header_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )

        header_frame.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        header_left = ctk.CTkFrame(
            header_frame,
            fg_color="transparent"
        )

        header_left.pack(
            side="left"
        )

        title = ctk.CTkLabel(
            header_left,
            text="System Performance",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            ),
            text_color="#ffffff"
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            header_left,
            text="Monitor your PC in real time",
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        )

        subtitle.pack(
            anchor="w",
            pady=(2, 0)
        )

        self.status_label = ctk.CTkLabel(
            header_frame,
            text="● SYSTEM ONLINE",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color="#34d399"
        )

        self.status_label.pack(
            side="right",
            pady=8
        )

        cards_container = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )

        cards_container.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        cards_container.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        (
            self.cpu_card,
            self.cpu_val_label,
            self.cpu_status_label,
            self.cpu_bar
        ) = self.create_metric_card(
            cards_container,
            0,
            "CPU Usage",
            "Processor load",
            "#3b82f6"
        )

        (
            self.ram_card,
            self.ram_val_label,
            self.ram_status_label,
            self.ram_bar
        ) = self.create_metric_card(
            cards_container,
            1,
            "RAM Memory",
            "Memory consumption",
            "#10b981"
        )

        (
            self.disk_card,
            self.disk_val_label,
            self.disk_status_label,
            self.disk_bar
        ) = self.create_metric_card(
            cards_container,
            2,
            "Disk Space",
            "Storage usage",
            "#f59e0b"
        )

        charts_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="#1e293b",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )

        charts_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=5
        )

        chart_header = ctk.CTkFrame(
            charts_frame,
            fg_color="transparent"
        )

        chart_header.pack(
            fill="x",
            padx=20,
            pady=(12, 0)
        )

        chart_title = ctk.CTkLabel(
            chart_header,
            text="📈 Live Performance",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color="#ffffff"
        )

        chart_title.pack(
            side="left"
        )

        self.update_label = ctk.CTkLabel(
            chart_header,
            text="Updating every second",
            font=ctk.CTkFont(size=10),
            text_color="#64748b"
        )

        self.update_label.pack(
            side="right"
        )

        plt.style.use("dark_background")

        self.fig, (
            self.ax_cpu,
            self.ax_ram
        ) = plt.subplots(
            1,
            2,
            figsize=(10, 3)
        )

        self.fig.patch.set_facecolor("#1e293b")

        for ax in (
            self.ax_cpu,
            self.ax_ram
        ):

            ax.set_facecolor("#0f172a")

            ax.tick_params(
                colors="#94a3b8",
                labelsize=8
            )

            ax.grid(
                True,
                linestyle="--",
                alpha=0.2,
                color="#475569"
            )

            for spine in ax.spines.values():
                spine.set_color("#334155")

        self.ax_cpu.set_title(
            "CPU Live Trend",
            color="#60a5fa",
            fontsize=11,
            fontweight="bold"
        )

        self.ax_ram.set_title(
            "RAM Live Trend",
            color="#34d399",
            fontsize=11,
            fontweight="bold"
        )

        self.ax_cpu.set_ylim(
            0,
            100
        )

        self.ax_ram.set_ylim(
            0,
            100
        )

        self.fig.tight_layout(
            pad=2
        )

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=charts_frame
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=15,
            pady=8
        )

        bottom_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )

        bottom_frame.pack(
            fill="x",
            padx=30,
            pady=(12, 20)
        )

        ai_card = ctk.CTkFrame(
            bottom_frame,
            fg_color="#1e293b",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )

        ai_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 6)
        )

        ai_title = ctk.CTkLabel(
            ai_card,
            text="🤖 PC Smart AI Assistant",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color="#60a5fa"
        )

        ai_title.pack(
            anchor="w",
            padx=18,
            pady=(12, 2)
        )

        self.ai_advice_label = ctk.CTkLabel(
            ai_card,
            text="Analyzing system health parameters...",
            font=ctk.CTkFont(size=12),
            text_color="#cbd5e1",
            justify="left",
            wraplength=450
        )

        self.ai_advice_label.pack(
            anchor="w",
            padx=18,
            pady=(0, 12)
        )

        health_card = ctk.CTkFrame(
            bottom_frame,
            fg_color="#1e293b",
            corner_radius=15,
            border_width=1,
            border_color="#334155"
        )

        health_card.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(6, 0)
        )

        health_title = ctk.CTkLabel(
            health_card,
            text="💚 System Health",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color="#34d399"
        )

        health_title.pack(
            anchor="w",
            padx=18,
            pady=(12, 2)
        )

        self.health_label = ctk.CTkLabel(
            health_card,
            text="Checking...",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color="#cbd5e1"
        )

        self.health_label.pack(
            anchor="w",
            padx=18,
            pady=(0, 12)
        )

    def create_metric_card(
        self,
        parent,
        col,
        title,
        description,
        accent_color
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="#1e293b",
            corner_radius=14,
            border_width=1,
            border_color="#334155",
            height=125
        )

        card.grid(
            row=0,
            column=col,
            sticky="nsew",
            padx=5
        )

        card.pack_propagate(False)

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=15,
            pady=(12, 0)
        )

        title_lbl = ctk.CTkLabel(
            top,
            text=title,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color="#cbd5e1"
        )

        title_lbl.pack(
            side="left"
        )

        status_lbl = ctk.CTkLabel(
            top,
            text="Normal",
            font=ctk.CTkFont(size=10),
            text_color="#34d399"
        )

        status_lbl.pack(
            side="right"
        )

        val_lbl = ctk.CTkLabel(
            card,
            text="0%",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            text_color="#ffffff"
        )

        val_lbl.pack(
            anchor="w",
            padx=15,
            pady=(2, 0)
        )

        desc_lbl = ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=10),
            text_color="#64748b"
        )

        desc_lbl.pack(
            anchor="w",
            padx=15
        )

        bar = ctk.CTkProgressBar(
            card,
            progress_color=accent_color,
            fg_color="#0f172a",
            height=6
        )

        bar.pack(
            fill="x",
            padx=15,
            pady=(8, 10)
        )

        bar.set(0)

        return (
            card,
            val_lbl,
            status_lbl,
            bar
        )

    def update_live_data(self):

        try:

            cpu = self.system_monitor.get_cpu_metrics()
            ram = self.system_monitor.get_ram_metrics()
            disk = self.system_monitor.get_disk_metrics()

            cpu_pct = float(
                cpu["usage_percent"]
            )

            ram_pct = float(
                ram["usage_percent"]
            )

            disk_pct = float(
                disk["usage_percent"]
            )

            self.cpu_val_label.configure(
                text=f"{cpu_pct:.1f}%"
            )

            self.cpu_bar.set(
                min(cpu_pct / 100, 1)
            )

            self.update_status(
                self.cpu_status_label,
                cpu_pct
            )

            self.ram_val_label.configure(
                text=f"{ram_pct:.1f}%"
            )

            self.ram_bar.set(
                min(ram_pct / 100, 1)
            )

            self.update_status(
                self.ram_status_label,
                ram_pct
            )

            self.disk_val_label.configure(
                text=f"{disk_pct:.1f}%"
            )

            self.disk_bar.set(
                min(disk_pct / 100, 1)
            )

            self.update_status(
                self.disk_status_label,
                disk_pct
            )

            self.cpu_history.pop(0)
            self.cpu_history.append(cpu_pct)

            self.ram_history.pop(0)
            self.ram_history.append(ram_pct)

            self.ax_cpu.clear()

            self.ax_cpu.set_facecolor(
                "#0f172a"
            )

            self.ax_cpu.plot(
                self.time_steps,
                self.cpu_history,
                color="#3b82f6",
                linewidth=2,
                marker="o",
                markersize=3
            )

            self.ax_cpu.fill_between(
                self.time_steps,
                self.cpu_history,
                alpha=0.08,
                color="#3b82f6"
            )

            self.ax_cpu.set_ylim(
                0,
                100
            )

            self.ax_cpu.set_title(
                f"CPU Trend • {cpu_pct:.1f}%",
                color="#60a5fa",
                fontsize=10,
                fontweight="bold"
            )

            self.ax_cpu.grid(
                True,
                linestyle="--",
                alpha=0.2,
                color="#475569"
            )

            self.ax_ram.clear()

            self.ax_ram.set_facecolor(
                "#0f172a"
            )

            self.ax_ram.plot(
                self.time_steps,
                self.ram_history,
                color="#10b981",
                linewidth=2,
                marker="o",
                markersize=3
            )

            self.ax_ram.fill_between(
                self.time_steps,
                self.ram_history,
                alpha=0.08,
                color="#10b981"
            )

            self.ax_ram.set_ylim(
                0,
                100
            )

            self.ax_ram.set_title(
                f"RAM Trend • {ram_pct:.1f}%",
                color="#34d399",
                fontsize=10,
                fontweight="bold"
            )

            self.ax_ram.grid(
                True,
                linestyle="--",
                alpha=0.2,
                color="#475569"
            )

            self.fig.tight_layout(
                pad=2
            )

            self.canvas.draw_idle()

            self.update_ai_insight(
                cpu_pct,
                ram_pct,
                disk_pct
            )

            highest = max(
                cpu_pct,
                ram_pct,
                disk_pct
            )

            if highest >= 90:

                self.health_label.configure(
                    text="🔴 Critical Load",
                    text_color="#ef4444"
                )

                self.status_label.configure(
                    text="● HIGH SYSTEM LOAD",
                    text_color="#ef4444"
                )

            elif highest >= 75:

                self.health_label.configure(
                    text="🟡 Moderate Load",
                    text_color="#f59e0b"
                )

                self.status_label.configure(
                    text="● SYSTEM UNDER LOAD",
                    text_color="#f59e0b"
                )

            else:

                self.health_label.configure(
                    text="🟢 Excellent",
                    text_color="#34d399"
                )

                self.status_label.configure(
                    text="● SYSTEM ONLINE",
                    text_color="#34d399"
                )

        except Exception as e:

            print(
                f"Error updating metrics: {e}"
            )

        self.after(
            1000,
            self.update_live_data
        )

    def update_status(
        self,
        label,
        value
    ):

        if value >= 90:

            label.configure(
                text="Critical",
                text_color="#ef4444"
            )

        elif value >= 75:

            label.configure(
                text="High",
                text_color="#f59e0b"
            )

        else:

            label.configure(
                text="Normal",
                text_color="#34d399"
            )

    def update_ai_insight(
        self,
        cpu,
        ram,
        disk
    ):

        if cpu >= 90:

            message = (
                f"⚠️ CPU usage is very high ({cpu:.1f}%). "
                "Heavy processes may be running."
            )

        elif ram >= 90:

            message = (
                f"⚠️ RAM usage is very high ({ram:.1f}%). "
                "Consider closing unused applications."
            )

        elif disk >= 90:

            message = (
                f"⚠️ Disk usage is critically high ({disk:.1f}%). "
                "Storage cleanup is recommended."
            )

        elif cpu >= 75 or ram >= 75:

            message = (
                "🟡 System load is above normal. "
                "PC Smart is monitoring the situation."
            )

        else:

            message = (
                "✅ Your system is running normally. "
                "No major performance issues detected."
            )

        self.ai_advice_label.configure(
            text=message
        )

    def open_file_cleaner_window(self):

        file_win = ctk.CTkToplevel(self)

        file_win.title(
            "PC Smart - Large Files Cleaner"
        )

        file_win.geometry(
            "1100x700"
        )

        file_win.configure(
            fg_color="#0f172a"
        )

        file_win.transient(self)

        def make_fullscreen():
            try:
                file_win.attributes(
                    "-fullscreen",
                    True
                )
            except Exception:
                try:
                    file_win.state("zoomed")
                except Exception:
                    pass

        file_win.after(
            100,
            make_fullscreen
        )

        header_frame = ctk.CTkFrame(
            file_win,
            fg_color="transparent"
        )

        header_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        title = ctk.CTkLabel(
            header_frame,
            text="📁 Large Files Cleaner (> 50 MB)",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color="#ffffff"
        )

        title.pack(
            side="left"
        )

        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back to Dashboard",
            width=180,
            height=40,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=file_win.destroy
        )

        back_btn.pack(
            side="right"
        )

        control_frame = ctk.CTkFrame(
            file_win,
            fg_color="transparent"
        )

        control_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 15)
        )

        status_lbl = ctk.CTkLabel(
            control_frame,
            text="Click Scan Large Files to search your user folders.",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )

        status_lbl.pack(
            side="left"
        )

        scroll_frame = ctk.CTkScrollableFrame(
            file_win,
            fg_color="#1e293b",
            corner_radius=12
        )

        scroll_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        def run_scan():

            for widget in scroll_frame.winfo_children():
                widget.destroy()

            status_lbl.configure(
                text="Scanning... Please wait.",
                text_color="#f59e0b"
            )

            file_win.update_idletasks()

            import os

            found_files = []

            user_profile = os.environ.get(
                "USERPROFILE"
            )

            search_dirs = []

            if user_profile:

                for folder in [
                    "Downloads",
                    "Documents",
                    "Desktop",
                    "Videos"
                ]:

                    folder_path = os.path.join(
                        user_profile,
                        folder
                    )

                    if os.path.exists(folder_path):

                        search_dirs.append(
                            folder_path
                        )

            size_threshold = (
                50 * 1024 * 1024
            )

            try:

                for search_dir in search_dirs:

                    for root, _, files in os.walk(
                        search_dir
                    ):

                        for file_name in files:

                            file_path = os.path.join(
                                root,
                                file_name
                            )

                            try:

                                if (
                                    os.path.exists(file_path)
                                    and not os.path.islink(file_path)
                                ):

                                    file_size = os.path.getsize(
                                        file_path
                                    )

                                    if file_size > size_threshold:

                                        found_files.append(
                                            (
                                                file_path,
                                                file_size
                                            )
                                        )

                            except Exception:
                                continue

            except Exception as e:

                messagebox.showerror(
                    "Scan Error",
                    f"Could not complete the scan.\n\n{e}",
                    parent=file_win
                )

                status_lbl.configure(
                    text="Scan failed.",
                    text_color="#ef4444"
                )

                return

            if not found_files:

                ctk.CTkLabel(
                    scroll_frame,
                    text="No files larger than 50 MB were found.",
                    font=ctk.CTkFont(size=14),
                    text_color="#cbd5e1"
                ).pack(
                    pady=30
                )

                status_lbl.configure(
                    text="Scan complete. No large files found.",
                    text_color="#34d399"
                )

                return

            status_lbl.configure(
                text=f"Found {len(found_files)} large file(s).",
                text_color="#34d399"
            )

            for file_path, file_size in found_files:

                size_mb = (
                    file_size / (1024 * 1024)
                )

                row = ctk.CTkFrame(
                    scroll_frame,
                    fg_color="#0f172a",
                    corner_radius=10
                )

                row.pack(
                    fill="x",
                    padx=10,
                    pady=6
                )

                info = ctk.CTkLabel(
                    row,
                    text=(
                        f"{os.path.basename(file_path)}\n"
                        f"Size: {size_mb:.2f} MB\n"
                        f"Path: {file_path}"
                    ),
                    font=ctk.CTkFont(size=12),
                    text_color="#cbd5e1",
                    justify="left",
                    anchor="w"
                )

                info.pack(
                    side="left",
                    fill="x",
                    expand=True,
                    padx=15,
                    pady=12
                )

                def delete_file(
                    path=file_path,
                    row_frame=row
                ):

                    try:

                        os.remove(path)

                        if os.path.exists(path):

                            messagebox.showerror(
                                "Delete Failed",
                                "The file still exists and could not be deleted.",
                                parent=file_win
                            )

                            return

                        row_frame.destroy()

                        status_lbl.configure(
                            text=(
                                f"Successfully deleted: "
                                f"{os.path.basename(path)}"
                            ),
                            text_color="#34d399"
                        )

                        messagebox.showinfo(
                            "File Deleted Successfully",
                            (
                                "The file was deleted successfully.\n\n"
                                f"{os.path.basename(path)}"
                            ),
                            parent=file_win
                        )

                    except PermissionError:

                        messagebox.showerror(
                            "Delete Failed",
                            (
                                "Permission denied.\n\n"
                                "The file may be currently in use."
                            ),
                            parent=file_win
                        )

                    except Exception as e:

                        messagebox.showerror(
                            "Delete Failed",
                            f"Could not delete the file.\n\n{e}",
                            parent=file_win
                        )

                delete_btn = ctk.CTkButton(
                    row,
                    text="Delete",
                    width=90,
                    height=36,
                    fg_color="#ef4444",
                    hover_color="#dc2626",
                    font=ctk.CTkFont(
                        size=12,
                        weight="bold"
                    ),
                    command=delete_file
                )

                delete_btn.pack(
                    side="right",
                    padx=15
                )

        scan_btn = ctk.CTkButton(
            control_frame,
            text="Scan Large Files",
            width=160,
            height=38,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=run_scan
        )

        scan_btn.pack(
            side="right"
        )

    def open_ai_assistant_window(self):

        ai_win = ctk.CTkToplevel(self)

        ai_win.title(
            "PC Smart - AI Expert Assistant"
        )

        ai_win.geometry(
            "1100x700"
        )

        ai_win.configure(
            fg_color="#0f172a"
        )

        ai_win.transient(self)

        def make_fullscreen():
            try:
                ai_win.attributes(
                    "-fullscreen",
                    True
                )
            except Exception:
                try:
                    ai_win.state("zoomed")
                except Exception:
                    pass

        ai_win.after(
            100,
            make_fullscreen
        )

        header_frame = ctk.CTkFrame(
            ai_win,
            fg_color="transparent"
        )

        header_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        title = ctk.CTkLabel(
            header_frame,
            text="🤖 PC Smart AI Expert",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color="#60a5fa"
        )

        title.pack(
            side="left"
        )

        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back to Dashboard",
            width=180,
            height=40,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=ai_win.destroy
        )

        back_btn.pack(
            side="right"
        )

        chat_box = ctk.CTkTextbox(
            ai_win,
            fg_color="#1e293b",
            text_color="#ffffff",
            corner_radius=12,
            font=ctk.CTkFont(size=13)
        )

        chat_box.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 15)
        )

        chat_box.insert(
            "end",
            (
                "AI Assistant: Hello! Ask me anything about "
                "hardware optimization, RAM usage, CPU usage, "
                "or system health.\n\n"
            )
        )

        chat_box.configure(
            state="disabled"
        )

        input_frame = ctk.CTkFrame(
            ai_win,
            fg_color="transparent"
        )

        input_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        q_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your question here...",
            height=42,
            fg_color="#1e293b",
            text_color="#ffffff",
            border_color="#334155"
        )

        q_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        def send_query():

            question = q_entry.get().strip()

            if not question:
                return

            chat_box.configure(
                state="normal"
            )

            chat_box.insert(
                "end",
                f"You: {question}\n"
            )

            q = question.lower()

            if (
                "slow" in q
                or "lag" in q
            ):

                answer = (
                    "AI: Your PC may be experiencing "
                    "high resource usage. Check CPU and "
                    "RAM usage from the Dashboard."
                )

            elif (
                "ram" in q
                or "memory" in q
            ):

                answer = (
                    "AI: RAM is used by active applications. "
                    "Closing unnecessary applications can "
                    "reduce memory usage."
                )

            elif "cpu" in q:

                answer = (
                    "AI: High CPU usage usually means that "
                    "one or more processes are heavily using "
                    "the processor."
                )

            elif (
                "disk" in q
                or "storage" in q
            ):

                answer = (
                    "AI: You can use File Manager to scan "
                    "for files larger than 50 MB and remove "
                    "unnecessary files."
                )

            else:

                answer = (
                    "AI: I am monitoring your system metrics. "
                    "Check the Dashboard for the current "
                    "CPU, RAM, and Disk status."
                )

            chat_box.insert(
                "end",
                f"{answer}\n\n"
            )

            chat_box.configure(
                state="disabled"
            )

            chat_box.see(
                "end"
            )

            q_entry.delete(
                0,
                "end"
            )

        send_btn = ctk.CTkButton(
            input_frame,
            text="Send",
            width=100,
            height=42,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            font=ctk.CTkFont(
                weight="bold"
            ),
            command=send_query
        )

        send_btn.pack(
            side="right"
        )

        q_entry.bind(
            "<Return>",
            lambda event: send_query()
        )

    def handle_logout(self):

        self.auth_manager.logout_user()

        self.destroy()

        self.on_logout()