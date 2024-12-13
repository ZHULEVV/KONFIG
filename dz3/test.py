import unittest
import os
from config_parser import ConfigParser
from config_parser import open_file_with_encoding  # Ensure you import this function

class TestConfigParser(unittest.TestCase):
    def setUp(self):
        """Создание тестовых файлов перед выполнением тестов."""
        self.input_file1 = "test_input1.txt"
        self.input_file2 = "test_input2.txt"
        self.output_file = "test_output.yaml"

        input1_content = """{{!-- Настройки веб-сервера --}}
def serverPort = 443;
def serverHost = "example.com";

begin
    server := "nginx";
    port := ![serverPort];
    host := ![serverHost];
    documentRoot := "/var/www/html";
    security := begin
        ssl := true;
        sslCertificate := "/etc/ssl/certs/server.crt";
        sslKey := "/etc/ssl/private/server.key";
        firewall := true;
    end;
    logging := begin
        accessLog := "/var/log/nginx/access.log";
        errorLog := "/var/log/nginx/error.log";
        logLevel := "warn";
    end
end

{{!-- Поддерживаемые модули --}}
#( "mod_rewrite", "mod_headers", "mod_ssl" )
"""

        input2_content = """{{!-- Настройки умного дома --}}
def timezone = "UTC+3";
def defaultTemperature = 22;

begin
    location := "Living Room";
    devices := #( "Thermostat", "Light", "Camera" );
    thermostat := begin
        targetTemperature := ![defaultTemperature];
        mode := "Auto";
    end;
    light := begin
        intensity := 75;
        color := "Warm White";
        schedule := #( "18:00-23:00", "06:00-08:00" );
    end;
    camera := begin
        enabled := true;
        recording := "Motion Detection";
        storage := "Cloud";
    end
end

{{!-- Список комнат --}}
#( "Living Room", "Bedroom", "Kitchen", "Garage" )
"""
        # Запись тестовых файлов
        with open(self.input_file1, "w", encoding="utf-8") as file:
            file.write(input1_content)

        with open(self.input_file2, "w", encoding="utf-8") as file:
            file.write(input2_content)

    def tearDown(self):
        """Удаление тестовых файлов после выполнения тестов."""
        if os.path.exists(self.input_file1):
            os.remove(self.input_file1)
        if os.path.exists(self.input_file2):
            os.remove(self.input_file2)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_input1(self):
        """Тестирование работы с input1.txt."""
        parser = ConfigParser()
        try:
            # Use open_file_with_encoding to ensure correct encoding
            with open_file_with_encoding(self.input_file1) as file:
                parser.parse(file)
        except Exception as e:
            self.fail(f"Failed to parse input1.txt: {e}")

        parser.save_to_yaml(self.output_file)

        with open(self.output_file, 'r', encoding='utf-8') as yaml_file:
            output_data = yaml_file.read()

        expected_output = """- documentRoot: /var/www/html
  firewall: true
  host: example.com
  port: 443
  security: {}
  server: nginx
  ssl: true
  sslCertificate: /etc/ssl/certs/server.crt
  sslKey: /etc/ssl/private/server.key
- accessLog: /var/log/nginx/access.log
  errorLog: /var/log/nginx/error.log
  logLevel: warn
  logging: {}

"""
        self.assertEqual(output_data.strip(), expected_output.strip())

    def test_input2(self):
        """Тестирование работы с input2.txt."""
        parser = ConfigParser()
        try:
            # Use open_file_with_encoding to ensure correct encoding
            with open_file_with_encoding(self.input_file2) as file:
                parser.parse(file)
        except Exception as e:
            self.fail(f"Failed to parse input2.txt: {e}")

        parser.save_to_yaml(self.output_file)

        with open(self.output_file, 'r', encoding='utf-8') as yaml_file:
            output_data = yaml_file.read()

        expected_output = """- devices:
  - Thermostat
  - Light
  - Camera
  location: Living Room
  mode: Auto
  targetTemperature: 22
  thermostat: {}
- color: Warm White
  intensity: 75
  light: {}
  schedule:
  - 18:00-23:00
  - 06:00-08:00
- camera: {}
  enabled: true
  recording: Motion Detection
  storage: Cloud
"""
        self.assertEqual(output_data.strip(), expected_output.strip())


if __name__ == "__main__":
    unittest.main()
