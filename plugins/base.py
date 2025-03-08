from abc import ABC, abstractmethod
from typing import Any, Dict


class TunnelBase(ABC):
    @abstractmethod
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the tunnel with specific settings"""
        pass

    @abstractmethod
    def make_request(self, url: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """Make a request through the tunnel and return response data"""
        pass
