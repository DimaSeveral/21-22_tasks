import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import socket
import time
import random
import json
import logging
import threading  # ← добавляем для многопоточности
from datetime import datetime
from tasks.task1_logic import find_unique_words
from tasks.task2_logic import find_longest_word
from tasks.task4_logic import process_big_numbers
from exceptions import AppException

# Настройка логирования в файл
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler("server.log", encoding='utf-8'),
        logging.StreamHandler()  # чтобы выводить в консоль
    ]
)
logger = logging.getLogger()

# Глобальный счётчик клиентов (для имён)
client_counter = 1

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

class ClientHandler(threading.Thread):
    """Класс для обработки одного клиента в отдельном потоке"""

    def __init__(self, client_socket, client_name):
        # Инициализируем Thread, указывая целевую функцию
        threading.Thread.__init__(self, target=self.handle_client)
        self.client_socket = client_socket
        self.client_name = client_name
        self.daemon = True  # Поток завершится при закрытии главного потока

    def handle_client(self):
        """Обработка запроса клиента"""
        logger.info(f"{get_timestamp()} {self.client_name}: подключился")

        try:
            # Получаем данные
            raw_data = self.client_socket.recv(4096).decode('utf-8')
            data = json.loads(raw_data)

            # Обрабатываем
            response = self.handle_client_request(data)

            # Отправляем ответ
            self.client_socket.send(json.dumps(response).encode('utf-8'))

        except json.JSONDecodeError:
            logger.error(f"{get_timestamp()} {self.client_name}: получен некорректный JSON")
            error_response = {"status": "error", "message": "Некорректный запрос"}
            self.client_socket.send(json.dumps(error_response).encode('utf-8'))
        except Exception as e:
            logger.error(f"{get_timestamp()} {self.client_name}: ошибка при обработке: {e}")
            error_response = {"status": "error", "message": "Ошибка сервера"}
            self.client_socket.send(json.dumps(error_response).encode('utf-8'))
        finally:
            self.client_socket.close()
            logger.info(f"{get_timestamp()} {self.client_name}: отключился")

    def handle_client_request(self, data: dict):
        """Обрабатывает запрос от клиента и возвращает результат"""
        task = data.get("task")
        params = data.get("params", {})

    
        try:
            if task == "task1":
                text = params.get("text", "")
                logger.info(f"{get_timestamp()} {self.client_name}: отправлен запрос на поиск уникальных слов")
                delay = random.uniform(10.5, 17.0)
                time.sleep(delay)

                result = find_unique_words(text)
                logger.info(f"{get_timestamp()} {self.client_name}: найдены уникальные слова")
                return {"status": "success", "result": result}

            elif task == "task2":
                text = params.get("text", "")
                logger.info(f"{get_timestamp()} {self.client_name}: отправлен запрос на поиск самого длинного слова")
                delay = random.uniform(10.5, 17.0)
                time.sleep(delay)

                words, length = find_longest_word(text)
                logger.info(f"{get_timestamp()} {self.client_name}: найдено самое длинное слово")
                return {"status": "success", "result": {"words": words, "length": length}}

            elif task == "task4":
                a = params.get("a", [])
                b = params.get("b", [])
                op = params.get("op", "")
                logger.info(f"{get_timestamp()} {self.client_name}: отправлен запрос на операцию с большими числами")
                delay = random.uniform(10.5, 17.0)
                time.sleep(delay)

                result = process_big_numbers(a, b, op)
                logger.info(f"{get_timestamp()} {self.client_name}: выполнена операция с большими числами")
                return {"status": "success", "result": result}

            else:
                return {"status": "error", "message": "Неизвестное задание"}

        except AppException as e:
            logger.warning(f"{get_timestamp()} {self.client_name}: ошибка приложения: {e}")
            return {"status": "error", "message": str(e)}
        except Exception as e:
            logger.error(f"{get_timestamp()} {self.client_name}: непредвиденная ошибка: {e}")
            return {"status": "error", "message": "Внутренняя ошибка сервера"}

def main():
    global client_counter
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(5)
    print("Сервер запущен на localhost:9999")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_name = f"Клиент{client_counter}"
            client_counter += 1

            # Создаём экземпляр потока-обработчика
            handler = ClientHandler(client_socket, client_name)
            # Запускаем поток
            handler.start()

    except KeyboardInterrupt:
        print("\nСервер остановлен.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()