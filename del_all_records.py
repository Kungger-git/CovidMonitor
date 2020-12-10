import os, shutil


def del_all_records(confirmation):
    filenames, filepath = [], []
    src = os.getcwd() + '/Records/'
    if confirmation.casefold() == 'y' or confirmation.casefold() == 'yes':
        try:
            for root, dirs, files in os.walk(src):
                for name in files:
                    filepath.append(os.path.join(root, name))
                    if name.endswith(('.csv')):
                        filenames.append(name)

            shutil.rmtree(src)
            for path in filepath:
                print(path + ' {Will be deleted}')

            if not os.path.isdir(src):
                for filename in filenames[0:]:
                    print("{" + filename + "} has been deleted successfully!")
            else:
                for root, dirs, files in os.walk(src):
                    for name in files:
                        if name.endswith(('.csv')):
                            print("{" + name + "} still exists!")
        except FileNotFoundError as io:
            print('Directory/File not Found! ', io)
    else:
        print('\nGoodbye!\n')
        quit()


option = str(
    input('Are you sure you want to delete all existing records?(y/n) '))
del_all_records(option)
