from typing import Any, Dict

from curl_cffi import requests

from .base import TunnelBase


class CurlImpersonateTunnel(TunnelBase):

    def __init__(self, browser: str):
        self.browser = browser

    def configure(self, config: Dict[str, Any]) -> None:
        self.host = config["browser"]

    def make_request(self, url: str, headers: Dict[str, str]):
        try:
            # Notice the impersonate parameter
            response = requests.get(url, impersonate="chrome")

            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "html": response.text,
            }
        except Exception as e:
            return {
                "status_code": 500,
                "headers": {},
                "html": None,
                "error": str(e),
            }
