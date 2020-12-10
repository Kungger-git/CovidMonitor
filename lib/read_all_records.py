from datetime import datetime
import pandas as pd
import os


def read():
    now = datetime.now()
    month, year = now.strftime('%B'), now.strftime('%Y')
    src = os.getcwd() + '/Records/' + year + '/' + month + '/'
    try:
        for f in os.listdir(src)[0:]:
            if os.path.splitext(f)[1] == '.csv':
                df = pd.read_csv(src + f)
                pd.set_option('display.max_rows', None)
                print(df)
                print('\n\n')
    except FileNotFoundError as io:
        print('Directory/File Not Found! ', io)
