import os


path = os.getcwd()
files = os.listdir()
for file in files:
    if file.endswith('.gif'):
        os.rename(path + r'\\' + file, path + r'\\' + file[:-4] + '.png')