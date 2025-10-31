import os
import shutil
import zipfile
import tarfile
import json
import csv

def convert_to_csv(file_path, output_dir):
    """
    Converts .json or .txt files to .csv format.
    Saves output file with same name but .csv extension.
    """
    base = os.path.basename(file_path)
    name, _ = os.path.splitext(base)
    csv_path = os.path.join(output_dir, f"{name}.csv")

    try:
        # --- JSON to CSV ---
        if file_path.lower().endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Convert dict or list of dicts to CSV
            if isinstance(data, dict):
                data = [data]

            if isinstance(data, list) and len(data) > 0:
                keys = data[0].keys()
                with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(data)
                print(f"🧩 Converted JSON → CSV: {csv_path}")

        # --- TXT to CSV ---
        elif file_path.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f_in, open(csv_path, "w", newline="", encoding="utf-8") as f_out:
                writer = csv.writer(f_out)
                for line in f_in:
                    row = line.strip().split()  # split by space
                    writer.writerow(row)
            print(f"📜 Converted TXT → CSV: {csv_path}")

        else:
            print(f"⚠️ Skipped conversion (unsupported format): {file_path}")

    except Exception as e:
        print(f"❌ Error converting {file_path} → {e}")


def extract_raw_data():
    """
    Extracts or copies raw data files from data/raw to data/interim.
    - If file is .zip/.tar/.tar.gz/.tgz → extracts it
    - If file is .csv/.json/.txt/.parquet → simply copies it
    - After extraction, converts non-CSV files to CSV if possible
    """
    raw_dir = os.path.join("data", "raw")
    interim_dir = os.path.join("data", "intermediate")
    os.makedirs(interim_dir, exist_ok=True)

    supported_direct_copy = (".csv", ".json", ".txt", ".parquet")

    for file in os.listdir(raw_dir):
        src_path = os.path.join(raw_dir, file)
        if not os.path.isfile(src_path):
            continue

        file_lower = file.lower()

        # --- Direct copy ---
        if file_lower.endswith(supported_direct_copy):
            dst_path = os.path.join(interim_dir, file)
            shutil.copy2(src_path, dst_path)
            print(f"📄 Copied: {file}")

        # --- ZIP extraction ---
        elif file_lower.endswith(".zip"):
            with zipfile.ZipFile(src_path, "r") as zip_ref:
                zip_ref.extractall(interim_dir)
            print(f"🗜️ Extracted ZIP: {file}")

        # --- TAR/TAR.GZ/TGZ extraction ---
        elif file_lower.endswith((".tar", ".tar.gz", ".tgz")):
            with tarfile.open(src_path, "r:*") as tar_ref:
                tar_ref.extractall(interim_dir)
            print(f"📦 Extracted TAR: {file}")

        else:
            print(f"⚠️ Skipped (unsupported): {file}")

    # --- Convert non-CSV files inside interim_dir ---
    for extracted in os.listdir(interim_dir):
        file_path = os.path.join(interim_dir, extracted)
        if not extracted.lower().endswith(".csv"):
            convert_to_csv(file_path, interim_dir)

    print(f"✅ Extraction & conversion complete → {interim_dir}")
    return interim_dir


if __name__ == "__main__":
    extract_raw_data()
