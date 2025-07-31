import json
import os
import sys

def check_results():
    try:
        if not os.path.exists("result.json"):
            return False
            
        with open('result.json') as f:
            data = json.load(f)
        
        required_fields = ['generation_time', 'sorting_time', 'total_time', 'correctly_sorted']
        for field in required_fields:
            if field not in data:
                return False
                
        if not data['correctly_sorted']:
            return False
            
        return True
        
    except:
        return False

if __name__ == "__main__":
    if not check_results():
        sys.exit(1)
