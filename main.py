# Library imports
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

import json
import csv

from dotenv import load_dotenv
from io import StringIO

import uvicorn

# DB Model imports
from models import User, Post, Lead

# CRUD Datatypes imports.
from schema import UserRead, UserCreate, UserUpdate, UserDelete
from schema import PostCreate, PostUpdate, PostDelete, PostRead
from schema import LeadRead

# DB Methods import
import dbconf

app = FastAPI(title="GlimpseProject API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/db-status")
async def db_status():
    """Check database connection using SQLAlchemy"""
    if dbconf.test_connection():
        return {"status": "connected", "message": "Database connection successful"}
    else:
        raise HTTPException(status_code=500, detail="Database connection failed")


@app.get("/leads/", response_model=List[LeadRead])
async def get_leads(id: Optional[int] = None,
                    name: Optional[str] = None,
                    source: Optional[str] = None,
                    interest_level: Optional[str] = None,
                    status: Optional[str] = None,
                    salesperson: Optional[str] = None,
                    db: Session = Depends(dbconf.get_database_session)):
    query = db.query(Lead)

    if id is not None:
        query = query.filter(Lead.id == id)  # ✅ Assign back to query
    else:
        if name is not None:
            query = query.filter(Lead.lead_name == name)  # ✅ Use correct column name
        if source is not None:
            query = query.filter(Lead.source == source)
        if interest_level is not None:
            query = query.filter(Lead.interest_level == interest_level)
        if status is not None:
            query = query.filter(Lead.status == status)
        if salesperson is not None:
            query = query.filter(Lead.salesperson == salesperson)

    leads = query.all()
    
    # ✅ Let Pydantic handle the conversion automatically
    return leads

# async def process_json_data(contents: bytes, db: Session):
#     data = json.loads(contents)
#     processed_count = 0

#     for item in data:
#         print(item)
#         # Process each item in the JSON data
#         # Eg, a json defined USER, create and batch 
#         # update the database.

#         # eg create some object
#         # create model class eg 
#         # row["user_id"] = int(row["user_id"]) // Cast type to match our PostCreate class.
#         # post = PostCreate(**row)
#         # db_post = Post(**post.model_dump())
#         # db.add(db_post)
#         processed_count += 1
#         pass

async def process_csv_data(contents: bytes, db: Session):
    csv_reader = csv.DictReader(StringIO(contents.decode("utf-8")))
    processed = 0

    for row in csv_reader:
        try:
            lead = Lead(
                id=int(row["Lead ID"]),
                lead_name=row.get("Lead Name"),
                email=row.get("Contact Information"),
                source=row.get("Source"),
                interest_level=row.get("Interest Level"),
                status=row.get("Status"),
                salesperson=row.get("Assigned Salesperson")
            )

            db.merge(lead)
            processed += 1
                
        except Exception as e:
            print(f"Skipping invalid row: {e}")
            continue

    db.commit()
    return processed  # Return total processed

@app.post("/files/", response_model=dict)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(dbconf.get_database_session)):
    # Handle file upload
    contents = await file.read()
    try:
        processed_count = 0
        # Process the file contents (e.g., save to database, store in local FS, whatever we want)
        if file.content_type == "application/json":
            print("Unsupported file type")
        elif file.content_type == "text/csv":
            processed_count = await process_csv_data(contents, db)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        return {
            "filename": file.filename,
            "processed_count": processed_count,
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")

load_dotenv()

# Not an async method
def startup_event():
    """Event handler for application startup."""
    if not dbconf.comprehensive_db_check():
        raise RuntimeError("Database issues detected - may have unexpected behaviors")
    else:
        print("✅ All database checks passed")

    print("Starting application...")

if __name__ == "__main__":
    startup_event() # Test the connection and migration status of our app
    port = int(os.getenv("PORT", 8888))
    uvicorn.run(app, host="0.0.0.0", port=port)
