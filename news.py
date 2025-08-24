# news.py
from datetime import datetime
from zoneinfo import ZoneInfo
from html import unescape
import feedparser

# Google News RSS accepts:
#   hl=<language-REGION> (UI language)
#   gl=<COUNTRY>         (geo)
#   ceid=<COUNTRY>:<lang>
#
# Topic keys map to Google News topic params
TOPIC_MAP = {
    "Top stories": "",
    "World": "topic=WORLD",
    "U.S.": "topic=NATION",
    "Business": "topic=BUSINESS",
    "Technology": "topic=TECHNOLOGY",
    "Science": "topic=SCIENCE",
    "Health": "topic=HEALTH",
    "Entertainment": "topic=ENTERTAINMENT",
    "Sports": "topic=SPORTS",
}

def _build_url(country: str = "US", language: str = "en", topic_key: str = "Top stories") -> str:
    """
    Build a Google News RSS URL for any country/language/topic.
    Examples:
      country="IN", language="en", topic="World" -> WORLD feed localized to India
      country="GB", language="en", topic="Top stories" -> UK top stories
    """
    base = f"https://news.google.com/rss?hl={language}-{country}&gl={country}&ceid={country}:{language}"
    topic_param = TOPIC_MAP.get(topic_key, "")
    return base if not topic_param else f"{base}&{topic_param}"

def fetch_news(
    topic_key: str = "Top stories",
    country: str = "US",
    language: str = "en",
    limit: int = 8,
    display_tz: str = "UTC",
):
    """
    Fetch news items. Times are converted to display_tz (IANA name e.g. 'US/Pacific', 'Europe/London').
    Returns a list of dicts: title, summary, link, source, time.
    """
    url = _build_url(country=country, language=language, topic_key=topic_key)
    feed = feedparser.parse(url)

    items = []
    for e in feed.entries[:limit]:
        # published_parsed is in UTC
        ts_str = ""
        if getattr(e, "published_parsed", None):
            dt_utc = datetime(*e.published_parsed[:6], tzinfo=ZoneInfo("UTC"))
            dt_local = dt_utc.astimezone(ZoneInfo(display_tz))
            ts_str = dt_local.strftime("%b %d, %I:%M %p")

        items.append({
            "title": unescape(getattr(e, "title", "")),
            "summary": unescape(getattr(e, "summary", ""))[:300],
            "link": getattr(e, "link", ""),
            "source": getattr(e, "source", {}).get("title", getattr(e, "publisher", "")),
            "time": ts_str,
        })
    return items
