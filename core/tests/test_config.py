import unittest

from core import Config, ArgParser


class TestConfig(unittest.TestCase):

    def test_config(self):
        config = Config({
            'engine': 'csv',
            'filename': 'test',
            'columns': [
                {'name': 'Pretty column name', 'type': 'str'},
                {'name': 'Numeric value 1', 'type': 'float'},
                {'name': 'Numeric value 2', 'type': 'float'},
                {'name': 'Integer', 'type': 'int'},
            ]
        })

        self.assertEqual(config.engine, 'csv')

    def test_invalid_config(self):
        with self.assertRaises(ValueError):
            Config({
                'engine': 'csv',
                'columns': [
                    {'name': 'Pretty column name', 'type': 'str'},
                    {'name': 'Numeric value 1', 'type': 'float'},
                    {'name': 'Numeric value 2', 'type': 'float'},
                    {'name': 'Integer', 'type': 'int'},
                ]
            })
