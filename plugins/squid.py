from typing import Any, Dict

import requests
import ua_generator

from .base import TunnelBase


class SquidTunnel(TunnelBase):
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def configure(self, config: Dict[str, Any]) -> None:
        self.host = config["host"]
        self.port = config["port"]
        self.username = config["username"]
        self.password = config["password"]

    def make_request(self, url: str, headers: Dict[str, str]) -> Dict[str, Any]:
        proxy_url = f"http://{self.username}:{self.password}@{self.host}:{self.port}"
        proxies = {"http": proxy_url, "https": proxy_url}
        auth = (self.username, self.password)

        if "User-Agent" not in headers:
            headers["User-Agent"] = ua_generator.generate()

        try:
            response = requests.get(
                url, headers=headers, proxies=proxies, auth=auth, timeout=30
            )

            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "html": response.text,
            }
        except requests.RequestException as e:
            return {
                "status_code": 500,
                "headers": {},
                "html": None,
                "error": str(e),
            }
        except Exception as e:
            return {
                "status_code": 500,
                "headers": {},
                "html": None,
                "error": str(e),
            }
