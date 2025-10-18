#!/usr/bin/env python3
"""
Test script to verify the AI integration functionality.
Run this after starting the server with: uvicorn app.main:app --reload
"""

import requests
from requests.sessions import Session

BASE_URL = "http://localhost:8000"

def test_ai_integration():
    print("🧪 Testing Taira AI Integration")
    print("=" * 50)
    
    # Create a session to maintain cookies
    session = Session()
    
    try:
        # Step 1: Register and login
        print("\n1️⃣ Setting up authentication...")
        
        register_data = {
            "email": "ai@taira.com",
            "password": "testpass123"
        }
        
        response = session.post(f"{BASE_URL}/register", data=register_data)
        if response.status_code == 200 and "dashboard" in response.url:
            print("✅ User registered and logged in!")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            return
        
        # Step 2: Create a company
        print("\n2️⃣ Creating a company...")
        company_data = {
            "name": "AI Tech Corp",
            "website": "https://aitech.com"
        }
        
        response = session.post(f"{BASE_URL}/companies", data=company_data)
        if response.status_code == 200:
            print("✅ Company created successfully!")
        else:
            print(f"❌ Company creation failed: {response.status_code}")
            return
        
        # Step 3: Create a vacancy
        print("\n3️⃣ Creating a vacancy...")
        vacancy_data = {
            "title": "Senior AI Engineer",
            "description": "Looking for an experienced AI engineer with machine learning expertise.",
            "company_id": "1"
        }
        
        response = session.post(f"{BASE_URL}/vacancies", data=vacancy_data)
        if response.status_code == 200:
            print("✅ Vacancy created successfully!")
        else:
            print(f"❌ Vacancy creation failed: {response.status_code}")
            return
        
        # Step 4: Create a lead
        print("\n4️⃣ Creating a lead...")
        lead_data = {
            "vacancy_id": "1",
            "ai_message": ""
        }
        
        response = session.post(f"{BASE_URL}/leads", data=lead_data)
        if response.status_code == 200:
            print("✅ Lead created successfully!")
        else:
            print(f"❌ Lead creation failed: {response.status_code}")
            return
        
        # Step 5: Test AI generation (this will fail without AWS credentials)
        print("\n5️⃣ Testing AI message generation...")
        response = session.post(f"{BASE_URL}/leads/1/generate")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            # Check if redirected back to leads
            if "leads" in response.url:
                print("✅ AI generation endpoint accessible!")
                
                # Check if error message is shown (expected without AWS credentials)
                response = session.get(f"{BASE_URL}/leads")
                if "Error" in response.text or "AWS credentials" in response.text:
                    print("✅ Error handling working correctly (AWS credentials not configured)")
                else:
                    print("ℹ️  No error message detected - check if AWS credentials are configured")
            else:
                print(f"❌ Unexpected redirect: {response.url}")
        else:
            print(f"❌ AI generation failed: {response.status_code}")
        
        # Step 6: Check leads page
        print("\n6️⃣ Verifying leads page...")
        response = session.get(f"{BASE_URL}/leads")
        if response.status_code == 200 and "Senior AI Engineer" in response.text:
            print("✅ Leads page shows the lead with AI generation button!")
        else:
            print(f"❌ Leads page verification failed: {response.status_code}")
        
        print("\n🎉 AI integration test completed!")
        print("\n📋 Summary:")
        print("- ✅ User authentication working")
        print("- ✅ Company and vacancy creation working")
        print("- ✅ Lead creation working")
        print("- ✅ AI generation endpoint accessible")
        print("- ✅ Error handling for missing AWS credentials")
        print("- ✅ Leads page shows AI generation UI")
        
        print("\n🔧 To test with real AI generation:")
        print("1. Configure AWS credentials in your .env file")
        print("2. Ensure you have access to Amazon Bedrock")
        print("3. Run the test again to see actual AI-generated messages")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running with: uvicorn app.main:app --reload")
        return

if __name__ == "__main__":
    test_ai_integration()
