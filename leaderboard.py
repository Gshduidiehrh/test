import os
import json
import glob
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def generate_leaderboard():
    # Убедимся, что папка results существует
    os.makedirs("results", exist_ok=True)
    
    # Диагностика: выводим содержимое папки results
    print("Current directory:", os.getcwd())
    print("Results contents:", os.listdir("results"))
    
    # Ищем все JSON файлы в папке results
    json_files = glob.glob("results/*.json")
    print("Found JSON files:", json_files)
    
    if not json_files:
        print("No JSON files found. Creating initial data.")
        initial_data = {"initial_user": 100}
        with open("results/initial.json", "w") as f:
            json.dump(initial_data, f)
        json_files = ["results/initial.json"]
    
    all_data = {}
    
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                print(f"Processing {json_file}: {data}")
                
                # Объединяем данные (берем максимальный балл для каждого пользователя)
                for user, score in data.items():
                    if user not in all_data or score > all_data[user]:
                        all_data[user] = score
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
    
    # Сортируем пользователей по баллам
    sorted_users = sorted(all_data.items(), key=lambda x: x[1], reverse=True)
    
    # Генерация Markdown таблицы
    leaderboard_md = "# Leaderboard\n\n"
    leaderboard_md += "| User | Score |\n"
    leaderboard_md += "|------|-------|\n"
    
    for user, score in sorted_users:
        leaderboard_md += f"| {user} | {score} |\n"
    
    # Генерация графика (пример)
    if sorted_users:
        users, scores = zip(*sorted_users)
        plt.figure(figsize=(10, 6))
        plt.bar(users, scores)
        plt.title("Leaderboard")
        plt.ylabel("Score")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("leaderboard.png")
        print("Generated leaderboard.png")
    
    # Сохраняем объединенные результаты
    with open("results/results.json", "w") as f:
        json.dump(all_data, f)
    
    return leaderboard_md

if __name__ == "__main__":
    leaderboard_md = generate_leaderboard()
    with open("LEADERBOARD.md", "w") as f:
        f.write(leaderboard_md)
    print("LEADERBOARD.md updated")
