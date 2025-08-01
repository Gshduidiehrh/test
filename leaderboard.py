import os
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time
import sys

def generate_leaderboard():
    # Создаем абсолютные пути
    current_dir = os.getcwd()
    results_dir = os.path.join(current_dir, "results")
    results_file = os.path.join(results_dir, "results.json")
    
    print(f"\n{'='*50}")
    print("Starting leaderboard generation")
    print(f"Current directory: {current_dir}")
    print(f"Results directory: {results_dir}")
    
    # Создаем папку результатов
    os.makedirs(results_dir, exist_ok=True)
    print(f"Directory exists: {os.path.exists(results_dir)}")
    
    # Создаем тестовый файл для проверки записи
    test_file = os.path.join(results_dir, "test.txt")
    try:
        with open(test_file, "w") as f:
            f.write("Test content at " + datetime.now().isoformat())
        print(f"Test file created: {test_file}")
    except Exception as e:
        print(f"Error creating test file: {e}")
    
    # Проверяем существование тестового файла
    print(f"Test file exists: {os.path.exists(test_file)}")
    
    # Ищем существующие JSON файлы
    json_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
    print(f"Found JSON files: {json_files}")
    
    # Если файлов нет - создаем начальный
    if not json_files:
        print("No JSON files found. Creating initial.json")
        initial_data = {"user1": 100, "user2": 85}
        with open(os.path.join(results_dir, "initial.json"), "w") as f:
            json.dump(initial_data, f)
        json_files = ["initial.json"]
    
    # Обрабатываем все JSON файлы
    all_data = {}
    for file_name in json_files:
        file_path = os.path.join(results_dir, file_name)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                print(f"Processing {file_name}: {len(data)} entries")
                
                # Объединяем данные
                for user, score in data.items():
                    if user not in all_data or score > all_data[user]:
                        all_data[user] = score
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
    
    print(f"Total users: {len(all_data)}")
    
    # Сортируем пользователей по баллам
    sorted_users = sorted(all_data.items(), key=lambda x: x[1], reverse=True)
    
    # Генерация Markdown таблицы
    leaderboard_md = "# Leaderboard\n\n"
    leaderboard_md += "| User | Score |\n"
    leaderboard_md += "|------|-------|\n"
    
    for user, score in sorted_users:
        leaderboard_md += f"| {user} | {score} |\n"
    
    # Генерация графика
    if sorted_users:
        users, scores = zip(*sorted_users)
        plt.figure(figsize=(12, 6))
        plt.bar(users, scores, color='skyblue')
        plt.title("Leaderboard Scores")
        plt.ylabel("Score")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig("leaderboard.png")
        print("Generated leaderboard.png")
    
    # Сохраняем объединенные результаты
    with open(results_file, "w") as f:
        json.dump(all_data, f, indent=2)
    print(f"Saved results to: {results_file}")
    
    # Принудительная синхронизация
    sys.stdout.flush()
    os.sync()
    time.sleep(1)  # Даем время для записи
    
    print(f"File exists: {os.path.exists(results_file)}")
    print(f"File size: {os.path.getsize(results_file)} bytes")
    print("Leaderboard generation complete")
    print('='*50)
    
    return leaderboard_md

if __name__ == "__main__":
    # Генерируем и сохраняем лидерборд
    leaderboard_md = generate_leaderboard()
    
    # Сохраняем Markdown файл
    with open("LEADERBOARD.md", "w") as f:
        f.write(leaderboard_md)
    print("LEADERBOARD.md updated")
    
    # Дополнительная проверка
    print("\nFinal directory contents:")
    print(f"LEADERBOARD.md: {os.path.exists('LEADERBOARD.md')}")
    print(f"leaderboard.png: {os.path.exists('leaderboard.png')}")
    print(f"results/results.json: {os.path.exists('results/results.json')}")
