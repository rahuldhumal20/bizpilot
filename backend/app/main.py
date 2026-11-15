
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="BizPilot API",
    description="Multi-Agent AI Business Consulting Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://bizpilotn.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router, prefix="/api")


@app.get("/")
def home():
    return {
        "message": "Welcome to BizPilot",
        "status": "Online"
    }


@app.get("/api/health")
def health():
    return {
        "success": True,
        "message": "BizPilot API is healthy"
    }
