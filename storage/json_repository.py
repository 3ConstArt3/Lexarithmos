# -*- coding: utf-8 -*-
import json

from pathlib import Path
from typing import Any, Dict
from core.exceptions import PhraseStorageError


class JsonRepository:

    """
    Handles low-level JSON file operations.
    """

    def __init__(self, file_path: str | Path) -> None:

        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, Any]:

        if not self.file_path.exists():
            return {}

        try:

            with self.file_path.open("r", encoding="utf-8") as file:
                return json.load(file)

        except (OSError, json.JSONDecodeError):
            return {}

    def save(self, data: Dict[str, Any]) -> None:

        temporary_path = self.file_path.with_suffix(
            self.file_path.suffix + ".tmp"
        )

        try:

            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            temporary_path.replace(self.file_path)

        except OSError as exc:
            raise PhraseStorageError(
                f"Failed to write JSON file '{self.file_path}': {exc}"
            ) from exc
