# from fastapi import FastAPI
# from auth_service.routes import auth_router

# auth_service = FastAPI()
# # Adding a sample route at the root URL
# @auth_service.get("/")
# def read_root():
#     return {"message": "Welcome to the Auth Service!"}
# auth_service.include_router(auth_router)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(auth_service, host="0.0.0.0", port=8001)



from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Sample data storage (you can replace this with an actual database)
users_db = {}

auth_service = FastAPI()

# Allow cross-origin requests from the frontend's origin
auth_service.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8081"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
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
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    # Here, you would hash the password before saving it
    users_db[user.email] = user.password
    return JSONResponse(content={"message": "User registered successfully!"})

@auth_service.post("/auth")
async def login(user: User):
    print("User data received", user)
    if user.email not in users_db or users_db[user.email] != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    
    return JSONResponse(content={"message": "Login successful!"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(auth_service, host="0.0.0.0", port=8001)

