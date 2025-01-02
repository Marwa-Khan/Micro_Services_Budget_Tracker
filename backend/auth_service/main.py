# # from fastapi import FastAPI
# # from auth_service.routes import auth_router

# # auth_service = FastAPI()
# # # Adding a sample route at the root URL
# # @auth_service.get("/")
# # def read_root():
# #     return {"message": "Welcome to the Auth Service!"}
# # auth_service.include_router(auth_router)

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(auth_service, host="0.0.0.0", port=8001)



# from fastapi import FastAPI, HTTPException, Body
# from pydantic import BaseModel
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware

# # Sample data storage (you can replace this with an actual database)
# users_db = {}

# auth_service = FastAPI()

# # Allow cross-origin requests from the frontend's origin
# auth_service.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://127.0.0.1:8081"],  # Frontend URL
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allow all headers
# )

# class User(BaseModel):

#     email: str
#     password: str

# @auth_service.get("/")
# def read_root():
#     return {"message": "Welcome to the Auth Service!"}

# @auth_service.post("/register")
# async def register(user: User):
#     if user.email in users_db:
#         raise HTTPException(status_code=400, detail="Email already registered.")
    
#     # Here, you would hash the password before saving it
#     users_db[user.email] = user.password
#     return JSONResponse(content={"message": "User registered successfully!"})

# @auth_service.post("/auth")
# async def login(user: User):
#     print("User data received", user)
#     if user.email not in users_db or users_db[user.email] != user.password:
#         raise HTTPException(status_code=400, detail="Invalid credentials.")
    
#     return JSONResponse(content={"message": "Login successful!"})

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(auth_service, host="0.0.0.0", port=8001)



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation
from psycopg2 import pool
import random

# Database connection pool
DATABASE_CONFIG = {
    'dbname': 'user_services',
    'user': 'postgres',
    'password': '9009',
    'host': 'localhost',
    'port': '5432'
}

connection_pool = pool.SimpleConnectionPool(
    1, 20,
    dbname=DATABASE_CONFIG['dbname'],
    user=DATABASE_CONFIG['user'],
    password=DATABASE_CONFIG['password'],
    host=DATABASE_CONFIG['host'],
    port=DATABASE_CONFIG['port']
)

def get_db_connection():
    if connection_pool:
        return connection_pool.getconn()

def release_db_connection(conn):
    if connection_pool:
        connection_pool.putconn(conn)


auth_service = FastAPI()

# Allow cross-origin requests from the frontend's origin
auth_service.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080","http://192.168.0.102:8080","http://127.0.0.1:8081","http://0.0.0.0:8001","http://localhost:8081"], 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class User(BaseModel):
    email: str
    password: str

@auth_service.get("/")
def read_root():
    return {"message": "Welcome to the Auth Service!"}

@auth_service.post("/register")
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


@auth_service.post("/auth")
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(auth_service, host="0.0.0.0", port=8001)


