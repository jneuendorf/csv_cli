from core import Config, ArgParser, Engine

if __name__ == '__main__':
    config = Config()
    parser = ArgParser.from_config(config)
    engine = Engine.from_config(config)
    record = parser.parse_args()
    # print('parsed args:', record)
    engine.write(record)

