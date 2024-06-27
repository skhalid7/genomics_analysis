import json
import ast

def get_config_parameter(parameter_name, config_file_path = "config.json"):
    try:
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
            if parameter_name in config_data:
                return config_data[parameter_name]
            else:
                raise KeyError(f"{parameter_name} not found in config.json")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"{config_file_path} not found")
