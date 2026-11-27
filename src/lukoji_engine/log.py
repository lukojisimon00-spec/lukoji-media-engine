"""Journalisation : console lisible + fichier JSON Lines (var/logs/engine.jsonl)."""
from __future__ import annotations

import json
import logging
import time
from pathlib import Path

_CONFIGURED = False
_RESERVED = set(logging.LogRecord("", 0, "", 0, "", None, None).__dict__) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created)) + "Z",
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        for k, v in record.__dict__.items():
            if k not in _RESERVED and not k.startswith("_"):
                payload[k] = v
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=str)


def setup_logging(level: str = "INFO", file: str | Path | None = None) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    root = logging.getLogger("lukoji")
    root.setLevel(level)
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter("%(levelname)-7s %(name)s · %(message)s"))
    root.addHandler(console)
    if file:
        Path(file).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(file, encoding="utf-8")
        fh.setFormatter(JsonFormatter())
        root.addHandler(fh)
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"lukoji.{name}")
