# Variables
BACKEND_DIR = backend
FRONTEND_DIR = frontend
VENV = backend/.env/bin/activate

# Start both backend and frontend
start: start-backend #start-frontend

# Start backend with file watching
start-backend:
	@echo "Starting backend..."
	@source $(VENV) && watchmedo auto-restart --directory=$(BACKEND_DIR) --pattern="*.py" --recursive -- python3 $(BACKEND_DIR)/main.py || (echo "Backend crashed" && exit 1)

# Start frontend with file watching
# start-frontend:
#     @echo "Starting frontend..."
#     @cd $(FRONTEND_DIR) && npm run dev || (echo "Frontend crashed" && exit 1)

# Clean up processes
stop:
	@echo "Stopping all processes..."
	@pkill -f "watchmedo" || true
	@pkill -f "python $(BACKEND_DIR)/main.py" || true
    #@pkill -f "npm run dev" || true

# Ensure clean stop on interrupt
.PHONY: start start-backend start-frontend stop