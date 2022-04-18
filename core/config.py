import json
from collections.abc import Callable
from pathlib import Path
from typing import TypedDict, Literal, Any


class ColumnDict(TypedDict):
    name: str
    type: Literal['str', 'int', 'float']
    eval: str


class ConfigDict(TypedDict):
    engine: Literal['csv', 'json']
    filename: str
    columns: list[ColumnDict]


class Column:
    name: str
    type: Literal['str', 'int', 'float']
    eval: str | None

    def __init__(self, column_dict: ColumnDict):
        self.name = column_dict['name']
        self.type = column_dict['type']
        if 'eval' not in column_dict or column_dict['eval'] is None:
            self.eval = None
        else:
            self.eval = column_dict['eval']

    def __repr__(self):
        return f'<Column name={self.name} type={self.type} eval={self.eval}>'


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
    def columns(self) -> list[Column]:
        return [Column(col) for col in self._config['columns']]

    @property
    def column_names(self) -> list[str]:
        return [col.name for col in self.columns]

    @staticmethod
    def get_column_type(column: Column) -> Callable[[str], Any]:
        if column.type == 'str':
            return str
        elif column.type == 'int':
            return int
        elif column.type == 'float':
            return float
        else:
            raise ValueError(f'invalid column type "{column.type}"')
