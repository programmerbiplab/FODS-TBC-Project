# file_handler.py

import os

DATA_PATH = "data"

def ensure_file(path):
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
    if not os.path.exists(path):
        open(path, 'w').close()

def read_file(filename):
    path = os.path.join(DATA_PATH, filename)
    ensure_file(path)
    with open(path, "r") as file:
        return [line.strip() for line in file.readlines()]

def write_file(filename, lines):
    path = os.path.join(DATA_PATH, filename)
    ensure_file(path)
    with open(path, "w") as file:
        file.writelines([line + "\n" for line in lines])

def append_file(filename, line):
    path = os.path.join(DATA_PATH, filename)
    ensure_file(path)
    with open(path, "a") as file:
        file.write(line + "\n")
