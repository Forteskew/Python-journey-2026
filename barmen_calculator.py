# День 2. Барменский калькулятор чаевых и смен

print("=== Барменский калькулятор v0.2 ===")

# Список смен за неделю
shifts = []

# Ввод данных через цикл while
while True:
    shift = input("\nСколько коктейлей приготовил за смену? (или 'стоп' для завершения): ")
    if shift.lower() == 'стоп':
        break
    try:
        shifts.append(int(shift))
    except ValueError:
        print("Пожалуйста, введи число или 'стоп'")

if not shifts:
    print("Нет данных о сменах.")
else:
    total_drinks = sum(shifts)
    average = total_drinks / len(shifts)
    
    # Расчёт чаевых (15% от среднего чека 800 руб. за коктейль)
    tips = total_drinks * 800 * 0.15
    
    print(f"\nЗа неделю ты приготовил {total_drinks} коктейлей")
    print(f"Среднее за смену: {average:.1f} коктейлей")
    print(f"Примерные чаевые за неделю: {tips:.0f} руб.")
    
    # Анализ производительности
    if average >= 40:
        print("🔥 Ты монстр! Такие результаты — это уже уровень senior-бармена.")
    elif average >= 25:
        print("👍 Хороший темп. Продолжай в том же духе!")
    else:
        print("🫡 Нормально для старта. Будем улучшать!")

print("\nОтличная работа! День 2 завершён.")