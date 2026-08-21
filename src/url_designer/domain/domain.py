from urllib.parse import urlparse
class OriginalUrl:
    def __init__(self,url:str):
        self.url=url
        self.validate_url(url)

    def validate_url(self,url:str) -> None:
        parse_url=urlparse(url)

        if parse_url.scheme not in ["http","https"]:
            raise ValueError("URL must use HTTP or HTTPS.")
        if parse_url.netloc !="":
            raise ValueError("URL must contain a host.")


