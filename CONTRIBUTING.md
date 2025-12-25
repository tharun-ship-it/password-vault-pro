# Contributing to Password Vault

Thank you for your interest in contributing to Password Vault! This document provides guidelines and information about contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or fix

```bash
git clone https://github.com/tharun-ship-it/password-vault.git
cd password-vault
git checkout -b feature/your-feature-name
```

## Development Setup

The project uses only Python's standard library, so no additional dependencies are required for development.

```bash
# Verify Python version
python --version  # Should be 3.7+

# Run the application
python src/vault.py

# Run tests
python -m pytest tests/ -v
```

## Code Style

This project follows PEP 8 guidelines. Please ensure your code:

- Uses 4 spaces for indentation (no tabs)
- Has docstrings for all public modules, functions, classes, and methods
- Includes type hints where applicable
- Keeps line length under 88 characters

### Example

```python
def add_entry(self, account: str, email: str, password: str) -> bool:
    """
    Add a new credential entry to the vault.
    
    Args:
        account: Name of the account or service.
        email: Associated email address.
        password: Password for the account.
        
    Returns:
        True if entry was added successfully, False otherwise.
    """
    ...
```

## Pull Request Process

1. Ensure all tests pass before submitting
2. Update documentation if you're changing functionality
3. Add tests for new features
4. Keep pull requests focused—one feature or fix per PR
5. Write clear commit messages

## Reporting Issues

When reporting bugs, please include:

- Python version (`python --version`)
- Operating system
- Steps to reproduce the issue
- Expected vs actual behavior

## Questions?

Feel free to open an issue for any questions about contributing.
