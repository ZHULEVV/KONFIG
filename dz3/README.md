## Инструмент командной строки для преобразования учебного конфигурационного языка в формат YAML

Этот проект представляет инструмент командной строки на Python, который преобразует текст из учебного конфигурационного языка в формат YAML. Он поддерживает различные конструкции, такие как однострочные комментарии, массивы, словари, объявления констант, вычисления выражений на этапе трансляции и работу с переменными. Инструмент обрабатывает синтаксические ошибки и выводит информативные сообщения об ошибках.


# Структура проекта
- config_parser.py
- test.py
- input1.txt
- input2.txt
- output1.yaml
- output2.yaml

# Примеры
input1.txt   
```bash

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

```
input2.txt   
```bash


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


#( "Living Room", "Bedroom", "Kitchen", "Garage" )


```
# Запуск команды 
```bash
python config_parser.py input1.txt output1.yaml
python config_parser.py input2.txt output2.yaml
```
Конвертированный yaml файл 
```bash
{
   - documentRoot: /var/www/html
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

}
```
Конвертированный yaml файл 
```bash
{
   - devices:
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

}
```

# Проверка тестов 
```bash
python -m unittest tests.py
```
![image](https://github.com/user-attachments/assets/3cb979cf-c149-4ef2-85fd-ded52d7f9523)

# Заключение 
Этот инструмент предоставляет удобный способ трансляции конфигураций из учебного конфигурационного языка в формат YAML, поддерживая все основные конструкции и обеспечивая надежную обработку ошибок.
