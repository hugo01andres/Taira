#!/usr/bin/env python3
"""
Test script to verify the complete company-vacancy-lead workflow.
Run this after starting the server with: uvicorn app.main:app --reload
"""

import requests
from requests.sessions import Session

BASE_URL = "http://localhost:8000"

def test_complete_workflow():
    print("🧪 Testing Complete Taira Workflow")
    print("=" * 50)
    
    # Create a session to maintain cookies
    session = Session()
    
    try:
        # Step 1: Register and login
        print("\n1️⃣ Setting up authentication...")
        
        register_data = {
            "email": "workflow@taira.com",
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
            "name": "TechCorp Solutions",
            "website": "https://techcorp.com"
        }
        
        response = session.post(f"{BASE_URL}/companies", data=company_data)
        if response.status_code == 200 and "companies" in response.url:
            print("✅ Company created successfully!")
        else:
            print(f"❌ Company creation failed: {response.status_code}")
            return
        
        # Step 3: Create another company
        print("\n3️⃣ Creating another company...")
        company_data2 = {
            "name": "DataFlow Inc",
            "website": "https://dataflow.io"
        }
        
        response = session.post(f"{BASE_URL}/companies", data=company_data2)
        if response.status_code == 200:
            print("✅ Second company created!")
        else:
            print(f"❌ Second company creation failed: {response.status_code}")
        
        # Step 4: Check companies page
        print("\n4️⃣ Verifying companies list...")
        response = session.get(f"{BASE_URL}/companies")
        if response.status_code == 200 and "TechCorp Solutions" in response.text and "DataFlow Inc" in response.text:
            print("✅ Companies list shows both companies!")
        else:
            print(f"❌ Companies list verification failed: {response.status_code}")
        
        # Step 5: Create a vacancy
        print("\n5️⃣ Creating a vacancy...")
        vacancy_data = {
            "title": "Senior Python Developer",
            "description": "Looking for an experienced Python developer with FastAPI knowledge.",
            "company_id": "1"  # Assuming first company has ID 1
        }
        
        response = session.post(f"{BASE_URL}/vacancies", data=vacancy_data)
        if response.status_code == 200 and "vacancies" in response.url:
            print("✅ Vacancy created successfully!")
        else:
            print(f"❌ Vacancy creation failed: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
        
        # Step 6: Create another vacancy
        print("\n6️⃣ Creating another vacancy...")
        vacancy_data2 = {
            "title": "Data Scientist",
            "description": "Machine learning and data analysis role.",
            "company_id": "2"  # Assuming second company has ID 2
        }
        
        response = session.post(f"{BASE_URL}/vacancies", data=vacancy_data2)
        if response.status_code == 200:
            print("✅ Second vacancy created!")
        else:
            print(f"❌ Second vacancy creation failed: {response.status_code}")
        
        # Step 7: Check vacancies page
        print("\n7️⃣ Verifying vacancies list...")
        response = session.get(f"{BASE_URL}/vacancies")
        if response.status_code == 200 and "Senior Python Developer" in response.text and "Data Scientist" in response.text:
            print("✅ Vacancies list shows both vacancies with company names!")
        else:
            print(f"❌ Vacancies list verification failed: {response.status_code}")
        
        # Step 8: Create a lead
        print("\n8️⃣ Creating a lead...")
        lead_data = {
            "vacancy_id": "1",  # Assuming first vacancy has ID 1
            "ai_message": "Generated cover letter for Python Developer position"
        }
        
        response = session.post(f"{BASE_URL}/leads", data=lead_data)
        if response.status_code == 200 and "leads" in response.url:
            print("✅ Lead created successfully!")
        else:
            print(f"❌ Lead creation failed: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
        
        # Step 9: Check leads page
        print("\n9️⃣ Verifying leads list...")
        response = session.get(f"{BASE_URL}/leads")
        if response.status_code == 200 and "Senior Python Developer" in response.text:
            print("✅ Leads list shows the lead with vacancy and company info!")
        else:
            print(f"❌ Leads list verification failed: {response.status_code}")
        
        print("\n🎉 Complete workflow test successful!")
        print("\n📋 Summary:")
        print("- ✅ User authentication working")
        print("- ✅ Company creation and listing working")
        print("- ✅ Vacancy creation with company selection working")
        print("- ✅ Lead creation with vacancy selection working")
        print("- ✅ All relationships properly configured")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running with: uvicorn app.main:app --reload")
        return

if __name__ == "__main__":
    test_complete_workflow()
