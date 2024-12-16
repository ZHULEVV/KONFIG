import unittest
import tempfile
import os
from commands import CommandExecutor


class TestCommandExecutor(unittest.TestCase):
    def setUp(self):
        """Настройка тестового окружения."""
        # Создаем временную директорию для виртуальной файловой системы
        self.test_dir = tempfile.TemporaryDirectory()
        self.vfs_root = self.test_dir.name

        # Создаем тестовые файлы и директории
        os.makedirs(os.path.join(self.vfs_root, "dir1"))
        os.makedirs(os.path.join(self.vfs_root, "dir2"))
        with open(os.path.join(self.vfs_root, "file1.txt"), "w") as f:
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")
        with open(os.path.join(self.vfs_root, "file2.txt"), "w") as f:
            f.write("Line A\nLine B\nLine C\nLine D\nLine E\n")

        # Инициализируем CommandExecutor
        self.executor = CommandExecutor(self.vfs_root, "/")

    def tearDown(self):
        """Очистка тестового окружения."""
        self.test_dir.cleanup()

    # Тесты для команды ls
    def test_ls_root_directory(self):
        result = self.executor.execute("ls")
        self.assertIn("dir1", result)
        self.assertIn("file1.txt", result)

    def test_ls_nonexistent_directory(self):
        result = self.executor.execute("ls nonexistent_dir")
        self.assertIn("Error:", result)

    # Тесты для команды cd
    def test_cd_to_subdirectory(self):
        self.executor.execute("cd dir1")
        self.assertEqual(self.executor.pwd(), "/dir1")

    def test_cd_to_nonexistent_directory(self):
        result = self.executor.execute("cd nonexistent")
        self.assertIn("Error:", result)

    # Тесты для команды pwd
    def test_pwd_initial_directory(self):
        result = self.executor.execute("pwd")
        self.assertEqual(result, "/")

    def test_pwd_after_cd(self):
        self.executor.execute("cd dir1")
        result = self.executor.execute("pwd")
        self.assertEqual(result, "/dir1")

    # Тесты для команды tail
    def test_tail_existing_file(self):
        result = self.executor.execute("tail file1.txt")
        self.assertIn("Line 1", result)

    def test_tail_nonexistent_file(self):
        result = self.executor.execute("tail nonexistent.txt")
        self.assertIn("Error:", result)

    # Тесты для команды exit
    def test_exit_command(self):
        result = self.executor.execute("exit")
        self.assertEqual(result, "Exiting...")

    def test_unknown_command(self):
        result = self.executor.execute("unknown")
        self.assertIn("Error: Unknown command", result)


if __name__ == "__main__":
    unittest.main()
