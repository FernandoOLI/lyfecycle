import os

def bash_generate():
    print()
    paths = os.listdir("output/rules")
    for path in paths:
        bash_command_generate(path)


def bash_command_generate(file_name):
    bucket_name = file_name.replace(".json","")
    json_filename = f"../rules/{file_name}"
    lines = []
    lines.append(f"echo Applying lifecycle to bucket: {bucket_name}")
    lines.append('SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"')
    lines.append(f'JSON_FILE="$SCRIPT_DIR/{json_filename}"')
    lines.append("aws s3api put-bucket-lifecycle-configuration \\")
    lines.append(f"  --bucket {bucket_name} \\")
    lines.append("  --lifecycle-configuration file://$JSON_FILE")
    with open("output/bash/lifecycle.sh", "a") as f:
        f.write("\n")
        for line in lines:
            f.write(line + "\n")