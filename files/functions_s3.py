import subprocess
import re
from collections import defaultdict
import boto3


def s3_prefix_exists(bucket: str, prefix: str) -> bool:
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=1)
    return "Contents" in response


def get_paths_list_s3(bucket: str, prefix: str) -> list:
    lines= s3_prefix_exists(bucket, prefix)
    if not lines or lines == ['']:
        print(f"[ERROR] No objects found in s3://{bucket}/{prefix}")
        return []
    cmd = ["aws", "s3", "ls", f"s3://{bucket}/{prefix}", "--recursive"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip().split("\n")


def get_valid_lifecycle_paths(bucket: str, prefix: str) -> list:
    try:
        lines = get_paths_list_s3(bucket, prefix)

        structure = defaultdict(set)

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 4:
                continue
            key = parts[3]
            path_parts = key.split("/")[:-1]

            if "_delta_log" in path_parts:
                base = "/".join(path_parts[:-1])
                structure[base].add("_delta_log")
            elif any(re.fullmatch(r"year=\d{4}", part) for part in path_parts):
                base = "/".join(path_parts[:-1])
                structure[base].add("year")

        valid_paths = []
        for base_path, tags in structure.items():
            delta_path = f"{base_path}/_delta_log/"
            year_path = f"{base_path}/year="

            if "_delta_log" in tags and "year" in tags:
                if s3_prefix_exists(bucket, delta_path) and s3_prefix_exists(bucket, year_path):
                    valid_paths.append(f"{base_path}")

        valid_paths = sorted(set(valid_paths))

        if valid_paths:
            print(f"[INFO] Found {len(valid_paths)} valid lifecycle {bucket} path(s).")
        else:
            print(f"[INFO] No valid lifecycle {bucket} paths found. Ensure both '_delta_log' and 'year=YYYY' folders exist.")

        return valid_paths

    except subprocess.CalledProcessError as e:
        print("[ERROR] AWS CLI command execution failed.")
        print("Command:", e.cmd)
        print("Output:", e.output)
        raise
