from datetime import datetime
import os
import requests


def generate_log(data):
    """Write a list of log entries to a dated file and return the filename.

    Raises ValueError if `data` is not a list.
    """
    if not isinstance(data, list):
        raise ValueError("data must be a list")

    today = datetime.now().strftime("%Y%m%d")
    filename = f"log_{today}.txt"

    with open(filename, "w") as file:
        for entry in data:
            file.write(f"{entry}\n")

    print(f"Log written to {filename}")
    return filename


def fetch_data():
    """Fetch a sample post from a public API and return parsed JSON.

    Returns empty dict on any error.
    """
    url = "https://jsonplaceholder.typicode.com/posts/1"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return {}


if __name__ == "__main__":
    sample_log = ["User logged in", "User updated profile", "Report exported"]
    generate_log(sample_log)

    post = fetch_data()
    print("Fetched Post Title:", post.get("title", "No title found"))
