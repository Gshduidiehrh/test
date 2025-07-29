import json
import os
import sys

def check_results():
    try:
        sys.stderr.write("Checking result.json...\n")
        if not os.path.exists("result.json"):
            sys.stderr.write("❌ Файл result.json не найден\n")
            return False
            
        with open('result.json') as f:
            data = json.load(f)
        
        required_fields = ['generation_time', 'sorting_time', 'total_time', 'correctly_sorted']
        for field in required_fields:
            if field not in data:
                sys.stderr.write(f"❌ Отсутствует поле: {field}\n")
                return False
                
        if not data['correctly_sorted']:
            sys.stderr.write("❌ Массив не отсортирован правильно\n")
            return False
            
        sys.stdout.write(f"✅ Результаты верны! Генерация: {data['generation_time']} мс, Сортировка: {data['sorting_time']} мс\n")
        return True
        
    except json.JSONDecodeError:
        sys.stderr.write("❌ Ошибка формата JSON\n")
        return False
    except Exception as e:
        sys.stderr.write(f"❌ Ошибка проверки: {str(e)}\n")
        return False

if __name__ == "__main__":
    if not check_results():
        sys.exit(1)
