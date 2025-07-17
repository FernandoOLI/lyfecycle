import json


def open_config_file(file_name):
    with open(f"resources/{file_name}", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data
