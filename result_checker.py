import json
import os
import sys

def check_results():
    try:
        if not os.path.exists("result.json"):
            sys.stderr.write("result.json not found\n")
            return False
            
        with open('result.json') as f:
            data = json.load(f)
        
        required_fields = ['generation_time', 'sorting_time', 'total_time', 'correctly_sorted']
        for field in required_fields:
            if field not in data:
                sys.stderr.write(f"Missing field: {field}\n")
                return False
                
        if not data['correctly_sorted']:
            sys.stderr.write("Array not sorted correctly\n")
            return False
            
        return True
        
    except Exception as e:
        sys.stderr.write(f"Validation error: {str(e)}\n")
        return False

if __name__ == "__main__":
    if not check_results():
        sys.exit(1)
