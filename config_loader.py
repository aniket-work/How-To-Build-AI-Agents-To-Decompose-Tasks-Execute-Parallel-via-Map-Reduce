import os
import yaml
from pathlib import Path
from dotenv import load_dotenv


class ConfigLoader:
    @staticmethod
    def load_config():
        load_dotenv()

        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)

        with open('prompts.yaml', 'r') as f:
            prompts = yaml.safe_load(f)

        return config, prompts