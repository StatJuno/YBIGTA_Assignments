import subprocess
import os
import time
import cowsay

def check_directory_structure(base_path):
    expected_structure = {
        "d1": {
            "d1_1": ["me_1", "me_2"],
            "d1_2": ["essay", "result"]
        },
        "d2": ["check.py", "p1.sh", "requirements.txt"],
        "d3": ["pac.png"]
    }

    def check_sub_structure(current_path, structure):
        for key, value in structure.items():
            path = os.path.join(current_path, key)
            if not os.path.exists(path):
                print(f"Missing directory or file: {path}")
                return False

            if isinstance(value, dict):
                if not os.path.isdir(path):
                    print(f"Expected directory but found file: {path}")
                    return False
                if not check_sub_structure(path, value):
                    return False
            elif isinstance(value, list):
                if not os.path.isdir(path):
                    print(f"Expected directory but found file: {path}")
                    return False
                for item in value:
                    item_path = os.path.join(path, item)
                    if not os.path.exists(item_path):
                        print(f"Missing file: {item_path}")
                        return False
        return True

    return check_sub_structure(base_path, expected_structure)

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def check_numpy_installed():
    result = subprocess.run(['pip', 'show', 'numpy'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return 'Name: numpy' in result.stdout
    
def check_pandas_installed():
    result = subprocess.run(['pip', 'show', 'pandas'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return 'Name: pandas' in result.stdout

def check_cowsay_installed():
    result = subprocess.run(['pip', 'show', 'cowsay'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return 'Name: cowsay' in result.stdout

def read_file_to_string_list(relative_path):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, relative_path)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        content_list = content.split()
        return content_list
    except Exception as e:
        return str(e)


while True:
    if check_directory_structure(base_path):
        print("Tree ZOA!")
    else:
        print("Tree T_T")
    if check_numpy_installed():
        print("Numpy ZOA!")
    else:
        print("Numpy T_T")
    if check_pandas_installed():
        print("Pandas ZOA!")
    else:
        print("Pandas T_T")
    if check_cowsay_installed():
        file_content = read_file_to_string_list('../d1/d1_1/me_1')
        cow_sound = 'Good job, ' + file_content[1] + '!'
        print(cowsay.get_output_string('tux', cow_sound))
    else:
        print("T_T")
    time.sleep(5)