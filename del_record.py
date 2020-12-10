import os

def delete_record(filename, search_path):
    src = os.getcwd() + '/Records/' + search_path

    if filename in os.listdir(src):
        os.remove(src + filename)
        if not filename in os.listdir(src):
            print(filename + ' has been deleted')
        else:
            print(filename + ' has not been deleted')
    else:
        raise FileNotFoundError(filename + ' does not exist.')

rem_file = str(input('Input filename: '))
file_path = str(input('Path:(year/month) '))
delete_record(rem_file, file_path)
