import platform
import random
from abc import ABC, abstractmethod
import requests
from typing import Optional, List

class IPRotator(ABC):
    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        pass

    @abstractmethod
    def get_current_ip(self) -> str:
        pass

class VPNRotator(IPRotator):
    def __init__(self, provider: str, credentials: dict):
        self.provider = provider
        self.credentials = credentials
        self.os_type = platform.system().lower()

    def connect(self) -> bool:
        try:
            if self.provider == "njord" and self.os_type == "darwin":
                import njord
                self.client = njord.Client(
                        user=self.credentials.get("username"),
                        password=self.credentials.get("password")
                )
                self.client.connect()
            elif self.provider == "openvpn":
                pass
            return True
        except Exception as e:
            print(f"VPN connection failed: {str(e)}")
            return False

    def disconnect(self) -> bool:
        try:
            if self.provider == "njord" and self.os_type == "darwin":
                self.client.disconnect()
            elif self.provider == "openvpn":
                pass
            return True
        except Exception as e:
            print(f"VPN disconnection failed: {str(e)}")
            return False

    def get_current_ip(self) -> str:
        try:
            response = requests.get('https://api.ipify.org?format=json')
            return response.json()['ip']
        except Exception:
            return ""

class ProxyRotator(IPRotator):
    def __init__(self, proxies: List[dict]):
        """
        {
            'http': 'http://user:pass@host:port',
            'https': 'https://user:pass@host:port'
        }
        """
        self.proxies = proxies
        self.current_proxy = None

    def connect(self) -> bool:
        if not self.proxies:
            return False
        self.current_proxy = random.choice(self.proxies)
        return True

    def disconnect(self) -> bool:
        self.current_proxy = None
        return True

    def get_current_ip(self) -> str:
        if not self.current_proxy:
            return ""
        try:
            response = requests.get(
                    'https://api.ipify.org?format=json',
                    proxies=self.current_proxy
            )
            return response.json()['ip']
        except Exception:
            return ""

def create_ip_rotator(config: dict) -> IPRotator:
    rotator_type = config.get("type", "proxy").lower()

    if rotator_type == "vpn":
        return VPNRotator(
                provider=config.get("provider"),
                credentials=config.get("credentials", {})
        )
    else:
        return ProxyRotator(proxies=config.get("proxies", []))