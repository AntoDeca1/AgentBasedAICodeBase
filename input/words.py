import os

path = os.path.join(os.path.abspath('./'), 'input/italian.txt')

words = []
with open(path, 'r') as file:
    for word in file.readlines():
        x = word.replace('\n', '')
        x = x.lower()
        words.append(x)
