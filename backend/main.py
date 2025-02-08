import uvicorn
from src.app import app
from core.config import Settings

server = Settings.server
if __name__ == "__main__":
    config = uvicorn.Config(
        "main:app", 
        port=server.port, 
        log_level=server.log_level,
        workers=server.workers,
        reload=server.reload
    )
    server = uvicorn.Server(config)
    server.run()