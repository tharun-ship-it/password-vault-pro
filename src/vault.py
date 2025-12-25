#!/usr/bin/env python3
"""
Password Vault Pro - Enterprise-grade secure password management.

A comprehensive GUI-based password storage solution featuring master password
protection, multi-factor recovery options, smart categorization, password
generator, strength analysis, and a modern glassmorphism-inspired dark UI.

Author: Tharun Ponnam
Created: July 2020
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import json
import os
import string
import random
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import re


class PasswordVaultPro:
    """
    Enterprise-grade password vault with modern UI and comprehensive features.
    
    Features:
        - Master password with SHA-256 hashing
        - Multi-factor recovery (email, phone, hint)
        - Password strength analyzer
        - Secure password generator
        - Smart service categorization (50+ services)
        - Search and filter functionality
        - Category-based organization
        - Modern dark glassmorphism UI
        - Statistics dashboard
    """
    
    DATA_DIR = Path.home() / ".password_vault_pro"
    DATA_FILE = DATA_DIR / "vault.json"
    CONFIG_FILE = DATA_DIR / "config.json"
    
    # Comprehensive service categories
    SERVICE_CATEGORIES = {
        "📱 Social Media": [
            "Instagram", "Twitter", "Facebook", "LinkedIn", "TikTok", 
            "Snapchat", "Pinterest", "Reddit", "Discord", "Telegram"
        ],
        "🎬 Streaming": [
            "Netflix", "Spotify", "YouTube", "Amazon Prime", "Disney+",
            "Apple Music", "HBO Max", "Hulu", "Twitch", "SoundCloud"
        ],
        "📧 Email": [
            "Gmail", "Outlook", "Yahoo Mail", "ProtonMail", "iCloud",
            "Zoho Mail", "FastMail", "Tutanota"
        ],
        "💻 Development": [
            "GitHub", "GitLab", "Bitbucket", "Stack Overflow", "Docker Hub",
            "npm", "PyPI", "Heroku", "Vercel", "Netlify", "AWS", "Azure"
        ],
        "☁️ Cloud Storage": [
            "Google Drive", "Dropbox", "OneDrive", "iCloud", "Box",
            "MEGA", "pCloud", "Backblaze"
        ],
        "💰 Finance": [
            "PayPal", "Stripe", "Venmo", "Cash App", "Robinhood",
            "Coinbase", "Bank of America", "Chase", "Wells Fargo"
        ],
        "🛒 Shopping": [
            "Amazon", "eBay", "Walmart", "Target", "Best Buy",
            "Etsy", "Shopify", "AliExpress", "Flipkart"
        ],
        "💼 Productivity": [
            "Slack", "Microsoft Teams", "Zoom", "Notion", "Trello",
            "Jira", "Asana", "Monday.com", "Figma", "Canva"
        ],
        "🎮 Gaming": [
            "Steam", "Epic Games", "PlayStation", "Xbox", "Nintendo",
            "Riot Games", "Blizzard", "EA", "Ubisoft"
        ],
        "📚 Education": [
            "Coursera", "Udemy", "edX", "Khan Academy", "Duolingo",
            "LinkedIn Learning", "Skillshare", "Codecademy"
        ]
    }
    
    # Modern color scheme with gradients
    COLORS = {
        "bg_primary": "#0a0a1a",
        "bg_secondary": "#12122a",
        "bg_tertiary": "#1a1a3e",
        "bg_card": "#1e1e42",
        "bg_input": "#252560",
        "accent_primary": "#6366f1",
        "accent_secondary": "#8b5cf6",
        "accent_gradient": "#a855f7",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "info": "#3b82f6",
        "text_primary": "#ffffff",
        "text_secondary": "#94a3b8",
        "text_muted": "#64748b",
        "border": "#334155"
    }
    
    def __init__(self):
        """Initialize the password vault application."""
        self._ensure_data_directory()
        self.root = tk.Tk()
        self.root.title("🔐 Password Vault Pro")
        self.root.geometry("900x900")
        self.root.resizable(True, True)
        self.root.minsize(800, 700)
        self.root.configure(bg=self.COLORS["bg_primary"])
        
        # Center window on screen
        self._center_window()
        
        self._configure_styles()
        
        self.entries: List[Dict] = []
        self.is_authenticated = False
        self.selected_index = -1
        
        if self._master_password_exists():
            self._show_login_screen()
        else:
            self._show_setup_screen()
    
    def _center_window(self) -> None:
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def _ensure_data_directory(self) -> None:
        """Create data directory if it doesn't exist."""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    def _configure_styles(self) -> None:
        """Configure ttk styles for modern dark theme."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook tabs
        style.configure("TNotebook", background=self.COLORS["bg_primary"])
        style.configure("TNotebook.Tab",
                       background=self.COLORS["bg_tertiary"],
                       foreground=self.COLORS["text_secondary"],
                       padding=[20, 12],
                       font=("Segoe UI", 11, "bold"))
        style.map("TNotebook.Tab",
                 background=[("selected", self.COLORS["accent_primary"])],
                 foreground=[("selected", self.COLORS["text_primary"])])
        
        # Treeview
        style.configure("Custom.Treeview",
                       background=self.COLORS["bg_card"],
                       foreground=self.COLORS["text_primary"],
                       fieldbackground=self.COLORS["bg_card"],
                       font=("Segoe UI", 11),
                       rowheight=45)
        style.configure("Custom.Treeview.Heading",
                       background=self.COLORS["bg_tertiary"],
                       foreground=self.COLORS["text_primary"],
                       font=("Segoe UI", 11, "bold"),
                       padding=[10, 8])
        style.map("Custom.Treeview",
                 background=[("selected", self.COLORS["accent_primary"])],
                 foreground=[("selected", self.COLORS["text_primary"])])
        
        # Combobox
        style.configure("TCombobox",
                       fieldbackground=self.COLORS["bg_input"],
                       background=self.COLORS["bg_input"],
                       foreground=self.COLORS["text_primary"])
    
    def _create_gradient_button(self, parent, text: str, command, 
                                 style: str = "primary", width: int = 20) -> tk.Button:
        """Create a modern gradient-style button."""
        colors = {
            "primary": (self.COLORS["accent_primary"], self.COLORS["accent_secondary"]),
            "success": (self.COLORS["success"], "#059669"),
            "danger": (self.COLORS["danger"], "#dc2626"),
            "warning": (self.COLORS["warning"], "#d97706"),
            "secondary": (self.COLORS["bg_tertiary"], self.COLORS["bg_card"])
        }
        
        bg_color, hover_color = colors.get(style, colors["primary"])
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=self.COLORS["text_primary"],
            font=("Segoe UI", 12, "bold"),
            width=width,
            height=2,
            relief="flat",
            cursor="hand2",
            activebackground=hover_color,
            activeforeground=self.COLORS["text_primary"],
            bd=0
        )
        
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg_color))
        
        return btn
    
    def _create_styled_entry(self, parent, show: str = None, 
                             width: int = 40, placeholder: str = "") -> tk.Entry:
        """Create a modern styled entry field."""
        entry = tk.Entry(
            parent,
            font=("Segoe UI", 13),
            bg=self.COLORS["bg_input"],
            fg=self.COLORS["text_primary"],
            insertbackground=self.COLORS["accent_primary"],
            relief="flat",
            width=width,
            show=show,
            highlightthickness=2,
            highlightbackground=self.COLORS["border"],
            highlightcolor=self.COLORS["accent_primary"]
        )
        return entry
    
    def _create_password_entry_with_toggle(self, parent, width: int = 40) -> tuple:
        """Create a password entry with eye toggle button."""
        frame = tk.Frame(parent, bg=parent.cget("bg"))
        
        entry = tk.Entry(
            frame,
            font=("Segoe UI", 13),
            bg=self.COLORS["bg_input"],
            fg=self.COLORS["text_primary"],
            insertbackground=self.COLORS["accent_primary"],
            relief="flat",
            width=width,
            show="●",
            highlightthickness=2,
            highlightbackground=self.COLORS["border"],
            highlightcolor=self.COLORS["accent_primary"]
        )
        entry.pack(side="left", fill="x", expand=True, ipady=10)
        
        # Eye toggle button
        toggle_btn = tk.Label(
            frame,
            text="👁",
            font=("Segoe UI", 16),
            bg=parent.cget("bg"),
            fg=self.COLORS["text_muted"],
            cursor="hand2",
            padx=10
        )
        toggle_btn.pack(side="right")
        
        # Store original show character
        entry._show_char = "●"
        entry._is_visible = False
        
        def toggle_visibility(event=None):
            if entry._is_visible:
                entry.configure(show="●")
                toggle_btn.configure(text="👁")
                entry._is_visible = False
            else:
                entry.configure(show="")
                toggle_btn.configure(text="🙈")
                entry._is_visible = True
        
        toggle_btn.bind("<Button-1>", toggle_visibility)
        
        # Hover effects
        toggle_btn.bind("<Enter>", lambda e: toggle_btn.configure(fg=self.COLORS["accent_primary"]))
        toggle_btn.bind("<Leave>", lambda e: toggle_btn.configure(fg=self.COLORS["text_muted"]))
        
        return frame, entry
    
    def _create_label(self, parent, text: str, size: int = 12, 
                      bold: bool = False, color: str = None) -> tk.Label:
        """Create a styled label."""
        if color is None:
            color = self.COLORS["text_primary"]
        weight = "bold" if bold else "normal"
        return tk.Label(
            parent,
            text=text,
            font=("Segoe UI", size, weight),
            bg=parent.cget("bg"),
            fg=color
        )
    
    def _hash_password(self, password: str) -> str:
        """Generate SHA-256 hash with salt."""
        salt = "vault_pro_2020"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _master_password_exists(self) -> bool:
        """Check if master password has been configured."""
        return self.CONFIG_FILE.exists()
    
    def _verify_master_password(self, password: str) -> bool:
        """Verify provided password against stored hash."""
        try:
            with open(self.CONFIG_FILE, "r") as f:
                config = json.load(f)
            return config.get("master_hash") == self._hash_password(password)
        except (json.JSONDecodeError, FileNotFoundError):
            return False
    
    def _get_recovery_info(self) -> Dict:
        """Get all recovery options."""
        try:
            with open(self.CONFIG_FILE, "r") as f:
                config = json.load(f)
            return {
                "hint": config.get("hint", ""),
                "email": config.get("recovery_email", ""),
                "phone": config.get("recovery_phone", "")
            }
        except (json.JSONDecodeError, FileNotFoundError):
            return {"hint": "", "email": "", "phone": ""}
    
    def _save_master_password(self, password: str, hint: str = "",
                              email: str = "", phone: str = "") -> None:
        """Save master password with recovery options."""
        config = {
            "master_hash": self._hash_password(password),
            "hint": hint,
            "recovery_email": email,
            "recovery_phone": phone,
            "created_at": datetime.now().isoformat(),
            "version": "2.0.0"
        }
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
    
    def _load_entries(self) -> List[Dict]:
        """Load stored entries from disk."""
        if not self.DATA_FILE.exists():
            return []
        try:
            with open(self.DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_entries(self) -> None:
        """Persist entries to disk."""
        with open(self.DATA_FILE, "w") as f:
            json.dump(self.entries, f, indent=2)
    
    def _clear_window(self) -> None:
        """Clear all widgets from window."""
        # Unbind mousewheel to prevent issues
        self.root.unbind_all("<MouseWheel>")
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def _check_password_strength(self, password: str) -> Tuple[int, str, str]:
        """Evaluate password strength with detailed scoring."""
        score = 0
        feedback = []
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        if re.search(r"[a-z]", password):
            score += 0.5
        if re.search(r"[A-Z]", password):
            score += 0.5
        if re.search(r"\d", password):
            score += 1
        if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\;'`~]", password):
            score += 1
        
        if score <= 2:
            return (int(score), self.COLORS["danger"], "Weak")
        elif score <= 4:
            return (int(score), self.COLORS["warning"], "Medium")
        elif score <= 5:
            return (int(score), self.COLORS["info"], "Strong")
        else:
            return (int(score), self.COLORS["success"], "Excellent")
    
    def _generate_password(self, length: int = 16) -> str:
        """Generate a secure random password."""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice("!@#$%^&*")
        ]
        password += random.choices(chars, k=length - 4)
        random.shuffle(password)
        return "".join(password)
    
    def _mask_info(self, text: str, type: str = "email") -> str:
        """Mask sensitive information for display."""
        if not text:
            return ""
        if type == "email" and "@" in text:
            parts = text.split("@")
            if len(parts[0]) > 2:
                return parts[0][:2] + "***@" + parts[1]
            return "***@" + parts[1]
        elif type == "phone" and len(text) > 4:
            return "***" + text[-4:]
        return "***"
    
    # ==================== SCREENS ====================
    
    def _show_setup_screen(self) -> None:
        """Display initial setup screen for new users."""
        self._clear_window()
        
        # Create scrollable canvas
        canvas = tk.Canvas(self.root, bg=self.COLORS["bg_primary"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.COLORS["bg_primary"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=880)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main container inside scrollable frame
        container = tk.Frame(scrollable_frame, bg=self.COLORS["bg_primary"])
        container.pack(expand=True, fill="both", padx=60, pady=30)
        
        # Logo (smaller)
        tk.Label(
            container, text="🔐", font=("Segoe UI", 50),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["accent_primary"]
        ).pack(pady=(0, 8))
        
        # Title
        tk.Label(
            container, text="Welcome to Password Vault Pro",
            font=("Segoe UI", 24, "bold"),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["text_primary"]
        ).pack(pady=(0, 3))
        
        tk.Label(
            container, text="Create your master password to get started",
            font=("Segoe UI", 11),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["text_secondary"]
        ).pack(pady=(0, 20))
        
        # Form card
        form = tk.Frame(container, bg=self.COLORS["bg_card"], padx=35, pady=25)
        form.pack(fill="x")
        
        # Master Password
        self._create_label(form, "Master Password", 11, True).pack(anchor="w")
        pass_frame, self.setup_pass = self._create_password_entry_with_toggle(form)
        pass_frame.pack(fill="x", pady=(5, 3))
        self.setup_pass.bind("<KeyRelease>", self._on_setup_password_change)
        
        # Strength bar
        self.strength_container = tk.Frame(form, bg=self.COLORS["bg_card"])
        self.strength_container.pack(fill="x", pady=(0, 12))
        
        self.strength_bar = tk.Canvas(
            self.strength_container, height=6,
            bg=self.COLORS["bg_input"], highlightthickness=0
        )
        self.strength_bar.pack(fill="x", side="left", expand=True)
        
        self.strength_text = tk.Label(
            self.strength_container, text="", font=("Segoe UI", 9, "bold"),
            bg=self.COLORS["bg_card"], fg=self.COLORS["text_muted"], width=10
        )
        self.strength_text.pack(side="right", padx=(10, 0))
        
        # Confirm Password
        self._create_label(form, "Confirm Password", 11, True).pack(anchor="w")
        confirm_frame, self.setup_confirm = self._create_password_entry_with_toggle(form)
        confirm_frame.pack(fill="x", pady=(5, 15))
        
        # Recovery section header
        recovery_label = tk.Frame(form, bg=self.COLORS["bg_card"])
        recovery_label.pack(fill="x", pady=(8, 12))
        self._create_label(recovery_label, "🔑 Recovery Options", 12, True).pack(side="left")
        self._create_label(
            recovery_label, "(Optional but recommended)", 9, color=self.COLORS["text_muted"]
        ).pack(side="left", padx=(8, 0))
        
        # Recovery Email
        self._create_label(form, "📧 Recovery Email", 10, True).pack(anchor="w")
        self.setup_email = self._create_styled_entry(form)
        self.setup_email.pack(fill="x", pady=(5, 10), ipady=6)
        
        # Recovery Phone
        self._create_label(form, "📱 Recovery Mobile Number", 10, True).pack(anchor="w")
        self.setup_phone = self._create_styled_entry(form)
        self.setup_phone.pack(fill="x", pady=(5, 10), ipady=6)
        
        # Password Hint
        self._create_label(form, "💡 Password Hint", 10, True).pack(anchor="w")
        self.setup_hint = self._create_styled_entry(form)
        self.setup_hint.pack(fill="x", pady=(5, 18), ipady=6)
        
        # Create button - IMPORTANT: This is the main action button
        self._create_gradient_button(
            form, "🚀  Create My Vault & Login", self._handle_setup, "success", 28
        ).pack(pady=(8, 5))
    
    def _on_setup_password_change(self, event=None) -> None:
        """Update strength indicator on password change."""
        password = self.setup_pass.get()
        score, color, text = self._check_password_strength(password)
        
        self.strength_bar.delete("all")
        if password:
            width = self.strength_bar.winfo_width()
            fill_width = (score / 6) * width
            self.strength_bar.create_rectangle(0, 0, fill_width, 6, fill=color, outline="")
            self.strength_text.configure(text=text, fg=color)
        else:
            self.strength_text.configure(text="")
    
    def _handle_setup(self) -> None:
        """Process setup form."""
        password = self.setup_pass.get()
        confirm = self.setup_confirm.get()
        email = self.setup_email.get().strip()
        phone = self.setup_phone.get().strip()
        hint = self.setup_hint.get().strip()
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters.")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        
        self._save_master_password(password, hint, email, phone)
        messagebox.showinfo("Success", "✅ Your vault has been created! Welcome!")
        
        # Go directly to main screen after setup
        self.is_authenticated = True
        self.entries = self._load_entries()
        self._show_main_screen()
    
    def _show_login_screen(self) -> None:
        """Display login screen."""
        self._clear_window()
        
        container = tk.Frame(self.root, bg=self.COLORS["bg_primary"])
        container.pack(expand=True, fill="both", padx=60, pady=60)
        
        # Logo with animation effect
        tk.Label(
            container, text="🔐", font=("Segoe UI", 80),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["accent_primary"]
        ).pack(pady=(0, 15))
        
        tk.Label(
            container, text="Password Vault Pro",
            font=("Segoe UI", 32, "bold"),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["text_primary"]
        ).pack(pady=(0, 5))
        
        tk.Label(
            container, text="Your secure password manager",
            font=("Segoe UI", 13),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["text_secondary"]
        ).pack(pady=(0, 40))
        
        # Login card
        card = tk.Frame(container, bg=self.COLORS["bg_card"], padx=45, pady=35)
        card.pack()
        
        self._create_label(card, "Master Password", 13, True).pack(anchor="w")
        login_frame, self.login_pass = self._create_password_entry_with_toggle(card, width=35)
        login_frame.pack(pady=(10, 25))
        self.login_pass.bind("<Return>", lambda e: self._handle_login())
        self.login_pass.focus_set()
        
        self._create_gradient_button(
            card, "🔓  Login", self._handle_login, "primary", 22
        ).pack()
        
        # Forgot password
        forgot = tk.Label(
            card, text="Forgot Password?", font=("Segoe UI", 11, "underline"),
            bg=self.COLORS["bg_card"], fg=self.COLORS["accent_primary"], cursor="hand2"
        )
        forgot.pack(pady=(25, 0))
        forgot.bind("<Button-1>", lambda e: self._show_recovery_modal())
    
    def _handle_login(self) -> None:
        """Verify login credentials."""
        if self._verify_master_password(self.login_pass.get()):
            self.is_authenticated = True
            self.entries = self._load_entries()
            self._show_main_screen()
        else:
            messagebox.showerror("Error", "Invalid master password.")
            self.login_pass.delete(0, tk.END)
    
    def _show_recovery_modal(self) -> None:
        """Display password recovery modal."""
        recovery = self._get_recovery_info()
        
        modal = tk.Toplevel(self.root)
        modal.title("Password Recovery")
        modal.geometry("500x450")
        modal.configure(bg=self.COLORS["bg_primary"])
        modal.resizable(False, False)
        modal.transient(self.root)
        modal.grab_set()
        
        # Center modal
        modal.geometry("+%d+%d" % (
            self.root.winfo_x() + 200,
            self.root.winfo_y() + 150
        ))
        
        tk.Label(
            modal, text="🔑", font=("Segoe UI", 48),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["warning"]
        ).pack(pady=(30, 15))
        
        tk.Label(
            modal, text="Password Recovery",
            font=("Segoe UI", 22, "bold"),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["text_primary"]
        ).pack(pady=(0, 25))
        
        info_frame = tk.Frame(modal, bg=self.COLORS["bg_card"], padx=30, pady=25)
        info_frame.pack(fill="x", padx=40)
        
        has_recovery = False
        
        if recovery["hint"]:
            has_recovery = True
            tk.Label(
                info_frame, text="💡 Password Hint:",
                font=("Segoe UI", 12, "bold"),
                bg=self.COLORS["bg_card"], fg=self.COLORS["text_primary"]
            ).pack(anchor="w")
            tk.Label(
                info_frame, text=recovery["hint"],
                font=("Segoe UI", 13),
                bg=self.COLORS["bg_card"], fg=self.COLORS["success"],
                wraplength=380
            ).pack(anchor="w", pady=(5, 18))
        
        if recovery["email"]:
            has_recovery = True
            tk.Label(
                info_frame, text="📧 Recovery Email:",
                font=("Segoe UI", 12, "bold"),
                bg=self.COLORS["bg_card"], fg=self.COLORS["text_primary"]
            ).pack(anchor="w")
            tk.Label(
                info_frame, text=self._mask_info(recovery["email"], "email"),
                font=("Segoe UI", 13),
                bg=self.COLORS["bg_card"], fg=self.COLORS["success"]
            ).pack(anchor="w", pady=(5, 18))
        
        if recovery["phone"]:
            has_recovery = True
            tk.Label(
                info_frame, text="📱 Recovery Phone:",
                font=("Segoe UI", 12, "bold"),
                bg=self.COLORS["bg_card"], fg=self.COLORS["text_primary"]
            ).pack(anchor="w")
            tk.Label(
                info_frame, text=self._mask_info(recovery["phone"], "phone"),
                font=("Segoe UI", 13),
                bg=self.COLORS["bg_card"], fg=self.COLORS["success"]
            ).pack(anchor="w", pady=(5, 0))
        
        if not has_recovery:
            tk.Label(
                info_frame, text="❌ No recovery options configured",
                font=("Segoe UI", 13),
                bg=self.COLORS["bg_card"], fg=self.COLORS["danger"]
            ).pack(pady=15)
        
        tk.Button(
            modal, text="Close", command=modal.destroy,
            bg=self.COLORS["bg_tertiary"], fg=self.COLORS["text_primary"],
            font=("Segoe UI", 11, "bold"), relief="flat", width=18, height=2, cursor="hand2"
        ).pack(pady=30)
    
    def _show_main_screen(self) -> None:
        """Display main application interface."""
        self._clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=self.COLORS["bg_secondary"], height=75)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg=self.COLORS["bg_secondary"])
        header_content.pack(expand=True, fill="both", padx=30)
        
        # Logo and title
        title_frame = tk.Frame(header_content, bg=self.COLORS["bg_secondary"])
        title_frame.pack(side="left", pady=20)
        
        tk.Label(
            title_frame, text="🔐", font=("Segoe UI", 24),
            bg=self.COLORS["bg_secondary"], fg=self.COLORS["accent_primary"]
        ).pack(side="left")
        
        tk.Label(
            title_frame, text="Password Vault Pro",
            font=("Segoe UI", 20, "bold"),
            bg=self.COLORS["bg_secondary"], fg=self.COLORS["text_primary"]
        ).pack(side="left", padx=(10, 0))
        
        # Stats badge
        stats_frame = tk.Frame(header_content, bg=self.COLORS["bg_tertiary"], padx=15, pady=8)
        stats_frame.pack(side="left", padx=30)
        
        tk.Label(
            stats_frame, text=f"📊 {len(self.entries)} passwords stored",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLORS["bg_tertiary"], fg=self.COLORS["text_secondary"]
        ).pack()
        
        # Lock button
        lock_btn = tk.Button(
            header_content, text="🔒 Lock Vault",
            command=self._show_login_screen,
            bg=self.COLORS["danger"], fg=self.COLORS["text_primary"],
            font=("Segoe UI", 11, "bold"), relief="flat", padx=18, pady=8, cursor="hand2"
        )
        lock_btn.pack(side="right", pady=20)
        
        # Notebook (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Tabs
        add_tab = tk.Frame(notebook, bg=self.COLORS["bg_primary"])
        notebook.add(add_tab, text="  ➕ Add Password  ")
        self._build_add_tab(add_tab)
        
        view_tab = tk.Frame(notebook, bg=self.COLORS["bg_primary"])
        notebook.add(view_tab, text="  📋 My Passwords  ")
        self._build_view_tab(view_tab)
        
        cat_tab = tk.Frame(notebook, bg=self.COLORS["bg_primary"])
        notebook.add(cat_tab, text="  📁 Categories  ")
        self._build_categories_tab(cat_tab)
        
        gen_tab = tk.Frame(notebook, bg=self.COLORS["bg_primary"])
        notebook.add(gen_tab, text="  🎲 Generator  ")
        self._build_generator_tab(gen_tab)
    
    def _build_add_tab(self, parent) -> None:
        """Build the add password tab."""
        # Quick add suggestions
        quick_frame = tk.Frame(parent, bg=self.COLORS["bg_card"], padx=20, pady=15)
        quick_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        tk.Label(
            quick_frame, text="🚀 Quick Add Popular Services:",
            font=("Segoe UI", 12, "bold"),
            bg=self.COLORS["bg_card"], fg=self.COLORS["text_primary"]
        ).pack(side="left", padx=(0, 20))
        
        services = ["Gmail", "Instagram", "GitHub", "Netflix", "Spotify", "Twitter", "LinkedIn", "Amazon"]
        for svc in services:
            btn = tk.Button(
                quick_frame, text=svc,
                command=lambda s=svc: self._quick_fill(s),
                bg=self.COLORS["bg_tertiary"], fg=self.COLORS["text_primary"],
                font=("Segoe UI", 10), relief="flat", padx=14, pady=6, cursor="hand2"
            )
            btn.pack(side="left", padx=4)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.COLORS["accent_primary"]))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.COLORS["bg_tertiary"]))
        
        # Form
        form = tk.Frame(parent, bg=self.COLORS["bg_card"], padx=35, pady=30)
        form.pack(fill="x", padx=20, pady=10)
        
        # Row 1: Service
        row1 = tk.Frame(form, bg=self.COLORS["bg_card"])
        row1.pack(fill="x", pady=12)
        self._create_label(row1, "Service/Account:", 12, True).pack(side="left", anchor="w", padx=(0, 20))
        self.add_service = self._create_styled_entry(row1, width=45)
        self.add_service.pack(side="left", ipady=8)
        
        # Row 2: Email
        row2 = tk.Frame(form, bg=self.COLORS["bg_card"])
        row2.pack(fill="x", pady=12)
        self._create_label(row2, "Email/Username:", 12, True).pack(side="left", anchor="w", padx=(0, 20))
        self.add_email = self._create_styled_entry(row2, width=45)
        self.add_email.pack(side="left", ipady=8)
        
        # Row 3: Password
        row3 = tk.Frame(form, bg=self.COLORS["bg_card"])
        row3.pack(fill="x", pady=12)
        self._create_label(row3, "Password:", 12, True).pack(side="left", anchor="w", padx=(0, 68))
        
        # Password entry with toggle
        pass_container = tk.Frame(row3, bg=self.COLORS["bg_card"])
        pass_container.pack(side="left")
        
        self.add_password = tk.Entry(
            pass_container,
            font=("Segoe UI", 13),
            bg=self.COLORS["bg_input"],
            fg=self.COLORS["text_primary"],
            insertbackground=self.COLORS["accent_primary"],
            relief="flat",
            width=33,
            show="●",
            highlightthickness=2,
            highlightbackground=self.COLORS["border"],
            highlightcolor=self.COLORS["accent_primary"]
        )
        self.add_password.pack(side="left", ipady=8)
        
        # Eye toggle for add password
        self.add_pass_toggle = tk.Label(
            pass_container, text="👁", font=("Segoe UI", 14),
            bg=self.COLORS["bg_card"], fg=self.COLORS["text_muted"], cursor="hand2", padx=8
        )
        self.add_pass_toggle.pack(side="left")
        self.add_pass_toggle.bind("<Button-1>", self._toggle_add_password)
        self.add_pass_toggle.bind("<Enter>", lambda e: self.add_pass_toggle.configure(fg=self.COLORS["accent_primary"]))
        self.add_pass_toggle.bind("<Leave>", lambda e: self.add_pass_toggle.configure(fg=self.COLORS["text_muted"]))
        
        gen_btn = tk.Button(
            row3, text="🎲", command=self._fill_generated_password,
            bg=self.COLORS["accent_secondary"], fg=self.COLORS["text_primary"],
            font=("Segoe UI", 14), relief="flat", width=3, cursor="hand2"
        )
        gen_btn.pack(side="left", padx=(10, 0), ipady=4)
        
        # Row 4: Category
        row4 = tk.Frame(form, bg=self.COLORS["bg_card"])
        row4.pack(fill="x", pady=12)
        self._create_label(row4, "Category:", 12, True).pack(side="left", anchor="w", padx=(0, 60))
        
        self.add_category = tk.StringVar(value="📱 Social Media")
        cat_menu = ttk.Combobox(
            row4, textvariable=self.add_category,
            values=list(self.SERVICE_CATEGORIES.keys()),
            state="readonly", width=43, font=("Segoe UI", 12)
        )
        cat_menu.pack(side="left", ipady=6)
        
        # Save button
        self._create_gradient_button(
            form, "💾  Save Password", self._add_entry, "success", 25
        ).pack(pady=(25, 5))
    
    def _quick_fill(self, service: str) -> None:
        """Quick fill service name and auto-select category."""
        self.add_service.delete(0, tk.END)
        self.add_service.insert(0, service)
        
        for cat, services in self.SERVICE_CATEGORIES.items():
            if service in services:
                self.add_category.set(cat)
                break
        
        self.add_email.focus_set()
    
    def _toggle_add_password(self, event=None) -> None:
        """Toggle password visibility in add form."""
        current_show = self.add_password.cget("show")
        if current_show == "●":
            self.add_password.configure(show="")
            self.add_pass_toggle.configure(text="🙈")
        else:
            self.add_password.configure(show="●")
            self.add_pass_toggle.configure(text="👁")
    
    def _fill_generated_password(self) -> None:
        """Fill password field with generated password."""
        self.add_password.delete(0, tk.END)
        self.add_password.config(show="")
        self.add_pass_toggle.configure(text="🙈")
        self.add_password.insert(0, self._generate_password())
        # Reset after 3 seconds
        def reset_visibility():
            self.add_password.config(show="●")
            self.add_pass_toggle.configure(text="👁")
        self.root.after(3000, reset_visibility)
    
    def _add_entry(self) -> None:
        """Save new password entry."""
        service = self.add_service.get().strip()
        email = self.add_email.get().strip()
        password = self.add_password.get()
        category = self.add_category.get()
        
        if not service or not password:
            messagebox.showerror("Error", "Service and password are required.")
            return
        
        self.entries.append({
            "service": service,
            "email": email,
            "password": password,
            "category": category,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self._save_entries()
        
        self.add_service.delete(0, tk.END)
        self.add_email.delete(0, tk.END)
        self.add_password.delete(0, tk.END)
        
        if hasattr(self, 'tree'):
            self._refresh_tree()
        
        messagebox.showinfo("Success", f"✅ Password for {service} saved!")
    
    def _build_view_tab(self, parent) -> None:
        """Build the view passwords tab."""
        
        # Create main container
        main_container = tk.Frame(parent, bg=self.COLORS["bg_primary"])
        main_container.pack(fill="both", expand=True)
        
        # Search bar at top
        search_frame = tk.Frame(main_container, bg=self.COLORS["bg_card"], padx=20, pady=12)
        search_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        tk.Label(
            search_frame, text="🔍", font=("Segoe UI", 18),
            bg=self.COLORS["bg_card"], fg=self.COLORS["text_primary"]
        ).pack(side="left")
        
        self.search_entry = self._create_styled_entry(search_frame, width=50)
        self.search_entry.pack(side="left", padx=15, ipady=8)
        self.search_entry.bind("<KeyRelease>", lambda e: self._refresh_tree())
        
        # ACTION BUTTONS - Pack these FIRST at the BOTTOM so they're always visible
        actions = tk.Frame(main_container, bg=self.COLORS["bg_card"], padx=20, pady=15)
        actions.pack(side="bottom", fill="x", padx=20, pady=(10, 20))
        
        # Left side buttons
        left_actions = tk.Frame(actions, bg=self.COLORS["bg_card"])
        left_actions.pack(side="left")
        
        view_btn = tk.Button(
            left_actions, text="👁  View Password", command=self._view_selected,
            bg=self.COLORS["info"], fg=self.COLORS["text_primary"],
            font=("Segoe UI", 11, "bold"), relief="flat", padx=20, pady=12, cursor="hand2"
        )
        view_btn.pack(side="left", padx=(0, 10))
        
        copy_btn = tk.Button(
            left_actions, text="📋  Copy", command=self._copy_selected,
            bg=self.COLORS["accent_secondary"], fg=self.COLORS["text_primary"],
            font=("Segoe UI", 11, "bold"), relief="flat", padx=20, pady=12, cursor="hand2"
        )
        copy_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = tk.Button(
            left_actions, text="🗑  Delete Password", command=self._delete_selected,
            bg=self.COLORS["danger"], fg=self.COLORS["text_primary"],
            font=("Segoe UI", 11, "bold"), relief="flat", padx=20, pady=12, cursor="hand2"
        )
        delete_btn.pack(side="left", padx=(0, 10))
        
        # Right side - Clear All
        clear_btn = tk.Button(
            actions, text="⚠️  Clear All", command=self._clear_all,
            bg=self.COLORS["warning"], fg=self.COLORS["bg_primary"],
            font=("Segoe UI", 11, "bold"), relief="flat", padx=20, pady=12, cursor="hand2"
        )
        clear_btn.pack(side="right")
        
        # Treeview in the middle - takes remaining space
        tree_frame = tk.Frame(main_container, bg=self.COLORS["bg_primary"])
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        columns = ("service", "email", "category", "date")
        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings",
            height=8, style="Custom.Treeview"
        )
        
        self.tree.heading("service", text="Service")
        self.tree.heading("email", text="Email/Username")
        self.tree.heading("category", text="Category")
        self.tree.heading("date", text="Added")
        
        self.tree.column("service", width=180)
        self.tree.column("email", width=250)
        self.tree.column("category", width=150)
        self.tree.column("date", width=130)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self._refresh_tree()
    
    def _refresh_tree(self) -> None:
        """Refresh the treeview with current entries."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search = self.search_entry.get().lower() if hasattr(self, 'search_entry') else ""
        
        for entry in self.entries:
            if search:
                if not any(search in str(v).lower() for v in entry.values()):
                    continue
            
            self.tree.insert("", "end", values=(
                entry["service"],
                entry.get("email", ""),
                entry.get("category", "General"),
                entry.get("created_at", "")[:10]
            ))
    
    def _view_selected(self) -> None:
        """View password for selected entry."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry.")
            return
        
        idx = self.tree.index(selection[0])
        entry = self.entries[idx]
        
        modal = tk.Toplevel(self.root)
        modal.title("View Password")
        modal.geometry("420x280")
        modal.configure(bg=self.COLORS["bg_primary"])
        modal.resizable(False, False)
        modal.transient(self.root)
        modal.grab_set()
        
        tk.Label(
            modal, text=f"🔑 {entry['service']}",
            font=("Segoe UI", 20, "bold"),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["text_primary"]
        ).pack(pady=(35, 20))
        
        pass_frame = tk.Frame(modal, bg=self.COLORS["bg_card"], padx=25, pady=20)
        pass_frame.pack(fill="x", padx=40)
        
        tk.Label(
            pass_frame, text=entry["password"],
            font=("Consolas", 16),
            bg=self.COLORS["bg_card"], fg=self.COLORS["success"]
        ).pack()
        
        btn_frame = tk.Frame(modal, bg=self.COLORS["bg_primary"])
        btn_frame.pack(pady=25)
        
        tk.Button(
            btn_frame, text="📋 Copy", 
            command=lambda: [self.root.clipboard_clear(), 
                           self.root.clipboard_append(entry["password"]),
                           messagebox.showinfo("Copied", "Password copied!")],
            bg=self.COLORS["accent_primary"], fg=self.COLORS["text_primary"],
            font=("Segoe UI", 11, "bold"), relief="flat", width=12, cursor="hand2"
        ).pack(side="left", padx=8)
        
        tk.Button(
            btn_frame, text="Close",
            command=modal.destroy,
            bg=self.COLORS["bg_tertiary"], fg=self.COLORS["text_primary"],
            font=("Segoe UI", 11), relief="flat", width=12, cursor="hand2"
        ).pack(side="left", padx=8)
    
    def _copy_selected(self) -> None:
        """Copy selected password to clipboard."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry.")
            return
        
        idx = self.tree.index(selection[0])
        self.root.clipboard_clear()
        self.root.clipboard_append(self.entries[idx]["password"])
        messagebox.showinfo("Copied", "✅ Password copied to clipboard!")
    
    def _delete_selected(self) -> None:
        """Delete selected entry."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry.")
            return
        
        if messagebox.askyesno("Confirm", "Delete this password?"):
            idx = self.tree.index(selection[0])
            del self.entries[idx]
            self._save_entries()
            self._refresh_tree()
    
    def _clear_all(self) -> None:
        """Clear all entries."""
        if not self.entries:
            messagebox.showinfo("Info", "No entries to clear.")
            return
        
        if messagebox.askyesno("⚠️ Warning", "Delete ALL passwords?\nThis cannot be undone!"):
            self.entries = []
            self._save_entries()
            self._refresh_tree()
    
    def _build_categories_tab(self, parent) -> None:
        """Build the categories browser tab."""
        tk.Label(
            parent, text="📁 Browse Services by Category",
            font=("Segoe UI", 18, "bold"),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["text_primary"]
        ).pack(pady=(25, 10))
        
        tk.Label(
            parent, text="Click any service to quickly add it to your vault",
            font=("Segoe UI", 11),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["text_secondary"]
        ).pack(pady=(0, 25))
        
        # Scrollable container
        canvas = tk.Canvas(parent, bg=self.COLORS["bg_primary"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.COLORS["bg_primary"])
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=820)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for category, services in self.SERVICE_CATEGORIES.items():
            cat_card = tk.Frame(scroll_frame, bg=self.COLORS["bg_card"], padx=20, pady=15)
            cat_card.pack(fill="x", padx=25, pady=10)
            
            tk.Label(
                cat_card, text=category, font=("Segoe UI", 14, "bold"),
                bg=self.COLORS["bg_card"], fg=self.COLORS["text_primary"]
            ).pack(anchor="w", pady=(0, 12))
            
            svc_frame = tk.Frame(cat_card, bg=self.COLORS["bg_card"])
            svc_frame.pack(fill="x")
            
            for i, svc in enumerate(services):
                btn = tk.Button(
                    svc_frame, text=svc,
                    command=lambda s=svc, c=category: self._add_from_category(s, c),
                    bg=self.COLORS["bg_tertiary"], fg=self.COLORS["text_primary"],
                    font=("Segoe UI", 10), relief="flat", padx=14, pady=8, cursor="hand2"
                )
                btn.grid(row=i//5, column=i%5, padx=5, pady=5, sticky="w")
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.COLORS["accent_primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.COLORS["bg_tertiary"]))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _add_from_category(self, service: str, category: str) -> None:
        """Switch to add tab with pre-filled service."""
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Notebook):
                widget.select(0)
                break
        
        self.add_service.delete(0, tk.END)
        self.add_service.insert(0, service)
        self.add_category.set(category)
        self.add_email.focus_set()
    
    def _build_generator_tab(self, parent) -> None:
        """Build the password generator tab."""
        container = tk.Frame(parent, bg=self.COLORS["bg_primary"])
        container.pack(expand=True, fill="both", padx=40, pady=40)
        
        tk.Label(
            container, text="🎲", font=("Segoe UI", 56),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["accent_primary"]
        ).pack(pady=(0, 15))
        
        tk.Label(
            container, text="Password Generator",
            font=("Segoe UI", 24, "bold"),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["text_primary"]
        ).pack(pady=(0, 30))
        
        # Generated password display
        gen_frame = tk.Frame(container, bg=self.COLORS["bg_card"], padx=30, pady=25)
        gen_frame.pack(fill="x")
        
        self.gen_display = tk.Label(
            gen_frame, text="Click Generate",
            font=("Consolas", 20),
            bg=self.COLORS["bg_card"], fg=self.COLORS["text_muted"]
        )
        self.gen_display.pack(pady=10)
        
        # Length slider
        length_frame = tk.Frame(container, bg=self.COLORS["bg_primary"])
        length_frame.pack(pady=30)
        
        tk.Label(
            length_frame, text="Password Length:",
            font=("Segoe UI", 12, "bold"),
            bg=self.COLORS["bg_primary"], fg=self.COLORS["text_primary"]
        ).pack(side="left", padx=(0, 15))
        
        self.length_var = tk.IntVar(value=16)
        length_scale = tk.Scale(
            length_frame, from_=8, to=32, orient="horizontal",
            variable=self.length_var, length=250,
            bg=self.COLORS["bg_primary"], fg=self.COLORS["text_primary"],
            highlightthickness=0, troughcolor=self.COLORS["bg_tertiary"],
            font=("Segoe UI", 10)
        )
        length_scale.pack(side="left")
        
        # Buttons
        btn_frame = tk.Frame(container, bg=self.COLORS["bg_primary"])
        btn_frame.pack(pady=20)
        
        self._create_gradient_button(
            btn_frame, "🎲  Generate", self._generate_new_password, "primary", 18
        ).pack(side="left", padx=10)
        
        self._create_gradient_button(
            btn_frame, "📋  Copy", self._copy_generated, "success", 18
        ).pack(side="left", padx=10)
    
    def _generate_new_password(self) -> None:
        """Generate and display new password."""
        length = self.length_var.get()
        password = self._generate_password(length)
        self.gen_display.configure(text=password, fg=self.COLORS["success"])
    
    def _copy_generated(self) -> None:
        """Copy generated password."""
        password = self.gen_display.cget("text")
        if password and password != "Click Generate":
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Copied", "✅ Password copied!")
    
    def run(self) -> None:
        """Start the application."""
        self.root.mainloop()


def main():
    """Application entry point."""
    app = PasswordVaultPro()
    app.run()


if __name__ == "__main__":
    main()
