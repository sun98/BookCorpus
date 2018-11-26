import os
import json


def test_para_input():
    test_dir = os.getcwd()
    path = os.path.join(test_dir, 'test_text的副本.txt')
    with open(path, 'r') as f:
        return f.read()
