import uvicorn
from api.v1.api import app  # Ensure this imports your FastAPI app
from db import database
from core.config import Settings
import os
import asyncio

# Set PYTHONDONTWRITEBYTECODE to disable bytecode generation
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
database.Base.metadata.create_all(database.engine)

async def run_server():
    server = Settings.server
    config = uvicorn.Config(
        "main:app", 
        port=server.port, 
        log_level=server.log_level,
        workers=server.workers,
        reload=server.reload
    )
    server = uvicorn.Server(config)

    try:
        # Run the server
        await server.serve()
    except asyncio.CancelledError:
        print("\nServer is shutting down gracefully...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Perform any cleanup here (e.g., closing database connections)
        print("Cleanup complete. Server stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\nServer interrupted by user. Shutting down...")