import uvicorn
from api import app
from config.config import Settings
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_server():
    server = Settings.server
    config = uvicorn.Config(
        "main:app",
        host=server.host,
        port=server.port, 
        log_level=server.log_level,
        workers=server.workers,
        reload=server.reload
    )
    server = uvicorn.Server(config)

    try:
        logger.info("Starting server...")
        await server.serve()
    except asyncio.CancelledError:
        logger.info("\nServer is shutting down gracefully...")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        # Perform any cleanup here (e.g., closing database connections)
        logger.info("Cleanup complete. Server stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("\nServer interrupted by user. Shutting down...")