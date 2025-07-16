import requests
import json
from typing import Optional, List, Dict
import sys

BASE_URL = "http://localhost:8000"

class TaskManagerClient:
    def __init__(self):
        self.base_url = BASE_URL
    
    def print_response(self, response: requests.Response):
        """
        Печатает ответ сервера в удобном формате.
        """
        try:
            if response.status_code == 204:  # No Content
                print("Успешно: нет содержимого в ответе")
                return
            
            data = response.json()
            print(f"Статус код: {response.status_code}")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except ValueError:
            print(f"Ответ сервера (не JSON): {response.text}")
    
    def create_user(self, name: str, surname: str) -> Optional[Dict]:
        """
        Создает нового пользователя.
        """
        url = f"{self.base_url}/users/"
        data = {"name": name, "surname": surname}
        response = requests.post(url, json=data)
        
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Ошибка при создании пользователя:")
            self.print_response(response)
            return None
    
    def create_task(self, title: str, user_id: int, description: Optional[str] = None) -> Optional[Dict]:
        """
        Создает новую задачу.
        """
        url = f"{self.base_url}/tasks/"
        data = {
            "title": title,
            "user_id": user_id,
            "description": description
        }
        response = requests.post(url, json=data)
        
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Ошибка при создании задачи:")
            self.print_response(response)
            return None
    
    def get_user_tasks(self, user_id: int) -> List[Dict]:
        """
        Получает задачи пользователя.
        """
        url = f"{self.base_url}/tasks/"
        params = {"user_id": user_id}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка при получении задач пользователя:")
            self.print_response(response)
            return []
    
    def get_all_tasks(self) -> List[Dict]:
        """
        Получает все задачи.
        """
        url = f"{self.base_url}/tasks/all"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка при получении всех задач:")
            self.print_response(response)
            return []
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """
        Получает задачу по ID.
        """
        url = f"{self.base_url}/tasks/{task_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка при получении задачи:")
            self.print_response(response)
            return None
    
    def update_task(self, task_id: int, title: Optional[str] = None, 
                   description: Optional[str] = None) -> Optional[Dict]:
        """
        Обновляет данные задачи.
        """
        url = f"{self.base_url}/tasks/{task_id}"
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        
        response = requests.put(url, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка при обновлении задачи:")
            self.print_response(response)
            return None
    
    def delete_task(self, task_id: int) -> bool:
        """
        Удаляет задачу.
        """
        url = f"{self.base_url}/tasks/{task_id}"
        response = requests.delete(url)
        
        if response.status_code == 200:
            print("Задача успешно удалена")
            return True
        else:
            print(f"Ошибка при удалении задачи:")
            self.print_response(response)
            return False


def show_menu():
    print("\n=== Меню управления задачами ===")
    print("1. Создать пользователя")
    print("2. Создать задачу")
    print("3. Показать задачи пользователя")
    print("4. Показать все задачи")
    print("5. Обновить задачу")
    print("6. Удалить задачу")
    print("7. Выход")

def get_input(prompt: str, required: bool = True) -> Optional[str]:
    while True:
        value = input(prompt).strip()
        if not value and required:
            print("Это поле обязательно для заполнения!")
            continue
        return value if value else None

def main():
    client = TaskManagerClient()
    current_user = None
    
    while True:
        show_menu()
        choice = get_input("Выберите действие (1-7): ")
        
        try:
            if choice == "1":  # Создать пользователя
                print("\n--- Создание пользователя ---")
                name = get_input("Имя: ")
                surname = get_input("Фамилия: ")
                
                user = client.create_user(name, surname)
                if user:
                    current_user = user
                    print(f"\nПользователь создан: {user['name']} {user['surname']} (ID: {user['id']})")
            
            elif choice == "2":  # Создать задачу
                if not current_user:
                    print("\nСначала создайте пользователя!")
                    continue
                
                print("\n--- Создание задачи ---")
                title = get_input("Название задачи: ")
                description = get_input("Описание (необязательно): ", required=False)
                
                task = client.create_task(title, current_user["id"], description)
                if task:
                    print(f"\nЗадача создана: {task['title']} (ID: {task['id']})")
            
            elif choice == "3":  # Показать задачи пользователя
                if not current_user:
                    print("\nСначала создайте пользователя!")
                    continue
                
                print(f"\n--- Задачи пользователя {current_user['name']} ---")
                tasks = client.get_user_tasks(current_user["id"])
                if tasks:
                    for task in tasks:
                        print(f"\nID: {task['id']}")
                        print(f"Заголовок: {task['title']}")
                        print(f"Описание: {task['description'] or 'нет описания'}")
                        print(f"Создана: {task['created_at']}")
                else:
                    print("У пользователя нет задач")
            
            elif choice == "4":  # Показать все задачи
                print("\n--- Все задачи ---")
                tasks = client.get_all_tasks()
                if tasks:
                    for task in tasks:
                        print(f"\nID: {task['id']}")
                        print(f"Заголовок: {task['title']}")
                        print(f"Пользователь: {task['user_name']} {task['user_surname']}")
                        print(f"Создана: {task['created_at']}")
                else:
                    print("Нет задач в системе")
            
            elif choice == "5":  # Обновить задачу
                task_id = get_input("Введите ID задачи для обновления: ")
                if not task_id.isdigit():
                    print("ID задачи должен быть числом!")
                    continue
                
                print("\n--- Обновление задачи ---")
                title = get_input("Новое название (оставьте пустым, чтобы не менять): ", required=False)
                description = get_input("Новое описание (оставьте пустым, чтобы не менять): ", required=False)
                
                if not title and not description:
                    print("Не указаны данные для обновления!")
                    continue
                
                updated_task = client.update_task(int(task_id), title, description)
                if updated_task:
                    print("\nЗадача обновлена:")
                    print(f"ID: {updated_task['id']}")
                    print(f"Новый заголовок: {updated_task['title']}")
                    print(f"Новое описание: {updated_task['description'] or 'нет описания'}")
            
            elif choice == "6":  # Удалить задачу
                task_id = get_input("Введите ID задачи для удаления: ")
                if not task_id.isdigit():
                    print("ID задачи должен быть числом!")
                    continue
                
                if client.delete_task(int(task_id)):
                    print("Задача успешно удалена")
            
            elif choice == "7":  # Выход
                print("\nДо свидания!")
                sys.exit(0)
            
            else:
                print("\nНеверный выбор. Попробуйте снова.")
        
        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")

if __name__ == "__main__":
    print("=== Клиент для управления задачами ===")
    main()