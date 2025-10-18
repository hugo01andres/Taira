#!/usr/bin/env python3
"""
Test script to verify the frontend authentication flow.
Run this after starting the server with: uvicorn app.main:app --reload
"""

import requests
from requests.sessions import Session

BASE_URL = "http://localhost:8000"

def test_frontend_flow():
    print("🧪 Testing Taira Frontend Authentication Flow")
    print("=" * 60)
    
    # Create a session to maintain cookies
    session = Session()
    
    try:
        # Test 1: Access root - should redirect to login
        print("\n1️⃣ Testing root redirect...")
        response = session.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200 and "login" in response.url:
            print("✅ Root correctly redirected to login!")
        else:
            print(f"❌ Root redirect failed: {response.url}")
        
        # Test 2: Access dashboard without auth - should redirect to login
        print("\n2️⃣ Testing dashboard without auth...")
        response = session.get(f"{BASE_URL}/dashboard")
        print(f"Status: {response.status_code}")
        if response.status_code == 200 and "login" in response.url:
            print("✅ Dashboard correctly redirected to login!")
        else:
            print(f"❌ Dashboard redirect failed: {response.url}")
        
        # Test 3: Register a new user
        print("\n3️⃣ Testing user registration...")
        register_data = {
            "email": "frontend@example.com",
            "password": "testpassword123"
        }
        
        response = session.post(f"{BASE_URL}/register", data=register_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200 and "dashboard" in response.url:
            print("✅ User registration successful!")
        else:
            print(f"❌ Registration failed: {response.url}")
            print(f"Response: {response.text[:200]}...")
        
        # Test 4: Access dashboard with auth
        print("\n4️⃣ Testing dashboard with auth...")
        response = session.get(f"{BASE_URL}/dashboard")
        print(f"Status: {response.status_code}")
        if response.status_code == 200 and "Welcome" in response.text:
            print("✅ Dashboard accessible with authentication!")
        else:
            print(f"❌ Dashboard access failed: {response.status_code}")
        
        # Test 5: Logout
        print("\n5️⃣ Testing logout...")
        response = session.get(f"{BASE_URL}/logout")
        print(f"Status: {response.status_code}")
        if response.status_code == 200 and "login" in response.url:
            print("✅ Logout successful!")
        else:
            print(f"❌ Logout failed: {response.url}")
        
        # Test 6: Try to access dashboard after logout
        print("\n6️⃣ Testing dashboard after logout...")
        response = session.get(f"{BASE_URL}/dashboard")
        print(f"Status: {response.status_code}")
        if response.status_code == 200 and "login" in response.url:
            print("✅ Dashboard correctly redirected after logout!")
        else:
            print(f"❌ Dashboard access after logout failed: {response.url}")
        
        print("\n🎉 Frontend authentication flow test completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running with: uvicorn app.main:app --reload")
        return

if __name__ == "__main__":
    test_frontend_flow()
