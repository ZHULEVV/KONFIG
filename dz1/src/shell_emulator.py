import zipfile
from pathlib import Path
import csv
import argparse
from commands import CommandExecutor


class ShellEmulator:
    def __init__(self, username, hostname, vfs_path, log_path):
        self.username = username
        self.hostname = hostname
        self.vfs_path = Path(vfs_path).resolve()  # Корень VFS
        self.log_path = Path(log_path).resolve()  # Путь до файла логов
        self.current_dir = "/"  # Начальная директория
        self.executor = CommandExecutor(str(self.vfs_path), self.current_dir)

    def log_action(self, command):
        """Логирование команды в CSV файл."""
        try:
            with open(self.log_path, mode="a", newline="") as log_file:
                writer = csv.writer(log_file)
                writer.writerow([self.username, command])
        except Exception as e:
            print(f"Error logging command: {e}")

    def start(self):
        """Запуск эмулятора shell."""
        print(f"Welcome to the shell emulator, {self.username} on {self.hostname}!")
        while True:
            try:
                # Показываем приглашение для ввода с текущей директорией
                print(f"{self.username}@{self.hostname}:{self.current_dir}$ ", end="")
                command = input().strip()

                # Логируем команду
                self.log_action(command)

                # Обработка команды "exit"
                if command == "exit":
                    print("Exiting shell emulator.")
                    break

                # Выполняем команду
                output = self.executor.execute(command)

                # Выводим результат команды
                if output:
                    print(output)

                # Синхронизируем текущую директорию
                self.current_dir = self.executor.current_dir

            except Exception as e:
                print(f"Error: {e}")


def extract_vfs(vfs_path, extract_to="vfs"):
    """Распаковка виртуальной файловой системы."""
    try:
        with zipfile.ZipFile(vfs_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        return Path(extract_to).resolve()
    except zipfile.BadZipFile:
        raise ValueError(f"Error: '{vfs_path}' is not a valid ZIP file.")
    except FileNotFoundError:
        raise ValueError(f"Error: File '{vfs_path}' not found.")
    except Exception as e:
        raise ValueError(f"Error extracting VFS: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--username", required=True, help="Username for the shell prompt")
    parser.add_argument("--hostname", required=True, help="Hostname for the shell prompt")
    parser.add_argument("--vfs", required=True, help="Path to the virtual file system (ZIP file)")
    parser.add_argument("--log", required=True, help="Path to the log file (CSV format)")

    args = parser.parse_args()

    try:
        # Проверяем, существует ли лог-файл и создаем его, если он отсутствует
        log_path = Path(args.log).resolve()
        if not log_path.exists():
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.touch()

        # Распаковываем VFS
        vfs_root = extract_vfs(args.vfs)

        # Запускаем эмулятор
        emulator = ShellEmulator(args.username, args.hostname, vfs_root, log_path)
        emulator.start()
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Critical error: {e}")
