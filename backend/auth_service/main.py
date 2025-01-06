
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from routes import auth_router
from auth_service.routes import auth_router
import random
auth_service = FastAPI()

# Allow cross-origin requests from the frontend's origin
auth_service.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080","http://192.168.0.102:8080","http://127.0.0.1:8081","http://0.0.0.0:8001","http://localhost:8081"], 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

auth_service.include_router(auth_router)

@auth_service.get("/")
def read_root():
    return {"message": "Welcome to the Auth Service!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(auth_service, host=" http://127.0.0.1", port=8001)
    # http://127.0.0.1:8001/


