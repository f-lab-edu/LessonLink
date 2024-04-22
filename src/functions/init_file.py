import configparser
import os


def get_init_config_data(section, option) -> str:

    config = configparser.ConfigParser()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '..', 'env.ini')

    config.read(config_path)

    return config.get(section, option)


def set_init_config_data(section, option, value) -> None:

    config = configparser.ConfigParser()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '..', 'env.ini')

    config.read(config_path)

    if not config.has_section(section):
        config.add_section(section)

    config.set(section, option, value)

    with open(config_path, 'w') as configfile:
        config.write(configfile)
