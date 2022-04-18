import csv
from abc import ABC, abstractmethod
from datetime import datetime, date
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

    def get_filename(self) -> str:
        return datetime.now().strftime(self.config.filename)

    def fill_eval_columns(self, record: dict[str, Any]) -> dict[str, Any]:
        eval_columns = [col for col in self.config.columns if col.eval]
        return {
            **record,
            **{
                col.name: eval(
                    col.eval,
                    globals(),
                    {'r': dict(record), 'datetime': datetime, 'date': date},
                )
                for col in eval_columns
            },
        }

    def write(self, record: dict[str, Any]) -> None:
        path = Path(self.get_filename()).resolve()
        return self._write(
            record=self.fill_eval_columns(record),
            path=path,
        )

    @abstractmethod
    def _write(self, record: dict[str, Any], path: Path) -> None:
        ...


class CsvEngine(Engine):

    def _write(self, record: dict[str, Any], path: Path):
        if path.exists():
            with path.open(mode='a') as file:
                writer = csv.DictWriter(file, fieldnames=self.config.column_names)
                writer.writerow(record)
        else:
            with path.open(mode='w') as file:
                writer = csv.DictWriter(file, fieldnames=self.config.column_names)
                writer.writeheader()
                writer.writerow(record)
