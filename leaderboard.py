import json
import glob
import os
from datetime import datetime

def generate_leaderboard():
    # Создаем базовую структуру
    md = "# 🏆 Таблица лидеров\n\n"
    md += f"Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Пытаемся найти и обработать результаты
    try:
        results = []
        for file in glob.glob("results/**/result.json", recursive=True):
            try:
                with open(file) as f:
                    data = json.load(f)
                username = os.path.basename(os.path.dirname(file))
                total = data['generation_time'] + data['sorting_time']
                results.append({
                    "user": username,
                    "generation": data["generation_time"],
                    "sorting": data["sorting_time"],
                    "total": total
                })
            except:
                continue
        
        if results:
            results.sort(key=lambda x: x["total"])
            md += "| Место | Пользователь | Генерация (мс) | Сортировка (мс) | Всего (мс) |\n"
            md += "|-------|-------------|----------------|-----------------|------------|\n"
            
            for i, res in enumerate(results[:10]):
                md += f"| {i+1} | {res['user']} | {res['generation']:.2f} | "
                md += f"{res['sorting']:.2f} | **{res['total']:.2f}** |\n"
        else:
            md += "## Пока нет результатов!\n"
            md += "Первые результаты появятся здесь после отправки решений.\n"
            
    except Exception as e:
        md += f"## Ошибка при генерации\n```\n{str(e)}\n```\n"
    
    # Гарантированный тестовый результат
    md += "\n\n## Пример формата\n"
    md += "| 1 | ExampleUser | 12.34 | 56.78 | **69.12** |"
    
    return md

if __name__ == "__main__":
    leaderboard = generate_leaderboard()
    with open("LEADERBOARD.md", "w") as f:
        f.write(leaderboard)
