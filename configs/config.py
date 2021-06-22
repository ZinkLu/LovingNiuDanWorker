import json
from pathlib import Path

CONFIG_FILE = Path('configs', 'config.json')
CONFIG_JSON = json.load(CONFIG_FILE.open())

NULL_CONFIG = {'desc': "", "value": ""}


class Config:
    @classmethod
    def get_config(key, default=None):
        return CONFIG_JSON.get(key, NULL_CONFIG).get("value", default)

    @classmethod
    def set_config(key, value):
        CONFIG_JSON[key]['value'] = value
        json.dump(CONFIG_FILE.open('w'))

    @classmethod
    def flush_config(config):
        global CONFIG_JSON
        CONFIG_JSON = config
        json.dump(CONFIG_FILE.open('w'))
