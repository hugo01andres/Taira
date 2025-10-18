# Taira

Taira Project - AI-Powered Job Lead Management System with FastAPI, SQLModel, Bootstrap, and Claude AI Integration.

## Technology Stack

- **Backend**: FastAPI
- **Database**: SQLite
- **Templates**: Jinja2 + Bootstrap 5
- **ORM**: SQLModel
- **Configuration**: Pydantic Settings
- **Authentication**: Session-based with JWT support
- **AI Integration**: Claude 3 Haiku via Amazon Bedrock
- **Containers**: Docker + Docker Compose

## Project Structure

```
taira/
├─ app/
│  ├─ main.py                 # Main FastAPI application
│  ├─ core/
│  │  ├─ config.py           # Configuration with Pydantic Settings
│  │  ├─ database.py         # Database configuration
│  │  ├─ security.py         # Password hashing and JWT
│  │  └─ auth.py             # Session authentication
│  ├─ models/
│  │  ├─ user.py             # User model
│  │  ├─ company.py          # Company model
│  │  ├─ vacancy.py          # Vacancy model
│  │  └─ lead.py             # Lead model with AI fields
│  ├─ api/
│  │  └─ routes/
│  │     ├─ auth.py           # Authentication routes
│  │     └─ core.py           # Core business routes
│  ├─ services/
│  │  └─ ai.py               # AI service with Bedrock integration
│  ├─ templates/
│  │  ├─ base.html           # Base template with Bootstrap
│  │  ├─ login.html          # Login page
│  │  ├─ register.html       # Registration page
│  │  ├─ dashboard.html      # Main dashboard
│  │  ├─ companies.html      # Companies management
│  │  ├─ vacancies.html      # Vacancies management
│  │  └─ leads.html           # Leads with AI generation
│  └─ static/                # Static files
├─ .env                      # Environment variables
├─ config.env.example        # Environment variables template
├─ requirements.txt       # Python dependencies
├─ Dockerfile               # Docker image
└─ docker-compose.yml       # Container orchestration
```

## Features

### 🔐 Authentication & Security
- **User Registration & Login**: Secure user management
- **Session Management**: Cookie-based authentication
- **Password Security**: Bcrypt hashing
- **JWT Support**: API authentication with JWT tokens
- **Access Control**: Protected routes and user-specific data

### 🏢 Core Business Logic
- **Company Management**: Create and manage companies
- **Job Vacancies**: Track job openings with company relationships
- **Lead Management**: User-specific job application leads
- **Database Relationships**: Proper foreign key relationships

### 🤖 AI Integration
- **Claude 3 Haiku**: AI-powered message generation via Amazon Bedrock
- **Smart Outreach**: Contextual messages based on company and job role
- **Professional Content**: AI-generated staffing service outreach
- **Error Handling**: Graceful AWS credential and service error handling

### 🎨 Modern UI
- **Bootstrap 5**: Responsive, modern design
- **Card-Based Layout**: Clean, organized interface
- **Interactive Forms**: Modal-based creation forms
- **Real-time Feedback**: Success/error notifications
- **Mobile Responsive**: Works on all devices

## Installation and Usage

### Prerequisites
- Python 3.11+
- AWS Account with Bedrock access (for AI features)
- Git

### Option 1: Local Development

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd taira
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp config.env.example .env
   # Edit .env with your configuration
   ```

4. **Configure AWS credentials** (for AI features):
   ```env
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_REGION=us-east-1
   ```

5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the application**:
   - Dashboard: http://localhost:8000
   - Health check: http://localhost:8000/health

### Option 2: Docker

1. **Build and run with Docker Compose**:
   ```bash
   docker compose up --build
   ```

2. **Access the application**:
   - Dashboard: http://localhost:8000
   - Health check: http://localhost:8000/health

## Environment Configuration

### Required Variables
```env
# Application
APP_NAME=Taira
ENV=dev
DATABASE_URL=sqlite:///./taira.db
SECRET_KEY=your-secret-key-change-in-production

# AWS (for AI features)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_SESSION_TOKEN=optional_session_token

