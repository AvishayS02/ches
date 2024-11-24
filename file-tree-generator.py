import os


def generate_file_tree(directory, padding="", exclude_files=None, exclude_dirs=None):
    file_tree = ""
    files = sorted(os.listdir(directory))
    pointers = ['├── '] * (len(files) - 1) + ['└── ']

    for pointer, file in zip(pointers, files):
        if exclude_files and file in exclude_files:
            continue
        if exclude_dirs and os.path.isdir(os.path.join(directory, file)) and file in exclude_dirs:
            continue
        file_path = os.path.join(directory, file)
        file_tree += padding + pointer + file + '\n'
        if os.path.isdir(file_path):
            if pointer == '└── ':
                file_tree += generate_file_tree(file_path, padding + '    ', exclude_files, exclude_dirs)
            else:
                file_tree += generate_file_tree(file_path, padding + '│   ', exclude_files, exclude_dirs)
    return file_tree


def list_files_and_contents(directory, exclude_files=None, exclude_dirs=None):
    files_and_contents = ""
    for root, dirs, files in os.walk(directory):
        # Exclude directories based on exclusion list
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if exclude_files and file in exclude_files:
                continue
            file_path = os.path.join(root, file)
            files_and_contents += f"\n{file_path}\n"
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    files_and_contents += f.read() + '\n------------------------------------------------------------------------\n****************************************************************************\n------------------------------------------------------------------------\n'
            except Exception as e:
                files_and_contents += f"Error reading file: {e}\n"
    return files_and_contents


def create_project_summary(directory, output_file, exclude_files=None, exclude_dirs=None):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("File Tree:\n")
        f.write(generate_file_tree(directory, exclude_files=exclude_files, exclude_dirs=exclude_dirs))
        f.write("\nFiles and Their Contents:\n")
        f.write(list_files_and_contents(directory, exclude_files=exclude_files, exclude_dirs=exclude_dirs))


# Get the current working directory
project_directory = os.getcwd()
output_file_name = 'project_summary.txt'
exclude_files_list = ['file-tree-generator.py',
                      'project_summary.txt',
                      'app (2).py',
                      'app.log',
                      'populate_huge_database.py']  # List of files to exclude
exclude_dirs_list = ['__pycache__',
                     '.venv',
                     'node_modules',
                     '.idea',
                     'images',
                     'old',
                     'old 2 (test 1)',
                     'old pm temp to delete']  # List of directories to exclude

# Create the project summary
create_project_summary(project_directory, output_file_name, exclude_files=exclude_files_list,
                       exclude_dirs=exclude_dirs_list)
