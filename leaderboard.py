import json
import glob
import os
from datetime import datetime

def generate_leaderboard():
    md = "# 🏆 Таблица лидеров\n\n"
    md += f"Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    try:
        results = []
        # Исправлен путь для поиска результатов
        for file in glob.glob("results/*/result.json", recursive=True):
            try:
                with open(file) as f:
                    data = json.load(f)
                # Извлекаем имя пользователя из пути
                username = os.path.basename(os.path.dirname(file))
                results.append({
                    "user": username,
                    "generation": data["generation_time"],
                    "sorting": data["sorting_time"],
                    "total": data["generation_time"] + data["sorting_time"]
                })
            except Exception as e:
                print(f"Ошибка обработки файла {file}: {str(e)}")
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
    
    return md

if __name__ == "__main__":
    leaderboard = generate_leaderboard()
    with open("LEADERBOARD.md", "w") as f:
        f.write(leaderboard)
