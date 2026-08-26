def url_cache_key(short_code_url: str) -> str:
    """Build the Redis cache key for a shortened URL."""
    return f"url:{short_code_url}"