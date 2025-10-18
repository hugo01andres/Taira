#!/usr/bin/env python3
"""
Test Bedrock model functionality.
This script tests if the Claude 3 Haiku model is working via Bedrock.
"""

import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from app.core.config import settings

def test_bedrock_model():
    """Test Bedrock model with a simple prompt."""
    print("🤖 Testing Bedrock Model")
    print("=" * 40)
    
    # Check configuration
    print(f"1️⃣ Checking Bedrock configuration...")
    print(f"   Model ID: {settings.bedrock_model_id}")
    print(f"   Region: {settings.aws_region}")
    
    try:
        # Create Bedrock runtime client
        print("\n2️⃣ Creating Bedrock runtime client...")
        bedrock_runtime = boto3.client(
            'bedrock-runtime',
            region_name=settings.aws_region,
            **settings.get_aws_credentials()
        )
        print("   ✅ Bedrock runtime client created")
        
        # Prepare test prompt
        test_prompt = "Write a short, professional message offering staffing services to a company hiring a Software Engineer at TechCorp. Keep it to 2-3 sentences."
        
        print(f"\n3️⃣ Sending test prompt to Claude...")
        print(f"   Prompt: {test_prompt}")
        
        # Prepare the request body for Claude 3 Haiku
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [
                {
                    "role": "user",
                    "content": test_prompt
                }
            ]
        }
        
        # Call Bedrock
        print("   📤 Sending request to Bedrock...")
        response = bedrock_runtime.invoke_model(
            modelId=settings.bedrock_model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )
        
        print("   📥 Response received from Bedrock")
        
        # Parse the response
        response_body = json.loads(response["body"].read())
        
        if "content" in response_body and len(response_body["content"]) > 0:
            generated_text = response_body["content"][0]["text"]
            
            print("\n4️⃣ AI Response:")
            print("   " + "="*50)
            print(f"   {generated_text}")
            print("   " + "="*50)
            
            print(f"\n✅ Bedrock model test successful!")
            print(f"   Generated {len(generated_text)} characters")
            print(f"   Model: {settings.bedrock_model_id}")
            
            return True
        else:
            print("   ❌ No content in response")
            return False
            
    except NoCredentialsError:
        print("   ❌ No AWS credentials found")
        print("   Please configure AWS credentials in .env file")
        return False
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', 'Unknown error')
        print(f"   ❌ Bedrock error: {error_code} - {error_message}")
        
        if error_code == 'AccessDeniedException':
            print("   💡 You may need to request access to Bedrock in AWS Console")
        elif error_code == 'ValidationException':
            print("   💡 Check if the model ID is correct and available in your region")
        elif error_code == 'ThrottlingException':
            print("   💡 Rate limit exceeded, try again later")
        
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_ai_service():
    """Test the AI service from the application."""
    print("\n5️⃣ Testing AI service from application...")
    try:
        from app.services.ai import generate_lead_message
        
        # Test the AI service
        print("   📤 Testing generate_lead_message...")
        ai_message = generate_lead_message("Senior Python Developer", "AI Tech Corp")
        
        print("   📥 AI service response:")
        print("   " + "="*50)
        print(f"   {ai_message}")
        print("   " + "="*50)
        
        print("   ✅ AI service test successful!")
        return True
        
    except Exception as e:
        print(f"   ❌ AI service error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Bedrock Model Test")
    print("=" * 50)
    
    # Test Bedrock model directly
    model_ok = test_bedrock_model()
    
    if model_ok:
        # Test AI service
        service_ok = test_ai_service()
        
        if service_ok:
            print("\n🎉 All Bedrock tests passed!")
            print("✅ Bedrock model is working")
            print("✅ AI service is functional")
            print("✅ Ready for production use")
        else:
            print("\n⚠️  Bedrock model works, but AI service failed")
            print("Check AI service configuration")
    else:
        print("\n❌ Bedrock model test failed")
        print("Check AWS credentials and Bedrock permissions")
