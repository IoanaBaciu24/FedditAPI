import yaml
import os

class Config:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.data = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file '{self.config_path}' not found.")

        with open(self.config_path, 'r') as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise RuntimeError(f"Error parsing YAML file: {e}")

    def get(self, key, default=None):
        return self.data.get(key, default)

    def __getitem__(self, key):
        return self.data[key]

    def __repr__(self):
        return f"Config({self.config_path})"
