import logging
import socket
from typing import Dict

logging.basicConfig(level=logging.ERROR)

def port_scan(ip: str, port_list: list, timeout: int=1) -> Dict[int, str]:
    """
    Функция получает адрес ip, список портов и таймаут (по умолчанию 3 секунды) и
    возвращает список вида: ключ - номер порта, значение "open" или "close".
    Args:
        ip (str) - ip адрес в виде строки
        port_list (list) - список портов (порты (int))
        timeout (int) - таймаут
    Returns:
        Dict[str, str] - словарь пар ключ, значение вида ключ - номер порта, значение "open" или "close".
    Exceptions:
        Если список портов не список - return {}
        Если передан пустой список портов - return {}
        Есле не разрешен ip адрес - return {}
    """
    ports = {}
    if not isinstance(port_list, list):
        logging.error("Переданный список портов не список")
        return {}
    if len(port_list) == 0:
        logging.error("Передан пустой список портов")
        return {}
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(timeout)
            for port in port_list:
                if client.connect_ex((ip, port)) == 0:
                    ports[port] = "open"
                else:
                    ports[port] = "closed"
    except socket.gaierror as e:
        logging.error(f"Ошибка разрешения ip адреса {e}")
        return {}
    return ports


def main():

    result = port_scan("scanme.nmap.org", [22, 80, 443])
    print(result)
    result = port_scan("abc", [22, 80, 443])
    print(result)
    result = port_scan("scanme.nmap.org", [])
    print(result)
    result = port_scan("scanme.nmap.org", "abv")
    print(result)

if __name__ == "__main__":

    main()