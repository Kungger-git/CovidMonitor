import os, shutil

def del_charts(confirmation):
    images = []
    src = os.getcwd() + '/Covid Pie Charts/'
    if option.casefold() == 'y' or option.casefold() == 'yes':
        try:
            for root, dirs, files in os.walk(src):
                for name in files:
                    if name.endswith(('.png')):
                        images.append(name)


            shutil.rmtree(src)

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
