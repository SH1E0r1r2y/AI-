import sys
import os
import glob
import myver as myver


def read_txt_files_in_directory(directory_path):
    html_input = ""
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, "r") as file:
                html_input += file.read() + "\n"
    return html_input


def get_multiline_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip() == ':wq':
            break
        lines.append(line)
    return '\n'.join(lines)


def read_file_content(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# data_flist = glob.glob("./data/data/*.txt")


# for f in data_flist:
with open("weeeb/data/filtered_data.txt", mode="r") as f:
    # infile = read_file_content(f)
    print(f"{f}:")
    myver.feed(f)

# while True:
#     if not query:
#         query = input("Prompt: ")
#     if query in ['quit', 'q', 'exit']:
#         sys.exit()
