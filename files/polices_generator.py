import json

from files import util


def polices_generator(file_name):
    data = util.open_config_file(file_name)

    default_rule = {
        "ID": "Default-Transition-Policy",
        "Filter": {
            "Prefix": "data"
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

    rules = ignore_delta_log(data)

    rules.append(default_rule)

    lifecycle_config = {
        "Rules": rules
    }
    save_file(lifecycle_config, file_name)


def ignore_delta_log(data):
    rules = []

    for path in data["paths"]:
        last_folder = path.strip("/").split("/")[-1]
        rules.append({
            "ID": f"ExcludeDeltaLog-{last_folder}",
            "Filter": {
                "Prefix": f"{path.rstrip('/')}/_delta_log/"
            },
            "Status": "Enabled"
        })

    return rules


def save_file(lifecycle_config, file_name):
    with open(f"output/rules/{file_name.replace('_config', '_lifecycle')}", "w") as f:
        json.dump(lifecycle_config, f, indent=2)
