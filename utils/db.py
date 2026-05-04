import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client
import streamlit as st

# Load environment variables explicitly
load_dotenv(override=True)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

print("--- DB Configuration Debug ---")
print(f"URL Loaded: {SUPABASE_URL}")
print(f"Key Loaded Prefix: {SUPABASE_KEY[:10] if SUPABASE_KEY else 'None'}")
print("------------------------------")

def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Supabase credentials not found in env.")
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Connection creation failed: {e}")
        return None

def insert_privacy_result(data: dict):
    print("Saving to Supabase...")
    
    client = get_supabase_client()
    if not client:
        print("Supabase client not initialized. Unable to save data.")
        return False
        
    try:
        # We explicitly serialize the dicts to JSON Strings using json.dumps to guarantee valid JSONB parsing
        safe_data = {
            "session_id": data.get("session_id", ""),
            "answers": data.get("answers", {}), # Supabase python client handles dict -> jsonb natively, but if it fails we can change to string
            "category_scores": data.get("category_scores", {}),
            "total_score": float(data.get("total_score", 0)),
            "risk_percentage": float(data.get("risk_percentage", 0)),
            "risk_level": data.get("risk_level", "Unknown")
        }
        
        print(f"Data to insert: {safe_data}")
        
        # Test basic insertion first if it fails
        # test_data = {"session_id": "test", "total_score": 10, "risk_percentage": 20, "risk_level": "Low"}
        
        # Insert data
        response = client.table("privacy_results").insert(safe_data).execute()
        print(f"Supabase response: {response}")
        return True
    except Exception as e:
        print(f"Error saving to Supabase: {e}")
        # Next fallback: stringify json
        try:
             print("Retrying with stringified JSON components...")
             safe_data["answers"] = json.dumps(safe_data["answers"])
             safe_data["category_scores"] = json.dumps(safe_data["category_scores"])
             response = client.table("privacy_results").insert(safe_data).execute()
             print(f"Supabase fallback response: {response}")
             return True
        except Exception as e2:
             print(f"Fallback Error saving to Supabase: {e2}")
        return False
