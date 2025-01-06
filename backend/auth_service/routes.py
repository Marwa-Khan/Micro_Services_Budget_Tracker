from fastapi import APIRouter, HTTPException
# from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation

# from shared.database import get_db_connection, release_db_connection
from auth_service.database import get_db_connection, release_db_connection

class User(BaseModel):
    email: str
    password: str

auth_router = APIRouter()

@auth_router.post("/register")
async def register(user: User):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id",
            ( user.email, user.password)  # Use hashed passwords in production
        )
        new_user = cursor.fetchone()
        print("new_user===", new_user)
        conn.commit()
        return JSONResponse(content={"message": "User registered successfully!", "id": int(new_user["id"])+1})
    except UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Email already registered.")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        release_db_connection(conn)

@auth_router.post("/auth")
async def login(user: User):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            "SELECT id, password_hash FROM users WHERE email = %s",
            (user.email,)
        )
        db_user = cursor.fetchone()
        if not db_user or db_user["password_hash"] != user.password:  # Use hashed password comparison in production
            raise HTTPException(status_code=400, detail="Invalid credentials.")
        return JSONResponse(content={"message": "Login successful!", "id": db_user["id"]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        release_db_connection(conn)