from src.data_Ingestion.extract_data import extract_raw_data
from src.data_Ingestion.dowload_data import download_data_from_github


def main():
    download_data_from_github()

    extract_raw_data()


if __name__ == "__main__":
    main()
