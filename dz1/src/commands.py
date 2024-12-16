import os

class CommandExecutor:
    def __init__(self, vfs_root, current_dir):
        """Инициализация исполнителя команд."""
        self.vfs_root = vfs_root
        self.current_dir = current_dir

    def execute(self, command):
        parts = command.split(maxsplit=1)
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "ls":
            return self.ls(arg)
        elif cmd == "cd":
            return self.cd(arg)
        elif cmd == "pwd":
            return self.pwd()
        elif cmd == "tail":
            return self.tail(arg)
        elif cmd == "exit":
            return "Exiting..."
        else:
            return f"Error: Unknown command '{command}'"

    def ls(self, directory=""):
        """Вывод содержимого текущей директории или указанной поддиректории."""
        try:
            base_path = os.path.join(self.vfs_root, self.current_dir.strip("/"))
            if directory:
                target_path = os.path.join(base_path, directory)
                if not os.path.exists(target_path):
                    return f"Error: '{directory}' does not exist."
                if os.path.isdir(target_path):
                    contents = os.listdir(target_path)
                    return "\n".join(contents) if contents else "No files or directories."
                return f"Error: '{directory}' is not a directory."
            else:
                contents = os.listdir(base_path)
                return "\n".join(contents) if contents else "No files or directories."
        except Exception as e:
            return f"Error accessing directory contents: {e}"

    def cd(self, new_dir):
        """Изменение текущей директории."""
        if not new_dir:
            return "Error: No directory specified."

        if new_dir == "..":
            if self.current_dir == "/":
                return "Error: Already at root directory."
            else:
                self.current_dir = os.path.dirname(self.current_dir.strip("/"))
                self.current_dir = "/" + self.current_dir if self.current_dir else "/"
                return None

        if new_dir == ".":
            return "Error: Already in the current directory."

        target_dir = os.path.join(self.vfs_root, self.current_dir.strip("/"), new_dir)
        target_dir = os.path.normpath(target_dir)

        if not os.path.exists(target_dir) or not os.path.isdir(target_dir):
            return f"Error: Directory '{new_dir}' does not exist."

        self.current_dir = os.path.relpath(target_dir, self.vfs_root)
        if not self.current_dir.startswith("/"):
            self.current_dir = "/" + self.current_dir
        return None

    def pwd(self):
        """Вывод текущей директории."""
        return self.current_dir

    def tail(self, file_name):
        """Вывод последних строк файла."""
        if not file_name:
            return "Error: No file name provided."

        file_path = os.path.join(self.vfs_root, self.current_dir.strip("/"), file_name)

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return f"Error: File '{file_name}' does not exist."

        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                return "".join(lines[-10:]) if lines else "File is empty."
        except Exception as e:
            return f"Error reading file '{file_name}': {e}"
