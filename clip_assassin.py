"""
Clip Assassin for DaVinci Resolve
GUI Application for cutting video clips based on time ranges
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
import os
from resolve_core import ResolveConnection


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class ClipAssassinGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("⚔️ Clip Assassin - DaVinci Resolve")
        self.root.geometry("550x750")
        self.root.resizable(True, True)
        self.root.minsize(500, 650)

        # Set icon for window and taskbar
        try:
            # Try .ico first (works best on Windows for taskbar)
            icon_path = resource_path('icon.ico')
            self.root.iconbitmap(icon_path)
        except Exception as e:
            try:
                # Fallback to PNG (for macOS/Linux)
                png_path = resource_path('Clip_assassin_icon.png')
                icon_image = tk.PhotoImage(file=png_path)
                self.root.iconphoto(True, icon_image)
            except Exception as ex:
                # Icon not found or error loading
                print(f"Icon loading failed: {e}, {ex}")

        # Dark theme colors
        self.bg_color = "#1a1a1a"
        self.fg_color = "#e0e0e0"
        self.accent_color = "#ff4444"
        self.section_bg = "#2a2a2a"
        self.button_bg = "#cc0000"
        self.button_hover = "#ff0000"
        self.reverse_button_bg = "#8800cc"
        self.reverse_button_hover = "#aa00ff"

        # Configure root background
        self.root.configure(bg=self.bg_color)

        # Resolve connection
        self.resolve_conn = ResolveConnection()
        self.connected = False

        # Build UI
        self.create_widgets()

        # Auto-connect on startup
        self.root.after(500, self.connect_to_resolve)

    def create_widgets(self):
        """Create all GUI widgets"""

        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(pady=20, padx=20, fill=tk.X)

        title_label = tk.Label(
            header_frame,
            text="⚔️ CLIP ASSASSIN",
            font=("Arial", 24, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack()

        tagline_label = tk.Label(
            header_frame,
            text="Cuts. Without mercy.",
            font=("Arial", 10, "italic"),
            fg="#999999",
            bg=self.bg_color
        )
        tagline_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="for DaVinci Resolve",
            font=("Arial", 9),
            fg="#666666",
            bg=self.bg_color
        )
        subtitle_label.pack()

        # Section 1: Connection Status
        section1 = tk.LabelFrame(
            self.root,
            text="1. Resolve Connection",
            font=("Arial", 10, "bold"),
            fg=self.fg_color,
            bg=self.section_bg,
            padx=10,
            pady=10
        )
        section1.pack(pady=5, padx=20, fill=tk.X)

        self.status_label = tk.Label(
            section1,
            text="⏳ Connecting to Resolve...",
            font=("Arial", 9),
            fg="#ffaa00",
            bg=self.section_bg,
            anchor="w"
        )
        self.status_label.pack(fill=tk.X, pady=5)

        connect_btn = tk.Button(
            section1,
            text="🔄 Reconnect",
            command=self.connect_to_resolve,
            bg="#555555",
            fg="white",
            font=("Arial", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        connect_btn.pack(pady=5)

        # Section 2: Time Ranges Input
        section2 = tk.LabelFrame(
            self.root,
            text="2. Mark Your Targets (one per line)",
            font=("Arial", 10, "bold"),
            fg=self.fg_color,
            bg=self.section_bg,
            padx=10,
            pady=10
        )
        section2.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        format_label = tk.Label(
            section2,
            text="Formats: 1m57-2m08 / 1:57-2:08 / 0:02:25-0:02:45 / 00:01:30:15-00:02:00:20 (timecode with frames)",
            font=("Arial", 8),
            fg="#999999",
            bg=self.section_bg,
            anchor="w"
        )
        format_label.pack(fill=tk.X, pady=(0, 5))

        self.timecodes_text = scrolledtext.ScrolledText(
            section2,
            height=10,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            padx=5,
            pady=5
        )
        self.timecodes_text.pack(fill=tk.BOTH, expand=True)

        # Placeholder text
        placeholder = "1m57-2m08\n3m10-3m22\n4m27-4m43\n5m28-5m36"
        self.timecodes_text.insert("1.0", placeholder)
        self.timecodes_text.config(fg="#666666")

        # Bind events for placeholder
        self.timecodes_text.bind("<FocusIn>", self.on_focus_in)
        self.timecodes_text.bind("<FocusOut>", self.on_focus_out)

        # Section 3: Execute
        section3 = tk.LabelFrame(
            self.root,
            text="3. Execute",
            font=("Arial", 10, "bold"),
            fg=self.fg_color,
            bg=self.section_bg,
            padx=10,
            pady=10
        )
        section3.pack(pady=5, padx=20, fill=tk.X)

        self.execute_btn = tk.Button(
            section3,
            text="🗡️ RUN THE BLADES",
            command=self.execute_cutting,
            bg=self.button_bg,
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.execute_btn.pack(fill=tk.X, pady=5)

        self.reverse_btn = tk.Button(
            section3,
            text="⚔️ REVERSE BLADES",
            command=self.execute_reverse_cutting,
            bg=self.reverse_button_bg,
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.reverse_btn.pack(fill=tk.X, pady=5)

        reverse_help = tk.Label(
            section3,
            text="REVERSE mode: Keep everything EXCEPT marked ranges (perfect for removing ads)",
            font=("Arial", 7),
            fg="#999999",
            bg=self.section_bg,
            anchor="w"
        )
        reverse_help.pack(fill=tk.X, pady=(0, 5))

        # Section 4: Mission Status
        section4 = tk.LabelFrame(
            self.root,
            text="Mission Status",
            font=("Arial", 10, "bold"),
            fg=self.fg_color,
            bg=self.section_bg,
            padx=10,
            pady=10
        )
        section4.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        self.result_text = scrolledtext.ScrolledText(
            section4,
            height=8,
            font=("Arial", 9),
            bg="#1e1e1e",
            fg=self.fg_color,
            relief=tk.FLAT,
            padx=5,
            pady=5,
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def on_focus_in(self, event):
        """Remove placeholder on focus"""
        if self.timecodes_text.get("1.0", "end-1c") == "1m57-2m08\n3m10-3m22\n4m27-4m43\n5m28-5m36":
            self.timecodes_text.delete("1.0", tk.END)
            self.timecodes_text.config(fg=self.fg_color)

    def on_focus_out(self, event):
        """Add placeholder if empty"""
        if not self.timecodes_text.get("1.0", "end-1c").strip():
            self.timecodes_text.insert("1.0", "1m57-2m08\n3m10-3m22\n4m27-4m43\n5m28-5m36")
            self.timecodes_text.config(fg="#666666")

    def connect_to_resolve(self):
        """Connect to DaVinci Resolve"""
        self.update_status("⏳ Connecting to Resolve...", "#ffaa00")
        self.execute_btn.config(state=tk.DISABLED)
        self.reverse_btn.config(state=tk.DISABLED)

        def connect_thread():
            success, message = self.resolve_conn.connect()
            self.root.after(0, lambda: self.connection_complete(success, message))

        threading.Thread(target=connect_thread, daemon=True).start()

    def connection_complete(self, success, message):
        """Handle connection result"""
        if success:
            self.connected = True
            self.update_status(f"✓ {message}", "#44ff44")
            self.execute_btn.config(state=tk.NORMAL)
            self.reverse_btn.config(state=tk.NORMAL)
            self.update_result(self.resolve_conn.get_project_info())
        else:
            self.connected = False
            self.update_status(f"✗ {message}", "#ff4444")
            self.execute_btn.config(state=tk.DISABLED)
            self.reverse_btn.config(state=tk.DISABLED)
            self.update_result(f"Connection failed:\n{message}\n\nMake sure DaVinci Resolve is running with a project open.")

    def update_status(self, text, color):
        """Update connection status label"""
        self.status_label.config(text=text, fg=color)

    def update_result(self, text):
        """Update result text area"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", text)
        self.result_text.config(state=tk.DISABLED)

    def execute_cutting(self):
        """Execute the video cutting operation"""
        self._execute_cutting_internal(reverse_mode=False)

    def execute_reverse_cutting(self):
        """Execute the video cutting operation in REVERSE mode"""
        self._execute_cutting_internal(reverse_mode=True)

    def _execute_cutting_internal(self, reverse_mode=False):
        """Internal method to execute cutting with optional reverse mode"""
        if not self.connected:
            messagebox.showerror("Not Connected", "Please connect to DaVinci Resolve first.")
            return

        # Get timecodes
        timecodes = self.timecodes_text.get("1.0", "end-1c").strip()

        # Check for placeholder
        if timecodes == "1m57-2m08\n3m10-3m22\n4m27-4m43\n5m28-5m36":
            messagebox.showwarning("No Targets", "Please enter your time ranges first.")
            return

        if not timecodes:
            messagebox.showwarning("No Targets", "Please enter time ranges to cut.")
            return

        # Disable buttons during operation
        self.execute_btn.config(state=tk.DISABLED, text="⏳ Executing...")
        self.reverse_btn.config(state=tk.DISABLED, text="⏳ Executing...")

        if reverse_mode:
            self.update_result("⚔️ REVERSE mode activated...\n🎯 Marking targets for elimination...\nProcessing...\n")
        else:
            self.update_result("🎯 Locking on targets...\nProcessing...\n")

        def cut_thread():
            success, message = self.resolve_conn.cut_video(timecodes, reverse_mode=reverse_mode)
            self.root.after(0, lambda: self.cutting_complete(success, message))

        threading.Thread(target=cut_thread, daemon=True).start()

    def cutting_complete(self, success, message):
        """Handle cutting operation result"""
        self.execute_btn.config(state=tk.NORMAL, text="🗡️ RUN THE BLADES")
        self.reverse_btn.config(state=tk.NORMAL, text="⚔️ REVERSE BLADES")

        if success:
            self.update_result(message)
            messagebox.showinfo("Mission Accomplished", "Timeline created successfully!\nCheck your Resolve project.")
        else:
            self.update_result(f"✗ Mission Failed\n\n{message}")
            messagebox.showerror("Mission Failed", message)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ClipAssassinGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
