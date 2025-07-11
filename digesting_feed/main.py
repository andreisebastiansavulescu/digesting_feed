"""Main module to fetch, score, save, and generate daily devops digest articles."""

from datetime import datetime
from .fetcher import fetch_hn_articles, fetch_reddit_articles, fetch_tech_blog_articles
from .generator import generate_html
from .store import save_articles_to_json


def score_article(article):
    """Score an article based on its title and source."""
    title = article["title"].lower()
    keywords = [
        "devops",
        "cloud",
        "kubernetes",
        "observability",
        "ai",
        "infra",
        "platform",
        "reliability",
        "linux",
        "docker",
        "automation",
        "monitoring",
        "security",
        "scalability",
        "performance",
        "networking",
    ]
    score = sum(1 for kw in keywords if kw in title)

    source_weights = {
        "Netflix": 3,
        "Amazon AWS": 3,
        "Google": 3,
        "Microsoft": 2,
        "Hacker News": 2,
        "Reddit": 1,
    }
    score += source_weights.get(article["source"], 0)
    return score


def main():
    """Main function to fetch articles, score them, add date, save, and generate HTML."""
    articles = (
        fetch_hn_articles() + fetch_reddit_articles() + fetch_tech_blog_articles()
    )

    today_str = datetime.now().strftime("%Y-%m-%d")

    for article in articles:
        article["score"] = score_article(article)
        article["date"] = today_str  # Add today's date here

    top_articles = sorted(articles, key=lambda x: x["score"], reverse=True)[:20]

    save_articles_to_json(top_articles)

    generate_html(top_articles)


if __name__ == "__main__":
    main()
