import configparser


class Config(object):
    cfg = None

    @staticmethod
    def get_cfg():
        if Config.cfg is None:
            Config.cfg = configparser.ConfigParser()
            Config.cfg.read("config.ini")
        return Config.cfg
