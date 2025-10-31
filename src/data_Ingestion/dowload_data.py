import os
import urllib.request
from dotenv import load_dotenv

def download_data_from_github():
    """
    Loads GITHUB_DATA_URL from .env and downloads the file into data/raw/
    """
    # Load variables from .env file
    load_dotenv()

    # Get GitHub URL from environment
    github_url = os.getenv("GITHUB_DATA_URL")
    if not github_url:
        raise ValueError("❌ Missing GITHUB_DATA_URL in .env file")

    # Make sure raw data folder exists
    raw_dir = os.path.join("data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    # Get filename from URL (last part after '/')
    filename = github_url.split("/")[-1]
    if not filename:
        filename = "downloaded_data"

    # Target path
    file_path = os.path.join(raw_dir, filename)

    # Download the file
    print(f"⬇️  Downloading from {github_url} ...")
    urllib.request.urlretrieve(github_url, file_path)
    print(f"✅ Data saved at: {file_path}")

    return file_path


if __name__ == "__main__":
    download_data_from_github()
