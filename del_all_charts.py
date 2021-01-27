import os, shutil


def del_charts():
    images, filepath = [], []
    src = os.getcwd() + '/Covid Pie Charts/'
    try:
        for root, dirs, files in os.walk(src):
            for name in files:
                filepath.append(os.path.join(root, name))
                if name.endswith(('.png')):
                    images.append(name)
            
        for path in filepath:
            print(path + ' {Will be deleted}')

        confirmation = str(
            input('Are you sure you want to delete all existing records?(y/n) '))
        if confirmation.casefold() == 'y' or confirmation.casefold() == 'yes':
            shutil.rmtree(src)

            if not os.path.isdir(src):
                for image in images[0:]:
                    print("{" + image + "} has been deleted successfully!")
            else:
                for root, dirs, files in os.walk(src):
                    for name in files:
                        if name.endswith(('.png')):
                            print("{" + name + "} still exists!")
        else:
            print('\nGoodbye!\n')
            quit()
    except FileNotFoundError as io:
        print('Directory/File Not Found! ', io)
    

del_charts()
