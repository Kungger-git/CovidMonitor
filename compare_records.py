import os
import pandas as pd

def find_files(file_one, file_two, search_path):
    results = []
    path = os.getcwd() + '/Records/'
    try:
        for root, dir, files in os.walk(path + search_path):
            if file_one and file_two in files:
                results.append(os.path.join(root, file_one))
                results.append(os.path.join(root, file_two))
                dir.append('None')

        for result in results:
            df = pd.read_csv(result)
            pd.set_option('display.max_rows', None)
            print(df)
            print('\n\n')

    except FileNotFoundError as io:
        print('Directory/File has not been found! ', io)
        

first_file = str(input('First File: '))
second_file = str(input('Second File: '))
file_path = str(input('Path:(year/month) '))
find_files(first_file, second_file, file_path)