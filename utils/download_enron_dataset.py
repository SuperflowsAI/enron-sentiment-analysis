import requests
from tqdm import tqdm

def download_file(url, local_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get("content-length", 0))
        with open(local_path, "wb") as f, tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    progress_bar.update(len(chunk))

def extract_tar_gz(tar_gz_file, target_dir):
    with tarfile.open(tar_gz_file, "r:gz") as tf:
        tf.extractall(target_dir)

url = "https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tar.gz"
local_zip_path = "enron_mail_20150507.tar.gz"
local_extract_path = "enron_dataset"

# Download the dataset
print("Downloading the Enron email dataset...")
download_file(url, local_zip_path)