import configparser
import os


def get_init_config_data(section, option):

    config = configparser.ConfigParser()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '..', 'env.ini')

    config.read(config_path)

    return config.get(section, option)


def set_init_config_data(section, option, value):

    config = configparser.ConfigParser()

    # 파일 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '..', 'env.ini')

    # 기존 설정 파일 읽기
    config.read(config_path)

    # section이 존재하지 않으면 추가
    if not config.has_section(section):
        config.add_section(section)

    # 옵션 설정 (새로운 값으로)
    config.set(section, option, value)

    # 변경된 내용을 파일에 다시 쓰기
    with open(config_path, 'w') as configfile:
        config.write(configfile)
