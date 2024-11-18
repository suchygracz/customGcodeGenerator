import os

def count_lines(directory):
    total_lines = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        stripped_line = line.strip()
                        # Ignore blank lines and lines starting with a comment
                        if stripped_line and not stripped_line.startswith("#"):
                            total_lines += 1
    return total_lines

project_directory = r'B:\allCodingRelated\cGg'
total_lines = count_lines(project_directory)
print(f'Total lines of Python code: {total_lines}')
