from datetime import datetime
import os, colorama
import pandas as pd


colorama.init()
now = datetime.now()
month, year = now.strftime('%B'), now.strftime('%Y')
src = os.getcwd() + f'/Records/{year}/{month}/'
try:
    i = 0
    for f in sorted(os.listdir(src))[0:]:
        if os.path.splitext(f)[1] == '.csv':
            i+=1
            df = pd.read_csv(src + f)
            pd.set_option('display.max_rows', None)
            print(f'{df}\n\n')
    print(colorama.Fore.GREEN,
          f'Total of files: {str(i)}\n', colorama.Style.RESET_ALL)
    if i == 218 or i == 219:
        print(colorama.Fore.GREEN,
              '[*] Everything is complete!', colorama.Style.RESET_ALL)
    else:
        print(colorama.Fore.RED,
              '[!] Countries are not complete', colorama.Style.RESET_ALL)
except:
    print("You currently have no records. Execute 'CovidMonitor.py' to create records.")
