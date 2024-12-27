from fastapi import APIRouter, HTTPException
from shared.database import get_db_connection, release_db_connection

auth_router = APIRouter()

@auth_router.post("/login")
def login(email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user or user[1] != password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Notification
        from shared.mqtt_client import publish_message
        publish_message("notifications", f"User {email} logged in.")
        
        return {"message": "Login successful"}
    finally:
        cursor.close()
        release_db_connection(conn)
