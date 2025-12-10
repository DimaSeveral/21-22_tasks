# client.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import socket
import json
from messages import MENUS, TASK1, TASK2, TASK4

# --- Вспомогательная функция отправки запросов (без изменений) ---
def send_request(task: str, params: dict):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9999))
        request_bytes = json.dumps({"task": task, "params": params}).encode('utf-8')
        sock.send(request_bytes)
        response_bytes = sock.recv(4096)
        response_text = response_bytes.decode('utf-8')
        return json.loads(response_text)
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None
    finally:
        sock.close()

# --- Состояния автомата ---
class ClientFSM:
    def __init__(self):
        self.current_state = "main_menu"
        self.context = {}  # Для хранения промежуточных данных (например, введённый текст)

        # Словарь состояний: ключ — имя состояния, значение — функция-обработчик
        self.states = {
            "main_menu": self.main_menu,
            "task1_input": self.task1_input,
            "task1_result": self.task1_result,
            "task2_input": self.task2_input,
            "task2_result": self.task2_result,
            "task4_input_a": self.task4_input_a,
            "task4_input_b": self.task4_input_b,
            "task4_input_op": self.task4_input_op,
            "task4_result": self.task4_result,
            "exit": self.exit_state
        }

    # --- Обработчики состояний ---
    def main_menu(self):
        print("\n" + "="*50)
        print(MENUS["main_title"])
        print("1. " + MENUS["task1"])
        print("2. " + MENUS["task2"])
        print("3. " + MENUS["task4"])
        print("4. " + MENUS["exit"])
        choice = input(MENUS["prompt_choice"]).strip()

        if choice == '1':
            return "task1_input"
        elif choice == '2':
            return "task2_input"
        elif choice == '3':
            return "task4_input_a"
        elif choice == '4':
            return "exit"
        else:
            print(MENUS["invalid_choice"])
            return "main_menu"  # остаёмся в том же состоянии

    def task1_input(self):
        print(f"\n{TASK1['title']}")
        text = input(TASK1["prompt_text"]).strip()
        if not text:
            print(TASK1["empty_input"])
            return "main_menu"
        self.context["task1_text"] = text
        return "task1_result"

    def task1_result(self):
        response = send_request("task1", {"text": self.context["task1_text"]})
        if response and response["status"] == "success":
            result = response["result"]
            if result:
                print(TASK1["result"].format(result))
            else:
                print(TASK1["no_unique"])
        else:
            print("Ошибка:", response["message"] if response else "Нет ответа от сервера")
        input("\nНажмите Enter, чтобы вернуться в меню...")
        return "main_menu"

    def task2_input(self):
        print(f"\n{TASK2['title']}")
        text = input(TASK2["prompt_text"]).strip()
        if not text:
            print(TASK2["empty_input"])
            return "main_menu"
        self.context["task2_text"] = text
        return "task2_result"

    def task2_result(self):
        response = send_request("task2", {"text": self.context["task2_text"]})
        if response and response["status"] == "success":
            words = response["result"]["words"]
            length = response["result"]["length"]
            if words:
                print(TASK2["result"].format(words, length))
            else:
                print(TASK2["no_words"])
        else:
            print("Ошибка:", response["message"] if response else "Нет ответа от сервера")
        input("\nНажмите Enter, чтобы вернуться в меню...")
        return "main_menu"

    def task4_input_a(self):
        print(f"\n{TASK4['title']}")
        print(TASK4["intro"])
        a_str = input(TASK4["prompt_a"]).strip()
        if not a_str:
            print(TASK4["empty_input"])
            return "main_menu"
        try:
            a = list(map(int, a_str.split()))
            self.context["task4_a"] = a
            return "task4_input_b"
        except ValueError:
            print(TASK4["error_input"].format("Некорректные цифры"))
            return "main_menu"

    def task4_input_b(self):
        b_str = input(TASK4["prompt_b"]).strip()
        if not b_str:
            print(TASK4["empty_input"])
            return "main_menu"
        try:
            b = list(map(int, b_str.split()))
            self.context["task4_b"] = b
            return "task4_input_op"
        except ValueError:
            print(TASK4["error_input"].format("Некорректные цифры"))
            return "main_menu"

    def task4_input_op(self):
        op = input(TASK4["prompt_op"]).strip().lower()
        if op not in ('add', 'sub'):
            print(TASK4["invalid_op"])
            return "main_menu"
        self.context["task4_op"] = op
        return "task4_result"

    def task4_result(self):
        a = self.context["task4_a"]
        b = self.context["task4_b"]
        op = self.context["task4_op"]
        response = send_request("task4", {"a": a, "b": b, "op": op})
        if response and response["status"] == "success":
            print(TASK4["result"].format(response["result"]))
        else:
            print("Ошибка:", response["message"] if response else "Нет ответа от сервера")
        input("\nНажмите Enter, чтобы вернуться в меню...")
        return "main_menu"

    def exit_state(self):
        print(MENUS["exit_message"])
        return None  # Сигнал завершения

    # --- Основной цикл автомата ---
    def run(self):
        print("Клиент запущен. Подключение к серверу...")
        while self.current_state is not None:
            handler = self.states[self.current_state]
            next_state = handler()
            self.current_state = next_state

# --- Запуск ---
if __name__ == "__main__":
    fsm = ClientFSM()
    fsm.run()