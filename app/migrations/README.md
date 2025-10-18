# Taira Database Migrations

This folder contains all database migration scripts for the Taira application.

## Migration Files

### 1. `migrate_database.py`
- **Purpose**: Adds `ai_generated` column to the `lead` table
- **When to run**: Initial AI features setup
- **Columns added**: `ai_generated` (BOOLEAN, default=False)

### 2. `migrate_user_profile.py`
- **Purpose**: Adds company information fields to the `user` table
- **When to run**: When implementing user profile features
- **Columns added**: `company_name` (TEXT), `company_website` (TEXT)

### 3. `migrate_lead_instructions.py`
- **Purpose**: Adds additional instructions field to the `lead` table
- **When to run**: When implementing custom AI instructions
- **Columns added**: `additional_instructions` (TEXT)

## Running Migrations

### Option 1: Run All Migrations (Recommended)
```bash
python app/migrations/run_migrations.py
```

### Option 2: Run Individual Migrations
```bash
# From project root
python app/migrations/migrate_database.py
python app/migrations/migrate_user_profile.py
python app/migrations/migrate_lead_instructions.py
```

### Option 3: Check Migration Status
```bash
python app/migrations/check_migration_status.py
```

## Migration Order

Migrations should be run in this specific order:

1. **migrate_database.py** - Core AI features
2. **migrate_user_profile.py** - User company context
3. **migrate_lead_instructions.py** - Custom AI instructions

## Safety Notes

- **Always backup your database** before running migrations
- Migrations are designed to be safe and non-destructive
- Each migration checks if columns already exist before adding them
- Failed migrations can be re-run safely

## Troubleshooting

### Common Issues

1. **"Database file not found"**
   - Make sure you're running from the project root
   - Check that `taira.db` exists in the project directory

2. **"Column already exists"**
   - This is normal if the migration was already run
   - The migration will skip existing columns

3. **"Permission denied"**
   - Make sure the database file is not locked by another process
   - Close any applications that might be using the database

### Getting Help

If you encounter issues:
1. Check the error messages carefully
2. Verify your database file exists and is accessible
3. Try running migrations individually to isolate the problem
4. Check the migration status with the status checker

## Development

When adding new migrations:

1. Create a new migration file following the naming pattern: `migrate_[feature].py`
2. Include a main function that can be called from the migration runner
3. Add the migration to the list in `run_migrations.py`
4. Test the migration thoroughly before committing
5. Update this README with the new migration information
