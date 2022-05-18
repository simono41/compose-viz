from typing import List

from compose_viz.service import Service


class Compose:
    def __init__(self, services: List[Service]) -> None:
        self._services = services

    def extract_networks(self) -> List[str]:
        raise NotImplementedError

    @property
    def services(self):
        return self._services
