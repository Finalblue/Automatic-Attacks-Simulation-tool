# For validating the URL format
def validate_url(url):
    return url.startswith("http://") or url.startswith("https://")
