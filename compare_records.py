import os
import pandas as pd


def find_files(file_one, file_two, search_path):
    results = []
    path = os.getcwd() + '/Records/'
    csv_one = file_one + '.csv'
    csv_two = file_two + '.csv'
    if os.path.isdir(path + search_path):
        try:
            for root, dir, files in os.walk(path + search_path):
                if csv_one and csv_two in files:
                    results.append(os.path.join(root, csv_one))
                    results.append(os.path.join(root, csv_two))
                    dir.append('None')
                else:
                    raise FileNotFoundError(
                        'Neither {' + csv_one + ' or ' + csv_two + '} exists in Records Library.')

            for result in results:
                df = pd.read_csv(result)
                pd.set_option('display.max_rows', None)
                print(df)
                print('\n\n')

        except FileNotFoundError as io:
            print('Directory/File has not been found! ', io)
    else:
        raise FileNotFoundError('{' + search_path + '} is not a directory.')


first_file = str(input('First Country: '))
second_file = str(input('Second Country: '))
file_path = str(input('Path:(year/month) '))

find_files(first_file, second_file, file_path)
