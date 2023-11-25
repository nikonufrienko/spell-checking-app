import configparser


class Settings:
    def __init__(self, file_path):
        config = configparser.ConfigParser()
        config.read(file_path)
        self.device = config['DEFAULT']['device']
        self.model = config['DEFAULT']['model']
        self.hotkey = config['DEFAULT']['capture_hotkey']
        self.max_time = config['DEFAULT']['max_time']