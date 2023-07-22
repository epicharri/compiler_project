import sys
import os

def get_file_path():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return None
    
def file_exists():
    file_path = get_file_path()
    if file_path:
        if os.path.exists(file_path):
            return True
        else:
            print("File does not exist. Goodbye!")
            return False
    else:
        print("Please give a file path as a parameter when calling the program. Goodbye!")
        return False

def read_file_to_string():
    if file_exists():
        with open(get_file_path(), 'r') as file:
            data = file.read()
        return data
    else:
        return None
