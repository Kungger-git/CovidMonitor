import os, shutil


def del_all_records():
    filenames, filepath = [], []
    src = os.getcwd() + '/Records/'    
    try:
        for root, dirs, files in os.walk(src):
            for name in files:
                filepath.append(os.path.join(root, name))
                if name.endswith(('.csv')):
                    filenames.append(name)
                    
        for path in filepath:
            print(path + ' {Will be deleted}')
    
        confirmation = str(
            input('Are you sure you want to delete all existing records?(y/n) '))
        if confirmation.casefold() == 'y' or confirmation.casefold() == 'yes':
            shutil.rmtree(src)        
                    
            if not os.path.isdir(src):
                for filename in filenames[0:]:
                    print("{" + filename + "} has been deleted successfully!")
            else:
                for root, dirs, files in os.walk(src):
                    for name in files:
                        if name.endswith(('.csv')):
                            print("{" + name + "} still exists!")
        else:
            print('\n\nGoodbye!\n')
            quit()
    except FileNotFoundError as io:
        print('Directory/File not Found! ', io)


del_all_records()
