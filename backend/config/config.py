import string
from fastapi import logger
import yaml
from pydantic import BaseModel
import pathlib


cwd = pathlib.Path(__file__).parent.parent
config_file = cwd / "config.yaml"



class Server(BaseModel):
    port: int
    address: str
    log_level: str
    workers: int
    reload: bool

    
class Sqlite(BaseModel):
    uri: str
    username: str
    password: str
    autocommit: bool
    autoflush: bool

class Config(BaseModel):
    server: Server
    sqlite: Sqlite
    

def _load_yml_config(path: pathlib.Path):
    """Classmethod returns YAML config"""
    try:
        return yaml.safe_load(path.read_text())

    except FileNotFoundError as error:
        message = "Error: yml config file not found."
        logger.logger.error(message)
        raise FileNotFoundError(error, message) from error


Settings = Config(**_load_yml_config(config_file))