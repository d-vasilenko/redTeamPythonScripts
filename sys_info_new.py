import os
import platform
import importlib.metadata as metadata
from typing import Dict

def get_pip_info() -> Dict[str, str]:
    """
    Функция возвращает словарь, ключи имена установленных pip пакетов, значения - версии.
    Args:
    Returns:
        dict(str: str) - результирующий словарь.
    Exeptions:

    """
    packages = {}
    try:
        for item in metadata.distributions():
            packages[f"{item.metadata['Name']}"] = item.metadata['Version']
        return packages
    except Exception as e:
        print(f"Error: {e}")
        return {}


def print_pip_install_list(pip_list: dict) -> bool:
    """
    Функция которая выводит в консоль установленные pip пакеты.
    Args:
        dict - словарь ключи - имена пакетов, значения - версии
    Returns:
        bool(True) - если ввывод успешный
        bool(False) - если вывод не успешный
    """
    if not pip_list:
        print("  (No packages installed)")
        return False
    try:
        for key in pip_list:
            print(f"{key:20} {pip_list[key]}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def print_info(info_dict: dict) -> bool:
    """
    Функция выводит информацию о системе в консоль.
    Args:
        dict - словарь с полями - информацией о системе, ключ - имя пареметра, значение - значение.
    Returns:
        bool(True) - при нормальном выводе
        bool(False) - при возникновении ошибки
    """
    try:
        print("=" * 10, "System Info", "=" * 10)
        for key in info_dict:
            if isinstance(info_dict[key], dict):
                print("=" * 11, "Pip List", "=" * 11)
                print_pip_install_list(info_dict[key])
            else:
                print(f"{key:20} {info_dict[key]}")
        print("=" * 40)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_system_info() -> dict:
    """
    Функция создает и возвращает объект и информацией о системе.
    ключи - значения.
    Args:
    Returns:
        dict - объект с информацией о системе.
    """
    
    info = {
        "python_version": platform.python_version(),
        "system_name": platform.system(),
        "current_user": os.getenv("USER") or os.getenv("USERNAME") or os.getenv("LOGNAME") or "unknown",
        "pip_list": get_pip_info()
    }
    return info

def main():

    system_info = get_system_info()

    print_info(system_info)
    
if __name__ == "__main__":

    main()
