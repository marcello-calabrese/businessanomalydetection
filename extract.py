import os
from kaggle.api.kaggle_api_extended import KaggleApi
from kaggle_auth import USERNAME, KEY, DATASET



class KaggleDataExtractor:
    def __init__(self, username: str, key: str):
        self.username = username
        self.key = key

    def authenticate(self) -> None:
        os.environ['KAGGLE_USERNAME'] = self.username
        os.environ['KAGGLE_KEY'] = self.key

    def download_dataset(self, dataset, path) -> None:
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files(dataset, path=path, unzip=True)
        