# Bedrock
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
```

## User Workflow

### 1. Authentication
- Register a new account at `/register`
- Login at `/login`
- Access protected dashboard at `/dashboard`

### 2. Company Management
- Navigate to `/companies`
- Add companies with name and website
- View company list with creation dates

### 3. Job Vacancies
- Navigate to `/vacancies`
- Create job postings linked to companies
- Select companies from dynamic dropdown
- View vacancies with company information

### 4. Lead Management
- Navigate to `/leads`
- Create leads linked to specific vacancies
- View personal lead dashboard

### 5. AI-Powered Outreach
- Click "🧠 Generate AI Message" on any lead
- AI generates professional outreach message
- View generated content in dedicated section
- Regenerate new messages as needed

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Current user info

### Core Business
- `GET /companies` - List companies
- `POST /companies` - Create company
- `GET /vacancies` - List vacancies
- `POST /vacancies` - Create vacancy
- `GET /leads` - List user leads
- `POST /leads` - Create lead
- `POST /leads/{lead_id}/generate` - Generate AI message

### System
- `GET /health` - Health check
- `GET /protected` - Protected API endpoint

## AI Integration

### Claude 3 Haiku Integration
- **Model**: `anthropic.claude-3-haiku-20240307-v1:0`
- **Service**: Amazon Bedrock
- **Purpose**: Generate professional outreach messages
- **Context**: Company name and job title
- **Output**: Tailored staffing service messages

### AI Message Generation
1. User clicks "Generate AI Message" on a lead
2. System fetches lead, vacancy, and company data
3. AI service calls Claude via Bedrock
4. Generated message saved to lead record
5. User views professional outreach message

## Testing

### Run Test Suites
```bash
# Test authentication flow
python test_auth.py

# Test frontend functionality
python test_frontend.py

# Test complete workflow
python test_workflow.py

# Test AI integration
python test_ai.py
```

### Manual Testing
1. **Authentication**: Register → Login → Dashboard
2. **Companies**: Create companies → View list
3. **Vacancies**: Create vacancies → Link to companies
4. **Leads**: Create leads → Link to vacancies
5. **AI Generation**: Generate AI messages → View results

## Database Migrations

All database migration scripts are organized in the `app/migrations/` folder:

```bash
# Run all migrations (recommended)
python app/migrations/run_migrations.py

# Check migration status
python app/migrations/check_migration_status.py

# Run individual migrations
python app/migrations/migrate_database.py
python app/migrations/migrate_user_profile.py
python app/migrations/migrate_lead_instructions.py
```

**Migration Files:**
- `migrate_database.py` - Adds AI features to lead table
- `migrate_user_profile.py` - Adds company fields to user table  
- `migrate_lead_instructions.py` - Adds custom instructions to lead table

## Development

### Project Structure
- **Models**: SQLModel-based database models
- **Routes**: FastAPI route handlers
- **Templates**: Jinja2 HTML templates
- **Services**: Business logic (AI, authentication)
- **Core**: Configuration, database, security

### Adding Features
1. Create models in `app/models/`
2. Add routes in `app/api/routes/`
3. Create templates in `app/templates/`
4. Add business logic in `app/services/`
5. Update configuration in `app/core/config.py`

## Deployment

### Production Considerations
- **Database**: Migrate from SQLite to PostgreSQL/MySQL
- **Security**: Use strong secret keys and HTTPS
- **AWS**: Configure proper IAM roles and permissions
- **Monitoring**: Add logging and error tracking
- **Scaling**: Use production ASGI server (Gunicorn)

### Environment Variables
- Set `ENV=production`
- Configure production database URL
- Set secure secret keys
- Configure AWS credentials
- Enable HTTPS

## Troubleshooting

### Common Issues
1. **AWS Credentials**: Ensure proper AWS configuration
2. **Bedrock Access**: Verify Bedrock permissions in AWS
3. **Database**: Check SQLite file permissions
4. **Dependencies**: Ensure all packages are installed
5. **Environment**: Verify .env file configuration

### Debug Mode
```bash
# Enable debug logging
export ENV=dev
uvicorn app.main:app --reload --log-level debug
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Check the troubleshooting section
- Review the test scripts
- Examine the API documentation
- Check AWS Bedrock documentation for AI features