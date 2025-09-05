# Database configuration file for Glimpse application
# Updated for SQLAlchemy + Alembic workflow

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from models import Base
from typing import Generator

# Alembic imports
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from alembic.autogenerate import compare_metadata
from io import StringIO

load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/glimpse")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_database_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection in FastAPI.
    
    Usage in FastAPI:
    from fastapi import Depends
    from dbconf import get_database_session
    
    @app.get("/users/")
    def get_users(db: Session = Depends(get_database_session)):
        return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session() -> Session:
    """
    Get a database session for use in non-FastAPI contexts.
    Remember to close the session when done!
    
    Usage:
    from models import User
    from dbconf import get_db_session
    
    db = get_db_session()
    try:
        users = db.query(User).all()
        # ... do work ...
        db.commit()
    finally:
        db.close()
    """
    return SessionLocal()

def test_connection() -> bool:
    """Test database connection"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Database connection successful!")
        return True
    except SQLAlchemyError as e:
        print(f"Database connection failed: {e}")
        return False
    
def check_migration_status() -> bool:
    """Check if DB Schema is up to date with migrations"""
    try:
        alembic_cfg = Config("alembic.ini")
        script = ScriptDirectory.from_config(alembic_cfg)

        with engine.connect() as connection:
            # Check the migration context
            context = MigrationContext.configure(connection)
            current_rev = context.get_current_revision()
            head_rev = script.get_current_head()

            if current_rev != head_rev:
                print("DB Schema Outdated")
                print(f"Current DB Revision: {current_rev}, Head Revision: {head_rev}")
                return False

            print("DB Schema Up to Date")
            return True

    except Exception as e:
        print(f"Error checking migration status: {e}")
        return False

def check_schema_drift() -> bool:
    """
    Check if models.py differs from actual database schema
    Returns True if schema matches, False if there are differences
    """
    try:
        alembic_cfg = Config("alembic.ini")
        
        with engine.connect() as connection:
            # Create migration context
            context = MigrationContext.configure(connection)
            
            # Compare metadata (models.py) with database
            diff = compare_metadata(context, Base.metadata)
            
            if diff:
                print("⚠️  Schema drift detected!")
                print("   Your models.py differs from the database schema:")
                for operation in diff:
                    print(f"   - {operation}")
                print("   Generate migration with: alembic revision --autogenerate -m 'description'")
                return False
            else:
                print("✅ Models match database schema")
                return True
                
    except Exception as e:
        print(f"Error checking schema drift: {e}")
        return False

def comprehensive_db_check() -> bool:
    """
    Complete database health check:
    1. Test connection
    2. Check migrations are applied  
    3. Check for schema drift (model changes not yet migrated)
    """
    print("🔍 Running database health check...")

    if os.getenv("RAILWAY_ENVIRONMENT_NAME"):
        return True
    
    # Step 1: Connection
    if not test_connection():
        print("❌ Database connection failed")
        return False
        
    # Step 2: Migration status
    if not check_migration_status():
        print("❌ Migrations not up to date")
        return False
        
    # Step 3: Schema drift detection
    if not check_schema_drift():
        print("❌ Schema drift detected - models.py has uncommitted changes")
        return False
        
    print("✅ All database checks passed!")
    return True
