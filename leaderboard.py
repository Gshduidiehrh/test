import json
import glob
import os
import sys
from datetime import datetime

def generate_leaderboard():
    try:
        user_results = {}
        result_count = 0
        
        for result_file in glob.glob("results/*/result.json"):
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)
                
                username = os.path.basename(os.path.dirname(result_file))
                total_time = data['generation_time'] + data['sorting_time']
                

                if username not in user_results or total_time < user_results[username]['total']:
                    user_results[username] = {
                        'generation': data['generation_time'],
                        'sorting': data['sorting_time'],
                        'total': total_time
                    }
                    result_count += 1
                    
            except Exception as e:
                sys.stderr.write(f"Error processing {result_file}: {str(e)}\n")
        
        sys.stderr.write(f"Processed {result_count} results from {len(user_results)} users\n")
        results = [
            {
                'user': user,
                'generation': data['generation'],
                'sorting': data['sorting'],
                'total': data['total']
            }
            for user, data in user_results.items()
        ]
        results.sort(key=lambda x: x['total'])
        
    
        md = "# 🏆 Таблица лидеров\n\n"
        md += f"Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if results:
            md += "| Место | Пользователь | Генерация (мс) | Сортировка (мс) | Всего (мс) |\n"
            md += "|-------|-------------|----------------|-----------------|------------|\n"
            
            for i, res in enumerate(results[:20]):
                md += f"| {i+1} | {res['user']} | {res['generation']:.2f} | {res['sorting']:.2f} | **{res['total']:.2f}** |\n"
        else:
            md += "Пока нет результатов!\n"
        
        return md
        
    except Exception as e:
        import traceback
        sys.stderr.write(f"Critical error: {str(e)}\n{traceback.format_exc()}")
        return f"# Ошибка генерации таблицы\n```\n{str(e)}\n```"

if __name__ == "__main__":
    leaderboard = generate_leaderboard()
    with open("LEADERBOARD.md", "w") as f:
        f.write(leaderboard)
