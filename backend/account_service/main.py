from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

account_service = FastAPI()

account_service.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://192.168.0.102:8080",
        "http://127.0.0.1:8081",
        "http://0.0.0.0:8002",
        "http://0.0.0.0:8003",
        "http://localhost:8081"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# Include the routes
account_service.include_router(router)

# Add metadata
@account_service.get("/")
def root():
    return {"message": "Savings Goal Service is up and running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(account_service, host="0.0.0.0", port=8003)