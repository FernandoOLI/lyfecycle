import subprocess

def get_relevant_s3_folders(bucket: str, prefix: str = "data/") -> list:
    try:
        # Run AWS CLI command to list objects recursively
        cmd = [
            "aws", "s3", "ls", f"s3://{bucket}/{prefix}", "--recursive"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        lines = result.stdout.strip().split("\n")
        folders = set()

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 4:
                continue
            key = parts[3]
            if "/" not in key:
                continue
            path_parts = key.split("/")[:-1]  # exclude file name
            if path_parts:
                folder_path = "/".join(path_parts) + "/"
                if "_delta_log/" in folder_path or any("year=" in part for part in path_parts):
                    folders.add(f"s3://{bucket}/{folder_path}")

        return sorted(folders)

    except subprocess.CalledProcessError as e:
        print("Error executing AWS CLI:", e.stderr)
        return []

# Example usage
folders = get_relevant_s3_folders("lyfecycle-management-bucket")
for folder in folders:
    print(folder)
