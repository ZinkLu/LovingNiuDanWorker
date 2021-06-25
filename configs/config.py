import json
from pathlib import Path
from threading import Lock

LOCK = Lock()

CONFIG_FILE = Path('configs', 'config.json')
CONFIG_JSON = json.load(CONFIG_FILE.open())  # type: dict

NULL_CONFIG = {'desc': "", "value": ""}


def with_lock(fn):

    def w(*args, **kwargs):
        return fn(*args, **kwargs)

    return w


class Config:

    @classmethod
    @with_lock
    def get_config(cls, key, default=None):
        return CONFIG_JSON.get(key, NULL_CONFIG).get("value", default)

    @classmethod
    @with_lock
    def set_config(cls, key, value):
        CONFIG_JSON[key]['value'] = value
        json.dump(CONFIG_JSON, CONFIG_FILE.open('w'), ensure_ascii=False, indent=2)

    @classmethod
    @with_lock
    def flush_config(cls, config):
        global CONFIG_JSON
        CONFIG_JSON = config
        json.dump(CONFIG_JSON, CONFIG_FILE.open('w'), ensure_ascii=False, indent=2)

    @classmethod
    @with_lock
    def iter_config(cls):
        return CONFIG_JSON.items()
