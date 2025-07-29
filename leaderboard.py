import json
import glob
import os
import sys
from datetime import datetime

def generate_leaderboard():
    try:
        sys.stderr.write("Generating leaderboard...\n")
        user_results = {}
        for file in glob.glob("results/*/result.json"):
            try:
                sys.stderr.write(f"Processing: {file}\n")
                with open(file) as f:
                    data = json.load(f)
                username = os.path.basename(os.path.dirname(file))
                total = data['generation_time'] + data['sorting_time']
                
                if username not in user_results or total < user_results[username]["total"]:
                    user_results[username] = {
                        "generation": data["generation_time"],
                        "sorting": data["sorting_time"],
                        "total": total
                    }
                    sys.stderr.write(f"New best for {username}: {total:.2f} ms\n")
            except Exception as e:
                sys.stderr.write(f"Error processing {file}: {str(e)}\n")
                continue
        
        results = []
        for user, data in user_results.items():
            results.append({
                "user": user,
                "generation": data["generation"],
                "sorting": data["sorting"],
                "total": data["total"]
            })
        
        results.sort(key=lambda x: x["total"])
        
        md = "# 🏆 Таблица лидеров\n\n"
        md += f"Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if results:
            md += "| Место | Пользователь | Генерация (мс) | Сортировка (мс) | Всего (мс) |\n"
            md += "|-------|-------------|----------------|-----------------|------------|\n"
            for i, res in enumerate(results[:10]):
                md += f"| {i+1} | {res['user']} | {res['generation']:.2f} | {res['sorting']:.2f} | **{res['total']:.2f}** |\n"
        else:
            md += "Пока нет результатов!\n"
            
        return md
        
    except Exception as e:
        sys.stderr.write(f"Leaderboard error: {str(e)}\n")
        return f"# Ошибка генерации таблицы\n```\n{str(e)}\n```"

if __name__ == "__main__":
    leaderboard = generate_leaderboard()
    with open("LEADERBOARD.md", "w") as f:
        f.write(leaderboard)
