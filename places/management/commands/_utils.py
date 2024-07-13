import json
import requests

MAX_TRIES = 3


def fetch_image_content(url: str, tries=MAX_TRIES) -> bytes | None:
    for _ in range(tries):
        try:
            response = requests.get(url)
            if "image" in response.headers.get("Content-Type", ""):
                return response.content
        except requests.exceptions.RequestException:
            continue

    return None


def fetch_json(url: str, tries=MAX_TRIES) -> dict:
    headers = {"Accept": "application/json"}
    for _ in range(tries):
        try:
            response = requests.get(url, headers=headers)
            if "application/json" in response.headers.get("Content-Type", ""):
                return response.json()

            if "text/plain" in response.headers.get("Content-Type"):
                content = response.content.decode(response.encoding or 'utf-8')
                return json.loads(content)

        except requests.exceptions.RequestException:
            continue
    raise Exception("Failed to fetch JSON data")
