"""Fixtures for pytest to set up the environment for tests."""

import pytest
import nltk


@pytest.fixture(autouse=True, scope="session")
def download_nltk_punkt():
    """Download NLTK punkt tokenizer data."""
    nltk.download("punkt_tab", quiet=True)
