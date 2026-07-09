"""
ТЗ
1. Напишите функцию, которая принимает IP-адрес и порт, и возвращает кортеж `(ip, port, status)`, где статус – строка `"open"` или `"closed"`. Используйте `socket.connect_ex()` для проверки.
2. Прочитайте файл `ips.txt` (каждый IP с новой строки) и для каждого IP проверьте порт 80, запишите открытые IP в файл `open_ips.txt`.
"""

import logging
import socket
from typing import Tuple

logging.basicConfig(level=logging.INFO)

def read_ip_list_from_file(file: str) -> list:
    """
    Функция читает список ip адресов из файла.

    Args:
        file (str): имя файла из которого читаем
    Returns:
        list: список IP адресов
    Raises:
        FileNotFoundError: Если файл не найден.
        PermissionError: Если нет прав для чтения файла.
        UnicodeDecodeError: Если проблемы с кодиравкой файла.
    """
    ip_list = []
    try:
        with open(file, 'r', encoding="utf-8") as f:
            for line in f:
                ip = line.strip()
                if ip:
                    ip_list.append(ip)
    except FileNotFoundError:
        logging.error("Ошибка: Файл не найден!")
        raise
    except PermissionError:
        logging.error("Ошибка: Нет прав для чтения файла!")
        raise
    except UnicodeDecodeError:
        logging.error("Ошибка: Проблемма с кодировкой файла!")
        raise
    # except Exception as e:
    #     logging.error(f"Неизвестная ошибка: {e}")
    #     raise
    return ip_list

def write_checked_ip(file: str, data: list) -> bool:
    """
    Функция записывает в файл хосты с открытым портом.

    Args: 
        file (str): имя файла, в который пишем найденные хосты.
        data (list): список хостов с открытым портом.
    Returns:
        bool: Произоша запись файла или нет.
    Raises:
        PermissionError: Если нет прав для записи файла.
        IsADirectoryError: Если путь являеться директорией.
        OSError: Если произошла ошибка при записи файла.
        UnicodeEncodeError: Если произошла ошибка кодировки.
    """
    try:
        with open(file, 'w', encoding="utf-8") as f:
            f.writelines(f"{line[0]}:{line[1]} {line[2]}\n" for line in data)
        print(f"Данные проверки успешно записаны в файл {file}")
        return True
    # except PermissionError:
    #     logging.error("Нет прав для записи файла!")
    # except IsADirectoryError:
    #     logging.error("Путь являеться директорией!")
    except OSError as e:
        logging.error(f"Ошибка ОС при записи в {file}: {e}")
        return False
    # except UnicodeEncodeError as e:
    #     logging.error(f"Ошибкаа кодировки: {e}")
    # except Exception as e:
    #     logging.error(f"Неожиданная ошибка: {e}")
    

def check_port(host: str, port: int, timeout: int=3) -> Tuple[str, int, str]:
    """
    Функция проверяет доступность TCP-порта на указанном хосте.

    Args:
        host (str): IP-адрес целевого хоста.
        port (int): Номер TCP-порта для проверки (например 80).
        timeout (int, optional): Время ожидания ответа в секундах, по умолчанию 3.
    Returns:
        Tuple[str, int, str]: Кортеж вида (host, port, status), где status может быть 'open', 'closed', 'invalid'.
    Raises:
        socket.gaierror: Если передан не валидный IP-адрес. 
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(timeout)

        try:
            result = client.connect_ex((host, port))
        except socket.gaierror as e:
            logging.error(f"Ошибка разрешения ip адреса {e}")
            return (host, port, 'invalid')

        if result == 0:
            status = 'open'
        else:
            status = 'closed'
    
    return (host, port, status)


def main():
    result_list = []
    ips = read_ip_list_from_file('ips.txt')

    for host in ips:
        line = check_port(host, 80)
        if line[2] == 'open':
            result_list.append(line)
    
    # logging.info(result_list)
    if result_list:
        print(f"[+] Найдено открытыв хостов: {len(result_list)}")
    else:
        print(f"[-] Открытых хостов не найдено.")

    write_checked_ip("open_hosts.txt", result_list)    

if __name__ == "__main__":
    
    # tests
    logging.disable(logging.CRITICAL)
    assert check_port("127.0.0.1", 22)[2] in ("open", "closed")
    assert check_port("abs", 80)[2] == "invalid"
    print("[v] Все тесты пройдены!")

    logging.disable(logging.NOTSET)
    main()
