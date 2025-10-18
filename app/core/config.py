import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    # Application Configuration
    app_name: str = os.getenv("APP_NAME", "Taira")
    env: str = os.getenv("ENV", "dev")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./taira.db")
    
    # Security Configuration
    secret_key: str = os.getenv("SECRET_KEY", "")
    
    # AWS Configuration
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    aws_session_token: str = os.getenv("AWS_SESSION_TOKEN", "")
    
    # Bedrock Configuration
    bedrock_model_id: str = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
    
    @classmethod
    def get_aws_credentials(cls):
        """Get AWS credentials for boto3 client."""
        credentials = {}
        if cls.aws_access_key_id:
            credentials["aws_access_key_id"] = cls.aws_access_key_id
        if cls.aws_secret_access_key:
            credentials["aws_secret_access_key"] = cls.aws_secret_access_key
        if cls.aws_session_token:
            credentials["aws_session_token"] = cls.aws_session_token
        return credentials
    
    @classmethod
    def is_aws_configured(cls):
        """Check if AWS credentials are properly configured."""
        return bool(cls.aws_access_key_id and cls.aws_secret_access_key)
    
    @classmethod
    def validate_security_config(cls):
        """Validate security configuration."""
        errors = []
        
        if not cls.secret_key:
            errors.append("SECRET_KEY is required for JWT token security")
        elif cls.secret_key == "your-secret-key-change-in-production":
            errors.append("SECRET_KEY must be changed from default value")
        elif len(cls.secret_key) < 32:
            errors.append("SECRET_KEY should be at least 32 characters long")
        
        return errors


settings = Settings()
