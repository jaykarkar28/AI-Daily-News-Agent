from dotenv import load_dotenv
import os

load_dotenv()

github_token = os.getenv("GITHUB_API_TOKEN")

headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github+json",
}