import json
import glob
import os
import sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def generate_leaderboard_image(results):
    print(f"Generating image for {len(results)} results")
    if not results:
        print("No results to display in image")
        return None
    
    img_width = 800
    img_height = 100 + len(results) * 50
    img = Image.new('RGB', (img_width, img_height), color=(40, 44, 52))
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except Exception as e:
        print(f"Font error: {str(e)}")
        sys.exit(1)
    
    draw.text((img_width//2, 30), "🏆 Топ рекордов", fill=(255, 215, 0), font=title_font, anchor="mm")
    draw.text((50, 80), "Место", fill=(100, 149, 237), font=header_font)
    draw.text((150, 80), "Никнейм", fill=(100, 149, 237), font=header_font)
    draw.text((550, 80), "Время (мс)", fill=(100, 149, 237), font=header_font)
    
    draw.line((20, 110, img_width-20, 110), fill=(86, 96, 119), width=2)
    
    y_pos = 130
    for i, res in enumerate(results):
        draw.text((50, y_pos), f"{i+1}", fill=(255, 255, 255), font=font)
        draw.text((150, y_pos), res['user'], fill=(255, 255, 255), font=font)
        draw.text((550, y_pos), f"{res['total']:.2f}", fill=(152, 195, 121), font=font)
        if i < len(results) - 1:
            draw.line((20, y_pos+40, img_width-20, y_pos+40), fill=(65, 72, 92), width=1)
        y_pos += 50
    
    footer = f"Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    draw.text((img_width//2, img_height-30), footer, fill=(128, 128, 128), font=font, anchor="mm")
    
    return img

def generate_leaderboard():
    print("Starting leaderboard generation")
    user_results = {}
    
    print("Searching for result files...")
    result_files = glob.glob("results/*/result.json")
    print(f"Found {len(result_files)} result files")
    
    if not result_files:
        print("No result files found in 'results' directory")
    
    for file in result_files:
        try:
            print(f"Processing file: {file}")
            with open(file) as f:
                data = json.load(f)
            username = os.path.basename(os.path.dirname(file))
            total = data['generation_time'] + data['sorting_time']
            print(f"  User: {username}, Total time: {total:.2f} ms")
            
            if username not in user_results or total < user_results[username]["total"]:
                user_results[username] = {
                    "generation": data["generation_time"],
                    "sorting": data["sorting_time"],
                    "total": total
                }
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")
            continue
    
    results = []
    for user, data in user_results.items():
        results.append({
            "user": user,
            "generation": data["generation"],
            "sorting": data["sorting"],
            "total": data["total"]
        })
    
    if results:
        results.sort(key=lambda x: x["total"])
        top_results = results[:10]
        print(f"Top {len(top_results)} results collected")
    else:
        top_results = []
        print("No valid results collected")
    
    img = generate_leaderboard_image(top_results)
    if img:
        img.save("leaderboard.png")
        print("Saved leaderboard.png")
    
    md = "# 🏆 Таблица лидеров\n\n"
    md += f"Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    if top_results:
        md += "![Leaderboard](leaderboard.png)\n\n"
        md += "| Место | Пользователь | Генерация (мс) | Сортировка (мс) | Всего (мс) |\n"
        md += "|-------|-------------|----------------|-----------------|------------|\n"
        for i, res in enumerate(top_results):
            md += f"| {i+1} | {res['user']} | {res['generation']:.2f} | {res['sorting']:.2f} | **{res['total']:.2f}** |\n"
    else:
        md += "Пока нет результатов!\n"
    
    return md

if __name__ == "__main__":
    leaderboard_md = generate_leaderboard()
    with open("LEADERBOARD.md", "w") as f:
        f.write(leaderboard_md)
    print("Leaderboard generation completed")
