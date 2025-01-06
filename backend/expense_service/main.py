from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from expense_service.routes import expense_router


# FastAPI app
expense_service = FastAPI()

# CORS Middleware
expense_service.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://192.168.0.102:8080",
        "http://127.0.0.1:8081",
        "http://0.0.0.0:8002",
        "http://localhost:8081"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routes
expense_service.include_router(expense_router)

@expense_service.get("/")
def read_root():
    return {"message": "Welcome to the Expense Service!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(expense_service, host="0.0.0.0", port=8002)
