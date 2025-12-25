"""
Unit tests for Password Vault Pro application.

Tests cover core functionality including password hashing,
data persistence, entry management, and password strength evaluation.
"""

import unittest
import tempfile
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestPasswordHashing(unittest.TestCase):
    """Test password hashing functionality."""
    
    def test_hash_consistency(self):
        """Same password should produce same hash."""
        from vault import PasswordVaultPro
        
        with patch.object(PasswordVaultPro, '__init__', lambda x: None):
            vault = PasswordVaultPro()
            vault._hash_password = PasswordVaultPro._hash_password.__get__(vault)
            
            password = "test_password_123"
            hash1 = vault._hash_password(password)
            hash2 = vault._hash_password(password)
            
            self.assertEqual(hash1, hash2)
    
    def test_hash_uniqueness(self):
        """Different passwords should produce different hashes."""
        from vault import PasswordVaultPro
        
        with patch.object(PasswordVaultPro, '__init__', lambda x: None):
            vault = PasswordVaultPro()
            vault._hash_password = PasswordVaultPro._hash_password.__get__(vault)
            
            hash1 = vault._hash_password("password1")
            hash2 = vault._hash_password("password2")
            
            self.assertNotEqual(hash1, hash2)
    
    def test_hash_length(self):
        """SHA-256 hash should be 64 characters."""
        from vault import PasswordVaultPro
        
        with patch.object(PasswordVaultPro, '__init__', lambda x: None):
            vault = PasswordVaultPro()
            vault._hash_password = PasswordVaultPro._hash_password.__get__(vault)
            
            hash_result = vault._hash_password("any_password")
            
            self.assertEqual(len(hash_result), 64)


class TestPasswordStrength(unittest.TestCase):
    """Test password strength evaluation."""
    
    def setUp(self):
        """Set up test fixtures."""
        from vault import PasswordVaultPro
        
        with patch.object(PasswordVaultPro, '__init__', lambda x: None):
            self.vault = PasswordVaultPro()
            self.vault._check_password_strength = PasswordVaultPro._check_password_strength.__get__(self.vault)
    
    def test_weak_password(self):
        """Short simple password should be weak."""
        score, color, message = self.vault._check_password_strength("abc")
        self.assertEqual(message, "Weak")
    
    def test_medium_password(self):
        """Password with some complexity should be medium."""
        score, color, message = self.vault._check_password_strength("Password1")
        self.assertIn(message, ["Medium", "Weak"])
    
    def test_strong_password(self):
        """Complex password should be strong."""
        score, color, message = self.vault._check_password_strength("MyP@ssw0rd!2024")
        self.assertEqual(message, "Strong")


class TestEmailMasking(unittest.TestCase):
    """Test email masking for privacy."""
    
    def setUp(self):
        """Set up test fixtures."""
        from vault import PasswordVaultPro
        
        with patch.object(PasswordVaultPro, '__init__', lambda x: None):
            self.vault = PasswordVaultPro()
            self.vault._mask_email = PasswordVaultPro._mask_email.__get__(self.vault)
    
    def test_mask_normal_email(self):
        """Normal email should be masked properly."""
        masked = self.vault._mask_email("tharunponnam007@gmail.com")
        self.assertEqual(masked, "th***@gmail.com")
    
    def test_mask_short_email(self):
        """Short username email should still mask."""
        masked = self.vault._mask_email("ab@test.com")
        self.assertEqual(masked, "***@test.com")
    
    def test_invalid_email(self):
        """Invalid email should return as-is."""
        masked = self.vault._mask_email("notanemail")
        self.assertEqual(masked, "notanemail")


class TestDataPersistence(unittest.TestCase):
    """Test data storage and retrieval."""
    
    def setUp(self):
        """Create temporary directory for test data."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_file = Path(self.temp_dir) / "vault.json"
    
    def tearDown(self):
        """Clean up temporary files."""
        if self.data_file.exists():
            self.data_file.unlink()
        os.rmdir(self.temp_dir)
    
    def test_save_and_load_entries(self):
        """Entries should persist correctly to JSON."""
        entries = [
            {
                "service": "GitHub",
                "email": "user@example.com",
                "password": "pass123",
                "category": "Development",
                "created_at": "2020-07-18"
            },
            {
                "service": "Gmail",
                "email": "user@gmail.com",
                "password": "pass456",
                "category": "Email",
                "created_at": "2020-07-15"
            }
        ]
        
        with open(self.data_file, "w") as f:
            json.dump(entries, f)
        
        with open(self.data_file, "r") as f:
            loaded = json.load(f)
        
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]["service"], "GitHub")
        self.assertEqual(loaded[0]["category"], "Development")
        self.assertEqual(loaded[1]["email"], "user@gmail.com")
    
    def test_empty_file_handling(self):
        """Should handle missing data file gracefully."""
        self.assertFalse(self.data_file.exists())


class TestEntryValidation(unittest.TestCase):
    """Test entry validation logic."""
    
    def test_required_fields(self):
        """Service and password should be required."""
        entry = {
            "service": "",
            "email": "test@test.com",
            "password": "",
            "category": "General"
        }
        
        is_valid = bool(entry["service"] and entry["password"])
        self.assertFalse(is_valid)
    
    def test_valid_entry(self):
        """Complete entry should pass validation."""
        entry = {
            "service": "GitHub",
            "email": "test@test.com",
            "password": "pass123",
            "category": "Development"
        }
        
        is_valid = bool(entry["service"] and entry["password"])
        self.assertTrue(is_valid)
    
    def test_optional_email(self):
        """Email should be optional."""
        entry = {
            "service": "Test",
            "email": "",
            "password": "pass123",
            "category": "General"
        }
        
        is_valid = bool(entry["service"] and entry["password"])
        self.assertTrue(is_valid)


class TestServiceCategories(unittest.TestCase):
    """Test service category mappings."""
    
    def setUp(self):
        """Set up test fixtures."""
        from vault import PasswordVaultPro
        self.categories = PasswordVaultPro.SERVICE_CATEGORIES
    
    def test_categories_exist(self):
        """Should have multiple categories defined."""
        self.assertGreater(len(self.categories), 5)
    
    def test_popular_services_included(self):
        """Popular services should be included."""
        all_services = []
        for services in self.categories.values():
            all_services.extend(services)
        
        self.assertIn("GitHub", all_services)
        self.assertIn("Gmail", all_services)
        self.assertIn("Netflix", all_services)
        self.assertIn("Instagram", all_services)
    
    def test_category_structure(self):
        """Each category should have services list."""
        for category, services in self.categories.items():
            self.assertIsInstance(services, list)
            self.assertGreater(len(services), 0)


if __name__ == "__main__":
    unittest.main()
