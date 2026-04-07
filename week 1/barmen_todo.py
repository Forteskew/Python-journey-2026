# День 3 — Барменский TODO-лист (упрощённая версия с комментариями)

# ====================== ИМПОРТЫ ======================
# import — это способ подключить готовые инструменты Python
import json                    # нужен, чтобы работать с файлами .json (сохранять и загружать данные)
from datetime import datetime  # нужен, чтобы автоматически ставить дату и время создания задачи


# ====================== ФУНКЦИИ ======================
# Функция — это блок кода, который можно вызывать много раз по имени.
# Мы создаём функции, чтобы не повторять один и тот же код.

def load_tasks():
    """Загружает задачи из файла tasks.json"""
    try:
        # Открываем файл tasks.json для чтения
        with open("tasks.json", "r", encoding="utf-8") as file:
            return json.load(file)   # превращаем содержимое файла в список Python
    except:
        # Если файла нет или произошла ошибка — возвращаем пустой список
        return []


def save_tasks(tasks):
    """Сохраняет список задач в файл tasks.json"""
    with open("tasks.json", "w", encoding="utf-8") as file:
        # json.dump — записывает данные в файл в формате JSON
        json.dump(tasks, file, ensure_ascii=False, indent=4)


def show_tasks(tasks):
    """Показывает все задачи на экране"""
    if not tasks:
        print("📭 Пока нет ни одной задачи.")
        return

    print("\n📋 Текущие задачи:")
    for task in tasks:
        # Определяем статус (эмодзи)
        if task["done"]:
            status = "✅"      # выполнена
        else:
            status = "⏳"      # ещё не выполнена
        
        print(f"{task['id']}. {status} {task['text']}   ({task['date']})")

    # Добавляем статистику по выполненным задачам 
    total = len(tasks)
    done = sum(1 for task in tasks if task["done"])
    print(f"\nВсего задач: {total} | Выполнено: {done}")

def add_task(tasks):
    """Добавляет новую задачу в список"""
    text = input("\nЧто нужно сделать во время смены? ").strip()
    
    if not text:                     # если пользователь ничего не ввёл
        print("❌ Задача не может быть пустой!")
        return

    # Создаём новую задачу в виде словаря
    new_task = {
        "id": len(tasks) + 1,                    # номер задачи = количество задач + 1
        "text": text,                            # текст задачи
        "done": False,                           # по умолчанию задача не выполнена
        "date": datetime.now().strftime("%d.%m %H:%M")  # текущая дата и время
    }
    
    tasks.append(new_task)           # добавляем задачу в список
    print(f"✅ Задача добавлена: {text}")


def mark_done(tasks):
    """Отмечает задачу как выполненную"""
    show_tasks(tasks)                # сначала показываем список
    
    try:
        num = int(input("\nВведите номер выполненной задачи: "))
        
        for task in tasks:
            if task["id"] == num:            # нашли задачу с нужным номером
                task["done"] = True
                print(f"🎉 Задача №{num} отмечена как выполненная!")
                return                       # выходим из функции
        
        print("❌ Задачи с таким номером не найдено.")
        
    except ValueError:
        print("❌ Нужно ввести число!")

def delete_task(tasks):
    """Удаляет задачу"""
    
    if not tasks:               # Если список задач пустой
        print("❌ Нет задач для удаления")
        return                  # выходим из функции
    
    show_tasks(tasks)           # показываем список задач

    try: 
        num = int(input("\nВведите номер задачи, которую хотите удалить: "))
        print(f"Вы ввели номер: {num}")

        for i in range(len(tasks)):     # перебираем индексы списка
            if tasks[i]["id"] == num:   # если id задачи совпадает с введннным номером
                deleted_text = tasks[i]["text"] # запоминаем текст задачи перед удалением
                del tasks[i]            # удаляем задачу по индексу
                print(f"🗑️ Задача удалена: {deleted_text}")
                return
        
        # Если дошли сюда, задача с таким номером не найдена
        print(f'❌ Задача с таким номером {num} не найдена!')


    except ValueError:
        print("❌ Нужно ввести число! ")



    # Просто показываем список задач и текстовую надпись
    print("\n---Функция удаления в раработке ---")
    

# ====================== ОСНОВНАЯ ПРОГРАММА ======================

# Загружаем задачи из файла при запуске программы
tasks = load_tasks()

print("🍸 Добро пожаловать в Барменский TODO-лист!\n")

while True:                          # бесконечный цикл, пока пользователь не выйдет
    print("=" * 45)
    print("1. Показать все задачи")
    print("2. Добавить новую задачу")
    print("3. Отметить задачу как выполненную")
    print("4. Удалить задачу")
    print("5. Сохранить и выйти")
    print("=" * 45)

    choice = input("\nВыберите действие (1-5): ").strip()

    if choice == "1":
        show_tasks(tasks)
    elif choice == "2":
        add_task(tasks)
    elif choice == "3":
        mark_done(tasks)
    elif choice == "4":
        delete_task(tasks)
    elif choice == "5":
        save_tasks(tasks)                    # сохраняем все задачи в файл
        print("💾 Задачи успешно сохранены! До следующей смены.")
        break                                # выходим из цикла while
    else:
        print("❌ Неверный выбор. Введите число от 1 до 5.")