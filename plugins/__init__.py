import json
import os
from typing import List

from .base import TunnelBase
from .curl_impersonate import CurlImpersonateTunnel
from .residential import ResidentialTunnel
from .squid import SquidTunnel

TUNNELS = {
    "curl-impersonate": CurlImpersonateTunnel,
    "squid": SquidTunnel,
    "residential": ResidentialTunnel,
}


def load_tunnels() -> List[TunnelBase]:
    """Load tunnel configurations from config file or environment"""
    tunnel_configs = []

    # Try loading from config file first
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "configs", "tunnels.json"
    )
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                tunnel_configs = json.load(f).get("tunnels", [])
            print(f"Loaded tunnel configurations from {config_path}")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading config file {config_path}: {e}")

    tunnels = []
    for config in tunnel_configs:
        tunnel_type = config.pop("type", None)
        if tunnel_type in TUNNELS:
            tunnel_class = TUNNELS[tunnel_type]
            print(f"Creating tunnel of type '{tunnel_type}' with config: {config}")
            tunnels.append(tunnel_class(**config))
        else:
            print(f"Warning: Unknown tunnel type '{tunnel_type}'")

    if not tunnels:
        print("No valid tunnel configurations found")

    return tunnels
