import csv
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from .config import Config


# TODO: support json lines?
class Engine(ABC):
    config: Config

    def __init__(self, config: Config):
        self.config = config

    @classmethod
    def from_config(cls, config: Config):
        engine = config.engine
        if engine == 'csv':
            return CsvEngine(config)
        elif engine == 'json':
            # TODO
            return None
        else:
            raise ValueError(f'invalid engine "{engine}"')

    @abstractmethod
    def write(self, record: dict[str, Any]) -> None:
        ...


class CsvEngine(Engine):

    def write(self, record: dict[str, Any]):
        path = Path(self.config.filename).resolve()
        if path.exists():
            with path.open(mode='a') as file:
                writer = csv.DictWriter(file, fieldnames=self.config.column_names)
                writer.writerow(record)
        else:
            with path.open(mode='w') as file:
                writer = csv.DictWriter(file, fieldnames=self.config.column_names)
                writer.writeheader()
                writer.writerow(record)
