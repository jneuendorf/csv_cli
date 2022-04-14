import json
from collections.abc import Callable
from pathlib import Path
from typing import TypedDict, Literal, Any


class ColumnDict(TypedDict):
    name: str
    type: Literal['str', 'int', 'float']


class ConfigDict(TypedDict):
    engine: Literal['csv', 'json']
    filename: str
    columns: list[ColumnDict]


class Config:
    _config: ConfigDict

    def __init__(self, config: ConfigDict = None):
        if config is None:
            with open(Path('config.json')) as f:
                config = json.load(f)
        else:
            config = config
        self._config = config
        self.clean()

    def __str__(self):
        return json.dumps(self._config, indent=4)

    def clean(self):
        if 'filename' not in self._config:
            raise ValueError('config is missing "filename"')

        if self._config['engine'] not in ['csv', 'json']:
            raise ValueError(f'invalid config: invalid engine "{self._config["engine"]}"')

        if 'columns' not in self._config:
            self._config['columns'] = []
        for column in self._config['columns']:
            if column['type'] not in ['str', 'int', 'float']:
                raise ValueError(f'invalid column type "{column["type"]}"')

    @property
    def engine(self) -> str:
        return self._config['engine']

    @property
    def filename(self) -> str:
        return self._config['filename']

    @property
    def columns(self) -> list[ColumnDict]:
        return self._config['columns']

    @property
    def column_names(self) -> list[str]:
        return [col['name'] for col in self.columns]

    @staticmethod
    def get_column_type(column: ColumnDict) -> Callable[[str], Any]:
        col_type = column['type']
        if col_type == 'str':
            return str
        elif col_type == 'int':
            return int
        elif col_type == 'float':
            return float
        else:
            raise ValueError(f'invalid column type "{col_type}"')
