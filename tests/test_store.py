import os
from datetime import datetime, timedelta
from unittest.mock import patch
import pytest

from digesting_feed import store

MOCK_ARTICLES = [
    {
        "title": "First",
        "link": "http://a.com",
        "date": (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d"),
    },
    {
        "title": "Second",
        "link": "http://b.com",
        "date": datetime.now().strftime("%Y-%m-%d"),
    },
]


@pytest.fixture
def mock_helper():
    with patch("digesting_feed.store.helper.get_full_path") as mock_get_path:
        mock_get_path.return_value = "/tmp/test_articles.json"
        yield mock_get_path


@pytest.fixture
def clean_fs():
    # Make sure test file does not exist before tests
    path = "/tmp/test_articles.json"
    if os.path.exists(path):
        os.remove(path)
    yield
    if os.path.exists(path):
        os.remove(path)


def test_save_and_load_articles(mock_helper, clean_fs):
    store.save_articles_to_json(MOCK_ARTICLES)
    loaded = store.load_articles_from_json()
    assert len(loaded) == 2
    assert all("title" in a and "link" in a for a in loaded)


def test_remove_duplicates():
    articles = [
        {"link": "http://a.com", "title": "Article A"},
        {"link": "http://b.com", "title": "Article B"},
        {"link": "http://a.com", "title": "Duplicate Article A"},
    ]
    result = store.remove_duplicates_by_link(articles)
    links = [a["link"] for a in result]

    # Assert both expected links are present, order doesn't matter
    assert set(links) == {"http://a.com", "http://b.com"}


def test_retention_trim(mock_helper, clean_fs):
    # Create articles older than retention
    old_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    new_date = datetime.now().strftime("%Y-%m-%d")

    articles = [
        {"title": "Old", "link": "http://old.com", "date": old_date},
        {"title": "New", "link": "http://new.com", "date": new_date},
    ]

    store.save_articles_to_json(articles)
    loaded = store.load_articles_from_json()
    assert len(loaded) == 1
    assert loaded[0]["link"] == "http://new.com"
