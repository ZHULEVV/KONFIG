## Описание

Инструмент для визуализации графа зависимостей пакетов PIP. Граф строится в формате Graphviz DOT и выводится на экран в виде кода.

## Установка 

1.**Клонируйте репозиторий:**
 ```bash
   https://github.com/ZHULEVV/KONFIG/tree/main/dz2
   ```
2.Установите необходимые зависимости:
```bash
sudo apt-get install graphviz
pip install pytest
```

## Конфигурация

1.Создайте config.toml:

```toml

  graphviz_path = "/usr/bin/dot"
  package_name = "matplotlib"
  output_path = "matplotlib.dot"
  max_depth = 3
  repository_url = "https://pypi.org"

```

## Пример использования

1. Запустите скрипт:
   ```bash
   python main.py config.toml
   ```
 Пример вывода графа:
   ```bash
   digraph dependencies {
  "matplotlib" -> "contourpy";
  "matplotlib" -> "cycler";
  "matplotlib" -> "fonttools";
  "matplotlib" -> "kiwisolver";
  "matplotlib" -> "numpy";
  "matplotlib" -> "packaging";
  "matplotlib" -> "pillow";
  "matplotlib" -> "pyparsing";
  "matplotlib" -> "python-dateutil";
  "contourpy" -> "numpy";
  "python-dateutil" -> "six";
}
}


## Тестирование
Запустите тесты:
```bash
python3 -m unittest test_core.py
```
![image](https://github.com/user-attachments/assets/303f4072-f7db-44e1-b437-3d064f5f8d75)

![image](https://github.com/user-attachments/assets/11504c55-e5ca-4dc1-b5eb-219c2190bfed)



