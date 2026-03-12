from __future__ import annotations

import logging
from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class ApiClient:
    base_url: str
    token: str | None = None

    def __post_init__(self) -> None:  # type: ignore[override]
        self._log = logging.getLogger(self.__class__.__name__)

    @property
    def headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def get(self, path: str, **kwargs):
        return requests.get(f"{self.base_url}{path}", headers=self.headers, timeout=30, **kwargs)

    def post(self, path: str, json: dict | None = None, **kwargs):
        return requests.post(
            f"{self.base_url}{path}", headers=self.headers, json=json, timeout=30, **kwargs
        )

