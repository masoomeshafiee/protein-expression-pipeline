import json
import os
import platform
import getpass
import socket
from datetime import datetime
import subprocess
import pkg_resources
import logging

def get_git_commit_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    except Exception:
        return "Not a Git repo or Git not available"

def get_installed_packages():
    return {pkg.key: pkg.version for pkg in pkg_resources.working_set}

def save_full_metadata(config, output_dir):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    protein_name = config["Path_settings"]["protein_name"]
    condition = config["Path_settings"]["condition"]
    metadata = {
        "timestamp": timestamp,
        "user": getpass.getuser(),
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
        "git_commit": get_git_commit_hash(),
        "config_used": config,
        "installed_packages": get_installed_packages()
    }

    filename = f"metadata_{protein_name}_{condition}_{timestamp}.json"
    metadata_path = os.path.join(output_dir, filename)

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    logging.info(f"Saved metadata to: {output_dir}")
