import json
import glob
import os

def generate_leaderboard():
    print("Generating leaderboard...")
    results = []
    result_files = glob.glob("results/**/result.json", recursive=True)
    print(f"Found {len(result_files)} result files")
    
    for file in result_files:
        try:
            username = os.path.basename(os.path.dirname(file))
            print(f"Processing {username}'s results")
            
            with open(file) as f:
                data = json.load(f)
                
            total = data['generation_time'] + data['sorting_time']
            results.append({
                "user": username,
                "generation": data["generation_time"],
                "sorting": data["sorting_time"],
                "total": total
            })
            print(f"Added {username}: {total:.2f} ms")
            
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")
    
    if not results:
        return "# 🏆 Таблица лидеров\n\nПока никаких результатов!"
    
    results.sort(key=lambda x: x["total"])
    
    md = "# 🏆 Таблица лидеров\n\n"
    md += "| Место | Пользователь | Генерация (мс) | Сортировка (мс) | Всего (мс) |\n"
    md += "|-------|-------------|----------------|-----------------|------------|\n"
    
    for i, res in enumerate(results[:10]):
        md += f"| {i+1} | {res['user']} | {res['generation']:.2f} | {res['sorting']:.2f} | **{res['total']:.2f}** |\n"
    
    return md

if __name__ == "__main__":
    leaderboard = generate_leaderboard()
    with open("LEADERBOARD.md", "w") as f:
        f.write(leaderboard)
