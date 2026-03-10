from dataclasses import dataclass
from dotenv import load_dotenv
import os
from typing import Dict

load_dotenv()


@dataclass
class Config:
    groq_api_key: str
    github_token: str
    repo_owner: str
    repo_name: str


def load_config() -> Config:
    env_values: Dict[str, str] = {
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY", "").strip(),
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN", "").strip(),
        "REPO_OWNER": os.getenv("REPO_OWNER", "").strip(),
        "REPO_NAME": os.getenv("REPO_NAME", "").strip(),
    }
    missing = [key for key, value in env_values.items() if not value]
    if missing:
        raise EnvironmentError(
            "The following environment variables must be set: "
            + ", ".join(missing)
        )
    return Config(
        groq_api_key=env_values["GROQ_API_KEY"],
        github_token=env_values["GITHUB_TOKEN"],
        repo_owner=env_values["REPO_OWNER"],
        repo_name=env_values["REPO_NAME"],
    )
