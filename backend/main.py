from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.routes import router as api_router
import logging
import os

# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging to file
LOG_FILE = os.path.join(LOG_DIR, "app.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # Optional: keeps logging in console too
    ]
)

logger = logging.getLogger(__name__)


app = FastAPI()

# Include API routes before mounting static frontend
app.include_router(api_router, prefix="/api")
logger.info("API router registered at /api")

# Mount static frontend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_path = os.path.join(BASE_DIR, "frontend")
app.mount("/", StaticFiles(directory=static_path, html=True), name="static")
logger.info(f"Frontend mounted from: {static_path}")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS middleware enabled for all origins")
