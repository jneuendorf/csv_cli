import argparse
from collections.abc import Sequence
from typing import Any

from .config import Config


class ArgParser:
    config: Config
    parser: argparse.ArgumentParser

    def __init__(self, config: Config):
        self.config = config
        self.parser = argparse.ArgumentParser(
            description='...',
        )

    @classmethod
    def from_config(cls, config: Config):
        parser = cls(config)
        parser.add_arguments()
        return parser

    def add_arguments(self):
        for column in self.config.columns:
            self.parser.add_argument(
                column['name'],
                type=self.config.get_column_type(column),
            )

    def parse_args(self, args: Sequence[str] = None) -> dict[str, Any]:
        return vars(self.parser.parse_args(args))
