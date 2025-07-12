import pytest
import nltk


@pytest.fixture(autouse=True, scope="session")
def download_nltk_punkt():
    nltk.download("punkt_tab", quiet=True)
