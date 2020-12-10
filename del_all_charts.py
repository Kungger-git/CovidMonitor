import os, shutil

def del_charts(confirmation):
    images = []
    filepath = []
    src = os.getcwd() + '/Covid Pie Charts/'
    if confirmation.casefold() == 'y' or confirmation.casefold() == 'yes':
        try:
            for root, dirs, files in os.walk(src):
                for name in files:
                    filepath.append(os.path.join(root, name))
                    if name.endswith(('.png')):
                        images.append(name)

            shutil.rmtree(src)
            for path in filepath:
                print(path + ' Will be deleted')
                
            if not os.path.isdir(src):
                for image in images[0:]:
                    print("{" + image + "} has been deleted successfully!")
            else:
                for root, dirs, files in os.walk(src):
                    for name in files:
                        if name.endswith(('.png')):
                            print("{" + name + "} still exists!")
        except FileNotFoundError as io:
            print('Directory/File Not Found! ', io)
    else:
        print('\nGoodbye!\n')
        quit()


option = str(input('Are you sure you want to delete all existing records?(y/n) '))
del_charts(option)