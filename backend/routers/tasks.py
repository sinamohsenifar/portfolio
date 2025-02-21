from webbrowser import BackgroundBrowser
from fastapi import APIRouter, BackgroundTasks
from services.tasks import background_backup
tasks_router = APIRouter()


@tasks_router.post("/run_backup/")
def run_backup(id: int, count: int, bt: BackgroundTasks):
    bt.add_task(background_backup, id, count)