from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.routes import router as api_router
import os
import logging

# Global logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

# ✅ Include API routes before mounting static frontend
app.include_router(api_router, prefix="/api")
logger.info("✅ API router registered at /api")

# ✅ Mount static frontend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_path = os.path.join(BASE_DIR, "frontend")
app.mount("/", StaticFiles(directory=static_path, html=True), name="static")
logger.info(f"✅ Frontend mounted from: {static_path}")

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("✅ CORS middleware enabled for all origins")
