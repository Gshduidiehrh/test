import json
import glob
import os
import sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def generate_leaderboard_image(results):
    img_width = 800
    img_height = 100 + len(results) * 50
    img = Image.new('RGB', (img_width, img_height), color=(40, 44, 52))
    draw = ImageDraw.Draw(img)
    
    try:
        font_path = "fonts/Roboto-Regular.ttf"
        title_font = ImageFont.truetype(font_path, 36)
        header_font = ImageFont.truetype(font_path, 24)
        font = ImageFont.truetype(font_path, 20)
    except:
        try:
            font_url = "https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Regular.ttf"
            response = requests.get(font_url)
            font_bytes = BytesIO(response.content)
            title_font = ImageFont.truetype(font_bytes, 36)
            header_font = ImageFont.truetype(font_bytes, 24)
            font = ImageFont.truetype(font_bytes, 20)
        except:
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            font = ImageFont.load_default()
    
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
    user_results = {}
    for file in glob.glob("results/*/result.json"):
        try:
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
        except:
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
    top_results = results[:10]
    
    img = generate_leaderboard_image(top_results)
    img.save("leaderboard.png")
    
    md = "# 🏆 Таблица лидеров\n\n"
    md += f"Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    md += "![Leaderboard](leaderboard.png)\n\n"
    
    if results:
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
