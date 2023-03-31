import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
configs_path = os.path.join(dir_path, "configs")
unit_testing_base_path = os.path.join(
    dir_path, "..", "tests", "temp")


class Config:
    def __init__(self):
        self.config_name = os.environ.get('RUN_ENV', "development")
        print(f"Using config '{self.config_name}'")
        config_path = os.path.join(configs_path, f"{self.config_name}.json")

        with open(config_path) as f:
            print(f"Opening config file '{self.config_name}'")
            data = json.load(f)

        self.config = data
        if self.config_name == "unit_test":
            self.change_paths()

    def dict(self):
        return self.config

    def change_paths(self):
        for key, value in self.config.items():
            if "path" in key.lower():
                folder = os.path.join(unit_testing_base_path, value)
                self.config[key] = folder


config = Config()
