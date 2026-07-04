import platform
import os
import sys
import datetime
import psutil

def get_system_info():
    """Собирает базовую информацию о системе."""

    info = {
        "timestamp": datetime.datetime.now().isocalendar(),
        "python_version": sys.version,
        "os": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "hostname": platform.node(),
        "username": os.getenv("USER") or os.getenv("USERNAME") or "unknown",
        "cpu_count": psutil.cpu_count(),
        "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 2)
    }
    
    return info

def main():
    info = get_system_info()

    print("\n" + "="*50)
    print("SYSTEM INFORMATION")
    print("\n" + "="*50)
    for key, value in info.items():
        print(f"{key:20}: {value}")
    print("="*50 + "\n")

    log_file = f"sys_info_{info['hostname']}.log"
    with open(log_file, "a") as f:
        f.write(f"[{info['timestamp']}] System info collected\n")
        for key, value in info.items():
            f.write(f" {key}: {value}\n")
        f.write("-"*50 + "\n")
    
    print(f"[+] Log saved to: {log_file}")


if __name__ == "__main__":
    main()