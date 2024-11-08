### Задача 1
На сайте https://onlywei.github.io/explain-git-with-d3 или http://git-school.github.io/visualizing-git/ (цвета могут отличаться, есть команды undo/redo) с помощью команд эмулятора git получить следующее состояние проекта (сливаем master с first, перебазируем second на master): см. картинку ниже. Прислать свою картинку.
![alt text](![image](https://github.com/user-attachments/assets/4b85fdaf-feac-44b3-9fb3-a9cc07a51c62)

```bash
git commit
git tag in
git branch first
git branch second
git commit
git commit
git checkout first
git commit
git commit
git checkout master
git merge first
git checkout second
git commit
git commit
git rebase master
git checkout master
git merge second
git checkout in
```


### Задача 2
```bash
# Инициализация локального репозитория
git init my_project
cd my_project

# Установка имени и почты для первого пользователя (coder1)
git config user.name "Coder 1"
git config user.email "coder1@corp.com"

# Создание файла prog.py с какими-то данными
nano prog.py
print('Hello, World!')

# Добавление файла в индекс
git add prog.py

# Создание коммита
git commit -m "new: добавлен файл prog.py"
```
![image](https://github.com/user-attachments/assets/dab81bc9-689f-4030-a4d7-9830b3b9bdfa)

```bash


### Задача 3
```bash
# Инициализация первого репозитория и настройка
git init
git config user.name "coder1"
git config user.email "coder1@example.com"
echo 'print("Hello, World!")' > prog.py
git add prog.py
git commit -m "first commit"

# Создание bare-репозитория
mkdir -p repository
cd repository
git init --bare server

# Возвращение в основной репозиторий, подключение к серверу и пуш
cd ..
git remote add server repository/server
git remote -v
git push server master

# Клонирование серверного репозитория в клиентский
git clone repository/server repository/client
cd repository/client
git config user.name "coder2"
git config user.email "coder2@example.com"

# Добавление нового файла и коммит
echo "Author Information:" > readme.md
git add readme.md
git commit -m "docs"

# Переименование удаленного репозитория и пуш
git remote rename origin server
git push server master

# Возвращение в основной репозиторий, чтобы сделать pull
cd ..
git pull server master --no-rebase  # Используем merge вместо rebase

# Внесение изменений от coder1 и пуш
echo "Author: coder1" >> readme.md
git add readme.md
git commit -m "coder1 info"
git push server master

# Переход в клиентский репозиторий и внесение изменений от coder2
cd client
echo "Author: coder2" >> readme.md
git add readme.md
git commit -m "coder2 info"

# Перед `push` выполняем `pull` с merge, чтобы избежать линейной истории
git pull server master --no-rebase
git push server master

# Получение последних изменений с сервера
git pull server master --no-rebase

# Последний коммит и пуш исправлений в readme
git add readme.md
git commit -m "readme fix"
git push server master

# Переход к bare-репозиторию и просмотр истории
cd ..
cd server
git log -n 5 --graph --decorate --all
```
![image](https://github.com/user-attachments/assets/bec208a0-afa7-4698-be46-09337a02c01e)



### Задача 4
Написать программу на Питоне (или другом ЯП), которая выводит список содержимого всех объектов репозитория. Воспользоваться командой "git cat-file -p". Идеальное решение – не использовать иных сторонних команд и библиотек для работы с git.
```bash
import os
import subprocess

def find_git_root(path):
    """Finds the root of the git repository containing the given path."""
    while path != os.path.dirname(path):
        if os.path.isdir(os.path.join(path, '.git')):
            return path
        path = os.path.dirname(path)
    return None

def main():
    # Find git root
    current_dir = os.getcwd()
    git_root = find_git_root(current_dir)
    if git_root is None:
        print('Not inside a git repository')
        return

    git_objects_dir = os.path.join(git_root, '.git', 'objects')

    # List to store object IDs
    object_ids = []

    # Walk through the .git/objects directory
    for root, dirs, files in os.walk(git_objects_dir):
        # Skip 'info' and 'pack' directories
        dirs[:] = [d for d in dirs if d not in ('info', 'pack')]

        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            for filename in os.listdir(dir_path):
                # Construct object ID
                object_id = dir_name + filename
                object_ids.append(object_id)

    # Remove duplicates (in case)
    object_ids = list(set(object_ids))

    # For each object ID, run "git cat-file -p <object_id>"
    for object_id in object_ids:
        try:
            output = subprocess.check_output(['git', 'cat-file', '-p', object_id], stderr=subprocess.STDOUT, cwd=git_root)
            print('Object ID:', object_id)
            print(output.decode('utf-8', errors='replace'))
            print('-' * 40)
        except subprocess.CalledProcessError as e:
            print('Error processing object ID:', object_id)
            print(e.output.decode('utf-8', errors='replace'))
            print('-' * 40)

if __name__ == '__main__':
    main()
```
![image](https://github.com/user-attachments/assets/0e9413f6-0e06-4c2b-90af-650a64e30c13)





```
