from core import Config, ArgParser

if __name__ == '__main__':
    parser = ArgParser(Config())
    parser.add_arguments()
    args = parser.parse_args(['asdf', '1', '2.0', '1'])
