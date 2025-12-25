<p align="center">
  <img src="https://img.icons8.com/fluency/96/lock-2.png" alt="Password Vault Pro Logo" width="100"/>
</p>

<h1 align="center">🔐 Password Vault Pro</h1>

<p align="center">
  <strong>A modern, feature-rich password manager with beautiful dark UI</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-live-demo">Live Demo</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-screenshots">Screenshots</a> •
  <a href="#-technologies">Technologies</a> •
  <a href="#-architecture">Architecture</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.7+"/>
  <img src="https://img.shields.io/badge/Tkinter-GUI-FF6B6B?style=for-the-badge" alt="Tkinter"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-00D9A5?style=for-the-badge" alt="MIT License"/>
  <img src="https://img.shields.io/badge/Dependencies-Zero-E94560?style=for-the-badge" alt="Zero Dependencies"/>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-blue?style=for-the-badge" alt="Platform"/>
</p>

---

## 🎯 Overview

Password Vault Pro is a **secure, offline password manager** with a stunning dark-themed interface. Built entirely with Python's standard library, it offers enterprise-level features like master password protection, password recovery options, smart service categorization, and password strength analysis—all without any external dependencies.

<p align="center">
  <img src="assets/screenshot.png" alt="Password Vault Pro Screenshot" width="700"/>
</p>

---

## 🚀 Live Demo

Experience Password Vault Pro directly in your browser! No installation required.

<p align="center">
  <a href="https://tharun-ship-it.github.io/password-vault-pro/">
    <img src="https://img.shields.io/badge/▶_TRY_LIVE_DEMO-E94560?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Live Demo" height="50"/>
  </a>
</p>

> **Demo Password:** `demo123`

---

## ✨ Features

### 🎨 Modern Dark UI
- Beautiful gradient dark theme
- Smooth animations and hover effects
- Intuitive tabbed interface
- Responsive design

### 🔒 Security Features
| Feature | Description |
|---------|-------------|
| **Master Password** | SHA-256 hashed protection |
| **Password Strength Meter** | Real-time strength analysis |
| **Password Recovery** | Email & hint-based recovery |
| **Local Storage** | All data stored locally—no cloud |

### 📂 Smart Organization
- **8 Pre-built Categories**: Social Media, Streaming, Email, Development, Cloud Storage, Finance, Shopping, Work
- **50+ Service Suggestions**: Quick-add buttons for popular services
- **Search & Filter**: Instantly find any password
- **Category Browser**: Visual grid of all supported services

### ⚡ Quick Actions
- One-click service addition (Gmail, GitHub, Netflix, etc.)
- Auto-category detection
- Bulk delete with confirmation
- Password visibility toggle

---

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- Tkinter (included with most Python installations)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/tharun-ship-it/password-vault-pro.git
cd password-vault

# Run the application
python src/vault.py
```

### Install as Package

```bash
pip install -e .
password-vault  # Run from anywhere
```

---

## 📸 Screenshots

### Login Screen
Secure master password authentication with password recovery options.

### Add Password Tab
Quick-add buttons, form validation, and real-time password strength indicator.

### My Passwords Tab
Searchable list with category tags, view/delete actions, and bulk operations.

### Categories Browser
Visual grid of 50+ services organized into 8 categories for quick addition.

---

## 🛠 Technologies

This project uses **two implementations** to showcase both desktop and web development skills:

### Desktop Application (Python)
| Technology | Purpose |
|------------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Core application logic |
| ![Tkinter](https://img.shields.io/badge/Tkinter-FF6B6B?style=flat) | GUI framework |
| `hashlib` | SHA-256 password hashing |
| `json` | Data storage |
| `pathlib` | Cross-platform file handling |

### Live Demo (Web)
| Technology | Purpose |
|------------|---------|
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) | Page structure |
| ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) | Styling & animations |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | Interactive functionality |

### Why Two Implementations?

- **Desktop App**: Demonstrates Python skills, OOP, GUI development, security best practices
- **Web Demo**: Allows recruiters to try the app instantly without installation, showcases HTML/CSS/JS skills

---

## 🏗 Architecture

```
password-vault-pro/
├── src/
│   ├── __init__.py           # Package initialization (Python)
│   └── vault.py              # Main desktop app - 700+ lines (Python + Tkinter)
├── tests/
│   └── test_vault.py         # Unit tests (Python)
├── assets/
│   └── screenshot.png        # App screenshot
├── index.html                # Live web demo (HTML + CSS + JavaScript)
├── .github/
│   └── workflows/ci.yml      # CI/CD pipeline (YAML)
├── requirements.txt          # Dependencies (none!)
├── setup.py                  # Package config (Python)
├── pyproject.toml           # Modern Python config
├── LICENSE                   # MIT License
└── README.md                 # Documentation (Markdown)
```

### Data Storage

```
~/.password_vault_pro/
├── config.json    # Master password hash, recovery email, hint
└── vault.json     # Stored credentials (JSON format)
```

### Security Model

| Component | Implementation |
|-----------|----------------|
| Master Password | SHA-256 hash (never stored plain) |
| Recovery Options | Email + Phone Number + Custom Hint |
| Password Display | Masked with 👁 eye toggle to reveal |
| Password Strength | Real-time meter (Weak → Excellent) |
| Storage | Local filesystem only (offline) |

---

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

---

## 🛣 Roadmap

- [x] Master password with recovery
- [x] Password strength indicator
- [x] Category-based organization
- [x] Quick-add service buttons
- [x] Search and filter
- [x] Live web demo
- [ ] Password generator
- [ ] Export/import (CSV, JSON)
- [ ] Browser extension
- [ ] Mobile companion app

---

## 🤝 Contributing

Contributions are welcome! Please read the [Contributing Guide](CONTRIBUTING.md) first.

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/password-vault.git

# Create branch
git checkout -b feature/amazing-feature

# Commit and push
git commit -m 'Add amazing feature'
git push origin feature/amazing-feature

# Open Pull Request
```

---

## 📄 License

This project is licensed under the MIT License—see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Tharun Ponnam**

* GitHub: [@tharun-ship-it](https://github.com/tharun-ship-it)
* Email: tharunponnam007@gmail.com

---

**Created: July 2020**
