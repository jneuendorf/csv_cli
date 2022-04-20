import unittest

from core import Config, ArgParser


class TestArgParser(unittest.TestCase):

    def test_cli_arg_generator(self):
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

        parser = ArgParser.from_config(config)
        args = parser.parse_args(['asdf', '1', '2.0', '1'])

        self.assertEqual(args, {
            'Pretty column name': 'asdf',
            'Numeric value 1': 1.0,
            'Numeric value 2': 2.0,
            'Integer': 1,
        })
        self.assertIsInstance(args['Numeric value 1'], float)
        self.assertIsInstance(args['Numeric value 2'], float)
        self.assertIsInstance(args['Integer'], int)
