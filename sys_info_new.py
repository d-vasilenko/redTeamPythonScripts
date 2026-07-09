import os
import platform
import importlib.metadata as metadata
from typing import Dict

def get_pip_info() -> dict:
    pips_dict = {}
    try:
        for item in metadata.distributions():
            pips_dict[f"{item.metadata['Name']}"] = item.metadata['Version']
        return pips_dict
    except Exception as e:
        print(f"Error: {e}")
        return {}


def view_pip_install_list(pip_list: dict) -> bool:
    try:
        for key in pip_list:
            print(f"{key:20} {pip_list[key]}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def view_info(info_dict: dict) -> bool:
    try:
        print("=" * 10, "System Info", "=" * 10)
        for key in info_dict:
            if isinstance(info_dict[key], dict):
                print("=" * 11, "Pip List", "=" * 11)
                view_pip_install_list(get_pip_info())
            else:
                print(f"{key:20} {info_dict[key]}")
        print("=" * 40)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_system_info() -> dict:
    
    info = {
        "python_version": platform.python_version(),
        "system_name": platform.system(),
        "current_user": os.getenv("USER") or os.getenv("USERNAME") or os.getenv("LOGNAME") or "unknown",
        "pip_list": get_pip_info()
    }
    return info

def main():

    state = get_system_info()

    view_info(state)
    
if __name__ == "__main__":

    main()
