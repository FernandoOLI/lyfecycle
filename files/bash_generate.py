from files import util


def bash_generate(file_name):
    bucket_name = util.open_config_file(file_name)['bucket_name']
    lines = [""]
    json_filename = f"../rules/{file_name.replace('_config', '_lifecycle')}"
    lines.append(f"echo Applying lifecycle to bucket: {bucket_name} \n")
    lines.append("SCRIPT_DIR='$(cd '$(dirname '${BASH_SOURCE[0]}')' && pwd)' \n")
    lines.append(f"JSON_FILE='$SCRIPT_DIR/{json_filename}'")
    lines.append("aws s3api put-bucket-lifecycle-configuration \\")
    lines.append(f"--bucket {bucket_name} \\")
    lines.append("--lifecycle-configuration file://$JSON_FILE")
    with open("output/bash/lifecycle.sh", "a") as f:
        f.writelines([line + "\n" for line in lines])