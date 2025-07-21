import json
import os

from files.bash_generate import bash_generate
from files.polices_generator import polices_generator


def run():
    folder_path = "resources/data_config.json"
    lines = ["#!/bin/bash\n"]
    create_folders()
    with open("output/bash/lifecycle.sh", "w") as f:
        f.writelines(line + "\n" for line in lines)

    with open(folder_path, "r") as f:
        data = json.load(f)
    for item in data:
        # Generate Policies file
        polices_generator(item)
    # Generate Bash
    bash_generate()

def create_folders():
    os.makedirs("output/rules", exist_ok=True)
    os.makedirs("output/bash", exist_ok=True)