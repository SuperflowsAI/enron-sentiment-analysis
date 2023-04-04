import requests
import tarfile
from pathlib import Path
from tqdm import tqdm
from utils.loadsave_emails import *

CHUNK_SIZE = 8192
URL = "https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tar.gz"
LOCAL_ZIP_PATH = Path("enron_mail_20150507.tar.gz")
LOCAL_EXTRACT_PATH = Path("enron_dataset")
LOCAL_JSON_PATH = Path("enron_dataset.json")

def download_file(url, local_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get("content-length", 0))
        with open(local_path, "wb") as f, tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
                    progress_bar.update(len(chunk))

def extract_tar_gz(tar_gz_file, target_dir):
    with tarfile.open(tar_gz_file, "r:gz") as tf:
        tf.extractall(target_dir)

if __name__ == "__main__":
    # Download the dataset
    print("Downloading the Enron email dataset...")
    download_file(URL, LOCAL_ZIP_PATH)

    # Extract the dataset
    print("Extracting the Enron email dataset...")
    extract_tar_gz(LOCAL_ZIP_PATH, LOCAL_EXTRACT_PATH)

    # Load and save emails
    emails = get_emails_from_directory(LOCAL_EXTRACT_PATH)
    save_emails_to_json(emails, LOCAL_EXTRACT_PATH / LOCAL_JSON_PATH)
