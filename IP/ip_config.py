DEFAULT_CONFIG = {
        "type": "proxy",  # or "vpn"
        "provider": "proxy",  # or "njord", "openvpn"
        "credentials": {
                "username": "",
                "password": ""
        },
        "proxies": [
                {
                        "http": "http://proxy1.example.com:8080",
                        "https": "https://proxy1.example.com:8080"
                },
                # Add more proxy servers here
        ]
}

def load_config() -> dict:
    return DEFAULT_CONFIG