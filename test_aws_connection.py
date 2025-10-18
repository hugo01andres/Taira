#!/usr/bin/env python3
"""
Test AWS connection and credentials.
This script tests if AWS credentials are properly configured.
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from app.core.config import settings

def test_aws_connection():
    """Test AWS connection and credentials."""
    print("🔍 Testing AWS Connection")
    print("=" * 40)
    
    # Check if credentials are configured
    print(f"1️⃣ Checking AWS configuration...")
    print(f"   AWS Region: {settings.aws_region}")
    print(f"   Access Key ID: {'✅ Set' if settings.aws_access_key_id else '❌ Not set'}")
    print(f"   Secret Access Key: {'✅ Set' if settings.aws_secret_access_key else '❌ Not set'}")
    print(f"   Session Token: {'✅ Set' if settings.aws_session_token else '❌ Not set'}")
    
    if not settings.is_aws_configured():
        print("\n❌ AWS credentials not properly configured!")
        print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in your .env file")
        return False
    
    print("\n2️⃣ Testing AWS STS (Security Token Service)...")
    try:
        # Test basic AWS connection with STS
        sts_client = boto3.client(
            'sts',
            region_name=settings.aws_region,
            **settings.get_aws_credentials()
        )
        
        # Get caller identity
        response = sts_client.get_caller_identity()
        print(f"   ✅ AWS connection successful!")
        print(f"   User ID: {response.get('UserId', 'Unknown')}")
        print(f"   Account: {response.get('Account', 'Unknown')}")
        print(f"   ARN: {response.get('Arn', 'Unknown')}")
        
        return True
        
    except NoCredentialsError:
        print("   ❌ No AWS credentials found")
        return False
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', 'Unknown error')
        print(f"   ❌ AWS Client Error: {error_code} - {error_message}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_bedrock_access():
    """Test Bedrock service access."""
    print("\n3️⃣ Testing Bedrock service access...")
    try:
        # Test Bedrock service access
        bedrock_client = boto3.client(
            'bedrock',
            region_name=settings.aws_region,
            **settings.get_aws_credentials()
        )
        
        # List foundation models (this tests Bedrock access)
        response = bedrock_client.list_foundation_models()
        models = response.get('modelSummaries', [])
        
        print(f"   ✅ Bedrock access successful!")
        print(f"   Found {len(models)} foundation models")
        
        # Check if Claude 3 Haiku is available
        claude_models = [m for m in models if 'claude' in m.get('modelId', '').lower()]
        if claude_models:
            print(f"   ✅ Claude models available:")
            for model in claude_models[:3]:  # Show first 3
                print(f"      - {model.get('modelId', 'Unknown')}")
        else:
            print(f"   ⚠️  No Claude models found")
        
        return True
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', 'Unknown error')
        print(f"   ❌ Bedrock access error: {error_code} - {error_message}")
        
        if error_code == 'AccessDeniedException':
            print("   💡 You may need to request access to Bedrock in AWS Console")
        elif error_code == 'ValidationException':
            print("   💡 Check if Bedrock is available in your region")
        
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 AWS Connection Test")
    print("=" * 50)
    
    # Test AWS connection
    aws_ok = test_aws_connection()
    
    if aws_ok:
        # Test Bedrock access
        bedrock_ok = test_bedrock_access()
        
        if bedrock_ok:
            print("\n🎉 All AWS tests passed!")
            print("✅ AWS credentials are working")
            print("✅ Bedrock service is accessible")
            print("✅ Ready for AI message generation")
        else:
            print("\n⚠️  AWS connection works, but Bedrock access failed")
            print("Check Bedrock permissions and region availability")
    else:
        print("\n❌ AWS connection failed")
        print("Please configure your AWS credentials in .env file")
