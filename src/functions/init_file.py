import configparser
import os


def get_init_config_data(section, option):

    config = configparser.ConfigParser()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '..', 'env.ini')

    config.read(config_path)

    return config.get(section, option)
