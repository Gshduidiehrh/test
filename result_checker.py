import json
import os

def check_results():
    try:
        if not os.path.exists("result.json"):
            print("❌ Файл result.json не найден")
            return False
            
        with open('result.json') as f:
            data = json.load(f)
        
        required_fields = ['generation_time', 'sorting_time', 'total_time', 'correctly_sorted']
        for field in required_fields:
            if field not in data:
                print(f"❌ Отсутствует поле: {field}")
                return False
                
        if not data['correctly_sorted']:
            print("❌ Массив не отсортирован правильно")
            return False
            
        print(f"✅ Результаты верны! Генерация: {data['generation_time']} мс, Сортировка: {data['sorting_time']} мс")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка проверки: {str(e)}")
        return False

if __name__ == "__main__":
    check_results()
