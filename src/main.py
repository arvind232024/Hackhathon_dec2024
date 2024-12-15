from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from mangum import Mangum
from src.generate import router  # Import the router from generate.py
import uvicorn


# Create FastAPI app instance
app = FastAPI()
# handler = Mangum(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)

# Define server running function
def run_server():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

# Entry point
if __name__ == "__main__":
    run_server()
