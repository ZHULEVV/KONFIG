import re
import yaml
import sys

class ConfigParser:
    def __init__(self):
        self.variables = {}  # Для хранения переменных (например, serverPort, serverHost)
        self.comments = []   # Для хранения комментариев
        self.output_data = []  # Для хранения структуры конфигурации

    def transform_value(self, value):
        """
        Преобразует строковое значение в соответствующий тип данных.
        :param value: строка
        :return: преобразованное значение
        """
        value = value.strip()

        # Обработка выражений вида ![имя] для вычисления констант
        if value.startswith('![') and value.endswith(']'):
            const_name = value[2:-1].strip()
            if const_name in self.variables:
                return self.variables[const_name]
            else:
                raise ValueError(f"Константа '{const_name}' не найдена.")

        # Обработка чисел
        if value.isdigit():
            return int(value)

        # Обработка строк
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]

        # Обработка булевых значений
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False

        # Если значение - это массив
        if value.startswith('#(') and value.endswith(')'):
            values = value[2:-1].split(',')
            return [v.strip().strip('"') for v in values]

        return value

    def parse(self, input_stream):
        lines = input_stream.readlines()
        current_scope = None

        for line in lines:
            line = line.strip()

            # Пропуск пустых строк и комментариев
            if not line or line.startswith("{{!--") or line.startswith("#"):
                continue

            # Обработка многострочного комментария
            if line.startswith("{{!--"):
                comment = []
                while not line.endswith("--}}"):
                    comment.append(line)
                    line = next(lines).strip()
                comment.append(line)
                self.comments.append("\n".join(comment))
                continue

            # Обработка определения констант
            if line.startswith("def"):
                match = re.match(r'def\s+(\w+)\s*=\s*(.*);', line)
                if match:
                    const_name = match.group(1).strip()
                    value = self.transform_value(match.group(2).strip())
                    self.variables[const_name] = value
                    continue
                else:
                    raise ValueError(f"Ошибка в определении константы: {line}")

            # Обработка начала и конца словаря (begin...end)
            if line.startswith("begin"):
                if current_scope is None:  # Если current_scope ещё не инициализирован, инициализируем его
                    current_scope = {}
                continue

            if line.startswith("end"):
                if current_scope is not None:
                    self.output_data.append(current_scope)
                    current_scope = None
                continue

            # Обработка присваивания значений
            match = re.match(r'(\w+)\s*:=\s*(.*);', line)
            if match:
                name = match.group(1).strip()
                value = self.transform_value(match.group(2).strip())
                if current_scope is not None:
                    current_scope[name] = value
                else:
                    self.variables[name] = value
                continue

            # Обработка вложенных блоков (например, logging и security)
            match_logging = re.match(r'(\w+)\s*:=\s*begin', line)
            if match_logging:
                section_name = match_logging.group(1).strip()
                if current_scope is None:  # Добавлена дополнительная проверка для безопасности
                    current_scope = {}
                current_scope[section_name] = {}
                continue

            match_end_section = re.match(r'end\s*', line)
            if match_end_section and current_scope:
                self.output_data.append(current_scope)
                current_scope = None
                continue

    def save_to_yaml(self, output_file):
        """
        Сохраняет результат в YAML.
        :param output_file: Путь к файлу
        """
        with open(output_file, 'w', encoding='utf-8') as file:
            yaml.dump(self.output_data, file, default_flow_style=False, allow_unicode=True)


def open_file_with_encoding(input_file):
    """
    Функция для открытия файла с различными кодировками.
    Пробует открыть файл с кодировками 'utf-8', 'windows-1251', 'latin1'.
    :param input_file: путь к файлу
    :return: открытый файл
    """
    encodings = ['utf-8', 'windows-1251', 'latin1']  # Добавлены дополнительные кодировки
    for encoding in encodings:
        try:
            return open(input_file, 'r', encoding=encoding)
        except UnicodeDecodeError:
            print(f"Ошибка кодировки для файла {input_file} с кодировкой {encoding}. Попробую другую.")
        except Exception as e:
            print(f"Не удалось открыть файл {input_file} с кодировкой {encoding}. Ошибка: {e}")
    raise ValueError(f"Не удалось открыть файл {input_file} с поддерживаемыми кодировками.")


def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "output.yaml"

        # Попытка открыть файл с кодировками
        try:
            with open_file_with_encoding(input_file) as file:
                parser = ConfigParser()
                parser.parse(file)
                parser.save_to_yaml(output_file)
                print(f"Файл успешно обработан и сохранён в {output_file}")
        except Exception as e:
            print(f"Ошибка при чтении или сохранении файла: {e}")
    else:
        print("Ошибка: Не указан файл входных данных или выходной файл.")


if __name__ == '__main__':
    main()
