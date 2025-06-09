import yaml
import os
from typing import Any, Optional, Dict


class Config:
    """
    A class to load and access configuration settings from a YAML file.

    Attributes:
        config_path (str): The path to the YAML configuration file.
        data (Dict[str, Any]): The parsed YAML content.
    """

    def __init__(self, config_path: str = "./config/config.yaml"):
        """
        Initializes the Config object and loads the configuration data.

        Args:
            config_path (str): The path to the YAML configuration file.
        """
        self.config_path: str = config_path
        self.data: Dict[str, Any] = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Loads and parses the YAML configuration file.

        Returns:
            Dict[str, Any]: Parsed configuration data.

        Raises:
            FileNotFoundError: If the file does not exist.
            RuntimeError: If the file contains invalid YAML.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file '{self.config_path}' not found.")

        with open(self.config_path, "r") as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise RuntimeError(f"Error parsing YAML file: {e}")

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """
        Gets the value associated with the key from the config.

        Args:
            key (str): The configuration key.
            default (Optional[Any]): The default value to return if the key is not found.

        Returns:
            Optional[Any]: The value for the key, or the default if not found.
        """
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """
        Enables dict-style access to the configuration values.

        Args:
            key (str): The configuration key.

        Returns:
            Any: The value for the key.
        """
        return self.data[key]

    def __repr__(self) -> str:
        """
        Returns a string representation of the Config object.
        """
        return f"Config({self.config_path})"
