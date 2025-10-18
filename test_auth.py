#!/usr/bin/env python3
"""
Simple test script to verify the authentication flow.
Run this after starting the server with: uvicorn app.main:app --reload
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth_flow():
    print("🧪 Testing Taira Authentication Flow")
    print("=" * 50)
    
    # Test 1: Register a new user
    print("\n1️⃣ Testing user registration...")
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "is_active": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ User registered successfully!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Registration failed: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running with: uvicorn app.main:app --reload")
        return
    
    # Test 2: Login
    print("\n2️⃣ Testing user login...")
    login_data = {
        "username": "test@example.com",  # OAuth2PasswordRequestForm uses 'username' field
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Login successful!")
        login_response = response.json()
        token = login_response["access_token"]
        print(f"Token: {token[:50]}...")
    else:
        print(f"❌ Login failed: {response.text}")
        return
    
    # Test 3: Access protected route
    print("\n3️⃣ Testing protected route...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/protected", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Protected route accessed successfully!")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ Protected route failed: {response.text}")
    
    # Test 4: Test without token (should fail)
    print("\n4️⃣ Testing protected route without token...")
    response = requests.get(f"{BASE_URL}/protected")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ Correctly rejected request without token!")
    else:
        print(f"❌ Should have been rejected: {response.text}")
    
    print("\n🎉 Authentication flow test completed!")

if __name__ == "__main__":
    test_auth_flow()
