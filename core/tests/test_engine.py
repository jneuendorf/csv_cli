import unittest
from datetime import date
from pathlib import Path

from core import Config, Engine, CsvEngine

TEST_FILE = 'core/tests/_test.csv'
TEST_FILE_DATETIME = 'core/tests/_%Y.csv'


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

    def test_eval_column(self):
        config = Config({
            'engine': 'csv',
            'filename': TEST_FILE,
            'columns': [
                {'name': 'A', 'type': 'str'},
                {'name': 'B', 'type': 'int', 'eval': 'r["D"] * 2'},
                {'name': 'C', 'type': 'str', 'eval': 'date.today()'},
                {'name': 'D', 'type': 'int'},
            ]
        })
        engine = Engine.from_config(config)
        engine.write({
            'A': 'a',
            'D': 3,
        })

        with open(TEST_FILE) as test_file:
            self.assertEqual(
                [line.strip() for line in test_file.readlines()],
                [
                    'A,B,C,D',
                    f'a,6,{date.today()},3',
                ],
            )

    def test_datetime_filename(self):
        config = Config({
            'engine': 'csv',
            'filename': TEST_FILE_DATETIME,
            'columns': [
                {'name': 'A', 'type': 'str'},
            ]
        })
        engine = Engine.from_config(config)
        engine.write({'A': 'a'})

        self.assertTrue(
            Path(TEST_FILE_DATETIME)
                .with_name(f'_{date.today().year}.csv')
                .exists()
        )
