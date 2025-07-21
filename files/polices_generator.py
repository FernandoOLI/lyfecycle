import json

from files.functions_s3 import get_valid_lifecycle_paths


def polices_generator(data):
    paths = get_valid_lifecycle_paths(data["name"], data["prefix"])

    if not paths or paths == ['']:
        return

    default_rule = {
        "ID": "Default-Transition-Policy",
        "Filter": {
            "Prefix": data["prefix"]
        },
        "Status": "Enabled",
        "Transitions": [
            {
                "Days": data["days_to_glacier"],
                "StorageClass": "GLACIER"
            },
            {
                "Days": data["days_to_deep_archive"],
                "StorageClass": "DEEP_ARCHIVE"
            }
        ],
        "Expiration": {
            "Days": data["days_to_expiration"]
        }
    }

    rules = ignore_delta_log(paths)

    rules.append(default_rule)

    lifecycle_config = {
        "Rules": rules
    }
    save_file(lifecycle_config, data["name"])

def get_custom_folder_name(s3_path: str) -> str:
    parts = s3_path.replace("s3://", "", 1).split("/")
    return "-".join(parts[1:])


def ignore_delta_log(paths):
    rules = []

    for path in filter(None, paths):
        last_folder = get_custom_folder_name(path)
        rules.append({
            "ID": f"ExcludeDeltaLog-{last_folder}",
            "Filter": {
                "Prefix": f"{path}/_delta_log/"
            },
            "Status": "Enabled",
            "Expiration": {
                "Days": 9999
            }
        })

    return rules


def save_file(lifecycle_config, file_name):
    with open(f"output/rules/{file_name}.json", "w") as f:
        json.dump(lifecycle_config, f, indent=2)
