import os
from pydantic import BaseModel

# TODO: Leave as env vars or better way to initialize this


class Config(BaseModel):

    OLLAMA_API_URL: str = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api")
    OLLAMA_MODEL_NAME: str = os.environ.get(
        "OLLAMA_MODEL_NAME", "artifish/llama3.2-uncensored"
    )
    LLAMA_CLOUD_API_KEY: str = os.environ.get(
        "LLAMA_CLOUD_API_KEY", "llx-owzYtE9Fic0pVNqgf5Ni7WzxFeGB6snsqFWNvm1Xw6xs3DLe"
    )


config = Config()
