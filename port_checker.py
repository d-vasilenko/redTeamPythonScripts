"""
ТЗ
1. Напишите функцию, которая принимает IP-адрес и порт, и возвращает кортеж `(ip, port, status)`, где статус – строка `"open"` или `"closed"`. Используйте `socket.connect_ex()` для проверки.
2. Прочитайте файл `ips.txt` (каждый IP с новой строки) и для каждого IP проверьте порт 80, запишите открытые IP в файл `open_ips.txt`.
"""

import socket
# from datetime import datetime as dt

def read_ip_list_from_file(file: str) -> list:
    """Функция читает список ip адресов из файла"""
    ip_list = []
    try:
        with open(file, 'r', encoding="utf-8") as f:
            for line in f:
                ip_list.append(line.strip())
    except FileNotFoundError:
        print("Ошибка: Файл не найден!")
    except PermissionError:
        print("Ошибка: Нет прав для чтения файла!")
    except UnicodeDecodeError:
        print("Ошибка: Проблемма с кодировкой файла!")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
    return ip_list

def write_checked_ip(file: str, data: list) -> bool:
    """Функция записывает в файл хосты с открытым портом"""
    try:
        with open(file, 'w', encoding="utf-8") as f:
            f.writelines(f"{line}\n" for line in data)
        print(f"Данные проверки успешно записаны в файл {file}")
        return True
    except PermissionError:
        print("Нет прав для записи файла!")
    except IsADirectoryError:
        print("Путь являеться директорией!")
    except OSError as e:
        print(f"Ошибка ОС при записи в {file}: {e}")
    except UnicodeEncodeError as e:
        print(f"Ошибкаа кодировки: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
    
    return False

def check_port(host: str, port: int, timeout: int=3) -> tuple:
    """Функция проверяет хост на открытый порт"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(timeout)

        result = client.connect_ex((host, port))

        if result == 0:
            status = 'open'
        else:
            status = 'close'
    
    return (host, port, status)


def main():
    result_list = []
    ips = read_ip_list_from_file('ips.txt')

    for host in ips:
        line = check_port(host, 80)
        if line[2] == 'open':
            result_list.append(line)
        else:
            continue
    
    print(result_list)

    write_checked_ip("open_hosts.txt", result_list)    

if __name__ == "__main__":
    main()