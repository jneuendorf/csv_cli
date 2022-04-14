import unittest
from pathlib import Path

from core import Config, Engine, CsvEngine


TEST_FILE = 'core/tests/_test.csv'


class TestEngine(unittest.TestCase):

    def setUp(self) -> None:
        if Path(TEST_FILE).exists():
            Path(TEST_FILE).unlink()

    def test_csv_engine(self):
        config = Config({
            'engine': 'csv',
            'filename': TEST_FILE,
            'columns': [
                {'name': 'Pretty column name', 'type': 'str'},
                {'name': 'Numeric value', 'type': 'float'},
                {'name': 'Integer', 'type': 'int'},
            ]
        })
        engine = Engine.from_config(config)

        self.assertIsInstance(engine, CsvEngine)

        engine.write({
            'Pretty column name': 'a',
            'Numeric value': 1.1,
            'Integer': 1,
        })
        engine.write({
            'Pretty column name': 'b',
            'Numeric value': 2.2,
            'Integer': 2,
        })

        with open(TEST_FILE) as test_file:
            self.assertEqual(
                [line.strip() for line in test_file.readlines()],
                [
                    'Pretty column name,Numeric value,Integer',
                    'a,1.1,1',
                    'b,2.2,2',
                ],
            )

