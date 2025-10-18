#!/usr/bin/env python3
"""
Test script to verify the core functionality (companies, vacancies, leads).
Run this after starting the server with: uvicorn app.main:app --reload
"""

import requests
from requests.sessions import Session

BASE_URL = "http://localhost:8000"

def test_core_functionality():
    print("🧪 Testing Taira Core Functionality")
    print("=" * 50)
    
    # Create a session to maintain cookies
    session = Session()
    
    try:
        # Test 1: Register and login
        print("\n1️⃣ Setting up authentication...")
        
        # Register a test user
        register_data = {
            "email": "test@taira.com",
            "password": "testpass123"
        }
        
        response = session.post(f"{BASE_URL}/register", data=register_data)
        if response.status_code == 200 and "dashboard" in response.url:
            print("✅ User registered and logged in!")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            return
        
        # Test 2: Access companies page
        print("\n2️⃣ Testing companies page...")
        response = session.get(f"{BASE_URL}/companies")
        print(f"Status: {response.status_code}")
        if response.status_code == 200 and "Companies" in response.text:
            print("✅ Companies page accessible!")
        else:
            print(f"❌ Companies page failed: {response.status_code}")
        
        # Test 3: Create a company
        print("\n3️⃣ Testing company creation...")
        company_data = {
            "name": "Test Company Inc",
            "website": "https://testcompany.com"
        }
        
        response = session.post(f"{BASE_URL}/companies", data=company_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200 and "companies" in response.url:
            print("✅ Company created successfully!")
        else:
            print(f"❌ Company creation failed: {response.status_code}")
        
        # Test 4: Access vacancies page
        print("\n4️⃣ Testing vacancies page...")
        response = session.get(f"{BASE_URL}/vacancies")
        print(f"Status: {response.status_code}")
        if response.status_code == 200 and "Vacancies" in response.text:
            print("✅ Vacancies page accessible!")
        else:
            print(f"❌ Vacancies page failed: {response.status_code}")
        
        # Test 5: Access leads page
        print("\n5️⃣ Testing leads page...")
        response = session.get(f"{BASE_URL}/leads")
        print(f"Status: {response.status_code}")
        if response.status_code == 200 and "Leads" in response.text:
            print("✅ Leads page accessible!")
        else:
            print(f"❌ Leads page failed: {response.status_code}")
        
        # Test 6: Test unauthenticated access
        print("\n6️⃣ Testing unauthenticated access...")
        session.cookies.clear()
        response = session.get(f"{BASE_URL}/companies")
        print(f"Status: {response.status_code}")
        if response.status_code == 200 and "login" in response.url:
            print("✅ Unauthenticated access correctly redirected!")
        else:
            print(f"❌ Unauthenticated access not properly handled: {response.status_code}")
        
        print("\n🎉 Core functionality test completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running with: uvicorn app.main:app --reload")
        return

if __name__ == "__main__":
    test_core_functionality()
