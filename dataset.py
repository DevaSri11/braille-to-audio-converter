import gdown
import zipfile
import os

# Google Drive file ID for your dataset
FILE_ID = "198StxDtEMsuPmvQpy3S8fHQerqJZhH1x"
OUTPUT_FILE = "Braille_Dataset.zip"
EXTRACT_DIR = "data"

def download_dataset():
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    if not os.path.exists(OUTPUT_FILE):
        print("⬇️ Downloading dataset...")
        gdown.download(url, OUTPUT_FILE, quiet=False)
    else:
        print("✅ Dataset file already exists.")

    if not os.path.exists(EXTRACT_DIR):
        print("📦 Extracting dataset...")
        with zipfile.ZipFile(OUTPUT_FILE, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)
        print("✅ Extraction complete into:", EXTRACT_DIR)
    else:
        print("📁 Data directory already exists.")

if __name__ == "__main__":
    download_dataset()
