import json
import glob
import os

def generate_leaderboard():
    print("Начало генерации таблицы лидеров...")
    results = []
    result_files = glob.glob("results/**/*.json", recursive=True)
    print(f"Найдено файлов с результатами: {len(result_files)}")
    
    for file in result_files:
        try:
            print(f"Обработка файла: {file}")
            with open(file) as f:
                data = json.load(f)
                
            # Извлекаем имя пользователя из пути
            username = os.path.basename(os.path.dirname(file))
            print(f"Пользователь: {username}")
            
            # Проверяем наличие необходимых полей
            if 'generation_time' not in data or 'sorting_time' not in data:
                print(f"⚠️ Отсутствуют поля в {file}: {data}")
                continue
                
            total = data['generation_time'] + data['sorting_time']
            results.append({
                "user": username,
                "generation": data["generation_time"],
                "sorting": data["sorting_time"],
                "total": total
            })
            print(f"✅ Добавлен результат: {username} - {total:.2f} мс")
            
        except Exception as e:
            print(f"❌ Ошибка обработки {file}: {str(e)}")
    
    # Сортируем по лучшему результату
    results.sort(key=lambda x: x["total"])
    print(f"Всего результатов: {len(results)}")
    
    # Генерация таблицы
    md = "# 🏆 Таблица лидеров\n\n"
    
    if not results:
        md += "Пока никаких результатов!\n"
        print("⚠️ Нет данных для таблицы лидеров")
        return md
    
    md += "| Место | Пользователь | Генерация (мс) | Сортировка (мс) | Всего (мс) |\n"
    md += "|-------|-------------|----------------|-----------------|------------|\n"
    
    for i, res in enumerate(results[:10]):
        md += f"| {i+1} | {res['user']} | {res['generation']:.2f} | {res['sorting']:.2f} | **{res['total']:.2f}** |\n"
    
    print("✅ Таблица лидеров сгенерирована")
    return md

if __name__ == "__main__":
    leaderboard = generate_leaderboard()
    with open("LEADERBOARD.md", "w") as f:
        f.write(leaderboard)
