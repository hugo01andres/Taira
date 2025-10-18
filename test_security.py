#!/usr/bin/env python3
"""
Security Test Script for Taira Application
Tests security configuration and identifies vulnerabilities.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.config import settings

def test_security_configuration():
    """Test security configuration."""
    print("🔒 Security Configuration Test")
    print("=" * 50)
    
    issues = []
    warnings = []
    
    # Test 1: Secret Key Security
    print("1. Testing Secret Key Security...")
    if not settings.secret_key:
        issues.append("❌ SECRET_KEY is not set")
    elif settings.secret_key == "your-secret-key-change-in-production":
        issues.append("❌ SECRET_KEY is using default value")
    elif settings.secret_key == "CHANGE-THIS-TO-A-STRONG-RANDOM-SECRET-KEY":
        issues.append("❌ SECRET_KEY is using placeholder value")
    elif len(settings.secret_key) < 32:
        warnings.append("⚠️  SECRET_KEY is shorter than recommended (32+ chars)")
    else:
        print("   ✅ SECRET_KEY is properly configured")
    
    # Test 2: AWS Credentials
    print("\n2. Testing AWS Credentials...")
    if not settings.aws_access_key_id:
        warnings.append("⚠️  AWS_ACCESS_KEY_ID not set (AI features disabled)")
    if not settings.aws_secret_access_key:
        warnings.append("⚠️  AWS_SECRET_ACCESS_KEY not set (AI features disabled)")
    if settings.aws_access_key_id and settings.aws_secret_access_key:
        print("   ✅ AWS credentials are configured")
    
    # Test 3: Environment File Security
    print("\n3. Testing Environment File Security...")
    env_file = Path(".env")
    if env_file.exists():
        print("   ✅ .env file exists")
        
        # Check for sensitive data in .env
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                if "your-secret-key-change-in-production" in content:
                    issues.append("❌ .env contains default secret key")
                if "CHANGE-THIS-TO-A-STRONG-RANDOM-SECRET-KEY" in content:
                    issues.append("❌ .env contains placeholder secret key")
        except Exception as e:
            warnings.append(f"⚠️  Could not read .env file: {e}")
    else:
        warnings.append("⚠️  .env file not found")
    
    # Test 4: Code Security
    print("\n4. Testing Code Security...")
    
    # Check for hardcoded secrets in source code
    security_files = [
        "app/core/security.py",
        "app/core/config.py",
        "app/main.py"
    ]
    
    for file_path in security_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    if "your-secret-key-change-in-production" in content:
                        issues.append(f"❌ Hardcoded secret key found in {file_path}")
                    if "AWS_ACCESS_KEY_ID" in content and "=" in content:
                        # Check if it's a hardcoded value
                        lines = content.split('\n')
                        for line in lines:
                            if "AWS_ACCESS_KEY_ID" in line and "=" in line and not "os.getenv" in line:
                                issues.append(f"❌ Potential hardcoded AWS key in {file_path}")
            except Exception as e:
                warnings.append(f"⚠️  Could not check {file_path}: {e}")
    
    # Test 5: Database Security
    print("\n5. Testing Database Security...")
    db_path = settings.database_url.replace("sqlite:///", "")
    if os.path.exists(db_path):
        # Check file permissions
        import stat
        file_stat = os.stat(db_path)
        permissions = stat.filemode(file_stat.st_mode)
        print(f"   Database permissions: {permissions}")
        
        if file_stat.st_mode & 0o077:  # Check if others can read/write
            warnings.append("⚠️  Database file has overly permissive permissions")
        else:
            print("   ✅ Database permissions look secure")
    else:
        warnings.append("⚠️  Database file not found")
    
    # Results
    print("\n" + "=" * 50)
    print("🔍 SECURITY TEST RESULTS")
    print("=" * 50)
    
    if issues:
        print("🚨 CRITICAL ISSUES FOUND:")
        for issue in issues:
            print(f"   {issue}")
        print()
    
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   {warning}")
        print()
    
    if not issues and not warnings:
        print("✅ All security tests passed!")
        print("Your application appears to be securely configured.")
    elif not issues:
        print("✅ No critical security issues found.")
        print("Review warnings above for potential improvements.")
    else:
        print("❌ Critical security issues found!")
        print("Please address the issues above before deploying.")
    
    print("\n📋 RECOMMENDATIONS:")
    print("1. Generate a strong SECRET_KEY:")
    print("   python -c \"import secrets; print(secrets.token_urlsafe(32))\"")
    print("2. Configure AWS credentials in .env file")
    print("3. Review SECURITY.md for best practices")
    print("4. Test your configuration regularly")
    
    return len(issues) == 0

if __name__ == "__main__":
    success = test_security_configuration()
    sys.exit(0 if success else 1)
