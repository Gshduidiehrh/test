import os
import json
import glob
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from tabulate import tabulate

def generate_leaderboard():
    print("="*60)
    print("🏆 Starting Code Execution Leaderboard Generation")
    print("="*60)
    
    # Создаем папку для результатов
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    print(f"📂 Results directory: {os.path.abspath(results_dir)}")
    
    # Создаем тестовые данные, если нет реальных
    if not glob.glob(os.path.join(results_dir, "*.json")):
        print("ℹ️ No results found. Creating sample data...")
        sample_data = [
            {"username": "coder42", "generation_time": 15.23, "sorting_time": 25.41, "total_time": 40.64, "correctly_sorted": True},
            {"username": "dev_guru", "generation_time": 12.87, "sorting_time": 28.34, "total_time": 41.21, "correctly_sorted": True},
            {"username": "python_ninja", "generation_time": 18.56, "sorting_time": 22.45, "total_time": 41.01, "correctly_sorted": True},
            {"username": "js_master", "generation_time": 22.12, "sorting_time": 24.78, "total_time": 46.90, "correctly_sorted": False},
            {"username": "algo_king", "generation_time": 10.45, "sorting_time": 30.12, "total_time": 40.57, "correctly_sorted": True}
        ]
        
        for data in sample_data:
            filename = os.path.join(results_dir, f"{data['username']}.json")
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"  ✅ Created sample file: {filename}")
    
    # Собираем все результаты
    all_results = []
    for filepath in glob.glob(os.path.join(results_dir, "*.json")):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
                # Извлекаем никнейм из имени файла, если он не указан в JSON
                if 'username' not in data:
                    username = os.path.splitext(os.path.basename(filepath))[0]
                    data['username'] = username
                
                all_results.append(data)
                print(f"📥 Loaded result: {data['username']} - Total time: {data['total_time']:.2f}s")
        except Exception as e:
            print(f"⚠️ Error processing {filepath}: {str(e)}")
    
    if not all_results:
        print("❌ No valid results found. Aborting leaderboard generation.")
        return
    
    # Сортируем по общему времени выполнения (чем меньше - тем лучше)
    sorted_results = sorted(all_results, key=lambda x: x['total_time'])
    
    # Генерация Markdown таблицы
    leaderboard_md = "# 🏆 Code Execution Leaderboard\n\n"
    leaderboard_md += "Rank | Username | Total Time (s) | Generation (s) | Sorting (s) | Correctly Sorted\n"
    leaderboard_md += "-----|----------|----------------|----------------|-------------|-----------------\n"
    
    for i, result in enumerate(sorted_results, 1):
        status_icon = "✅" if result['correctly_sorted'] else "❌"
        leaderboard_md += (
            f"{i} | {result['username']} | {result['total_time']:.2f} | "
            f"{result['generation_time']:.2f} | {result['sorting_time']:.2f} | "
            f"{status_icon}\n"
        )
    
    # Генерация графика
    if sorted_results:
        usernames = [result['username'] for result in sorted_results]
        total_times = [result['total_time'] for result in sorted_results]
        gen_times = [result['generation_time'] for result in sorted_results]
        sort_times = [result['sorting_time'] for result in sorted_results]
        
        plt.figure(figsize=(14, 8))
        
        # Ширина столбцов
        bar_width = 0.25
        index = np.arange(len(usernames))
        
        # Столбцы для каждого типа времени
        plt.bar(index, gen_times, bar_width, label='Generation Time', color='#3498db')
        plt.bar(index + bar_width, sort_times, bar_width, label='Sorting Time', color='#2ecc71')
        plt.bar(index + 2*bar_width, total_times, bar_width, label='Total Time', color='#e74c3c')
        
        plt.xlabel('Username')
        plt.ylabel('Time (seconds)')
        plt.title('Code Execution Times (Lower is Better)')
        plt.xticks(index + bar_width, usernames)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Добавляем значения на график
        for i in index:
            plt.text(i, gen_times[i] + 0.5, f'{gen_times[i]:.2f}', ha='center')
            plt.text(i + bar_width, sort_times[i] + 0.5, f'{sort_times[i]:.2f}', ha='center')
            plt.text(i + 2*bar_width, total_times[i] + 0.5, f'{total_times[i]:.2f}', ha='center')
        
        plt.tight_layout()
        plt.savefig('leaderboard.png')
        print("\n📊 Generated leaderboard.png visualization")
    
    # Сохраняем результаты в JSON
    with open('leaderboard.json', 'w') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "results": sorted_results
        }, f, indent=2)
    
    # Сохраняем Markdown файл
    with open("LEADERBOARD.md", "w") as f:
        f.write(leaderboard_md)
    
    print("\n" + "="*60)
    print(f"🏁 Leaderboard generation complete! Top performer: {sorted_results[0]['username']}")
    print(f"  - Total time: {sorted_results[0]['total_time']:.2f}s")
    print(f"  - Correctly sorted: {'Yes' if sorted_results[0]['correctly_sorted'] else 'No'}")
    print("="*60)

if __name__ == "__main__":
    generate_leaderboard()
