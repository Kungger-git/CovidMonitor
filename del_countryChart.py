import os, shutil, errno


def delete_country(folder):
    src = os.getcwd() + '/Covid Pie Charts/'

    if folder in os.listdir(src):
        shutil.rmtree(src + folder + '/')
        if not folder in os.listdir(src):
            print(folder + ' has been deleted')
        else:
            print(folder + ' still exists')
    else:
        raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), folder)


rem_folder = str(input('Input folder: '))
delete_country(rem_folder)
