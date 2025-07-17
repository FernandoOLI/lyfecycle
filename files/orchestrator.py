import os

from files.bash_generate import bash_generate
from files.polices_generator import polices_generator


def run():
    folder_path = "resources/"
    lines = ["#!/bin/bash\n"]
    create_folders()
    with open("output/bash/lifecycle.sh", "w") as f:
        f.writelines(line + "\n" for line in lines)

    for file_name in os.listdir(folder_path):
        # Generate Policies file
        polices_generator(file_name)
        # Generate Bash
        bash_generate(file_name)

def create_folders():
    os.makedirs("output/rules", exist_ok=True)
    os.makedirs("output/bash", exist_ok=True)