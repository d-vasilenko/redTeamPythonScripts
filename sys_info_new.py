import os
import platform
import importlib.metadata as metadata
from typing import Dict

def get_pip_info() -> dict:
    pip_list = [
        f"{dist.metadata['Name']}=={dist.metadata['Version']}" for dist in metadata.distributions()
    ]
    return sorted(pip_list)

def view_pip_install_list(pip_list: list) -> bool:
    for item in pip_list:
        name, version = item.split('==')[0], item.split('==')[1]
        print(f"{name:20} Versin: {version}")
    return True

def view_info(info_dict: dict) -> bool:
    print("=" * 10, "System Info", "=" * 10)
    for key in info_dict:
        if isinstance(info_dict[key], list):
            print("=" * 11, "Pip List", "=" * 11)
            view_pip_install_list(info_dict[key])
        else:
            print(f"{key:20} {info_dict[key]}")
    print("=" * 40)
    return True

def get_system_info() -> dict:
    info = {
        "python_version": platform.python_version(),
        "system_name": platform.system(),
        "current_user": os.getenv("USER") or os.getenv("USERNAME") or os.getenv("LOGNAME") or "unknown",
        "pip_list": get_pip_info()
    }
    return info

def main():

    view_info(get_system_info())

    
if __name__ == "__main__":

    main()
