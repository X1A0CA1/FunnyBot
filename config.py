import yaml


class Config:
    def __init__(self, filename='config.yml'):
        self.filename = filename

        self.API_ID = None
        self.API_HASH = None
        self.BOT_NAME = None
        self.BOT_USERNAME = None
        self.BOT_TOKEN = None
        self.TIME_ZONE = None

        self.load_config()
        self._check_required_configs()

    def load_config(self):
        try:
            with open(self.filename, 'r') as config_file:
                config_data = yaml.safe_load(config_file)

            self.API_ID = config_data.get('api_id', None)
            self.API_HASH = config_data.get('api_hash', None)
            self.BOT_NAME = config_data.get('bot_name', None)
            self.BOT_USERNAME = config_data.get('bot_username', None)
            self.BOT_TOKEN = config_data.get('bot_token', None)
            self.TIME_ZONE = config_data.get('time_zone', 'Asia/Shanghai')

        except FileNotFoundError:
            raise FileNotFoundError("配置文件不存在")
        except yaml.YAMLError:
            raise yaml.YAMLError("配置文件格式错误")
        except KeyError:
            raise KeyError("配置文件缺少关键配置项")
        except Exception as e:
            raise e

    def _check_required_configs(self):
        required_configs = [
            ('api_id', self.API_ID),
            ('api_hash', self.API_HASH),
            ('bot_name', self.BOT_NAME),
            ('bot_username', self.BOT_USERNAME),
            ('bot_token', self.BOT_TOKEN),
        ]

        missing_configs = [name for name, value in required_configs if value is None]

        if missing_configs:
            raise KeyError(f"配置文件缺少关键配置项: {', '.join(missing_configs)}")


config = Config()
