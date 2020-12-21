import requests
import time
import shutil
import os
import colorama
from bs4 import BeautifulSoup as soup
from datetime import datetime
from collections import OrderedDict
import matplotlib.pyplot as plt
import pandas as pd
from lib import table
from lib import read_all_records


def main(option):
    source = os.getcwd() + '/'
    for f in os.listdir(source):
        if os.path.splitext(f)[1] == '.png':
            os.remove(f)
        if os.path.splitext(f)[1] == '.csv':
            os.remove(f)

    name_of_file = option.capitalize() + '.csv'
    checkFile(source, name_of_file, option)

    if option.casefold() in table.options_container:
        # Grab connection and Parse HTML
        try:
            start = time.time()
            print('\n\nSending Request...\n')
            ref_req = 'https://www.worldometers.info/coronavirus/' + \
                table.options_container.get(option.casefold())
            req = requests.get(
                ref_req.replace("'", '').replace('None', ''), timeout=1
            )
            req.raise_for_status()
            page_soup = soup(req.text, "html.parser")

            getInfo(page_soup)
            writeFile(source, name_of_file, page_soup, option)

            end = time.time()
            print(colorama.Fore.GREEN, '\nScraping took ' +
                  convert(end - start) + '\n', colorama.Style.RESET_ALL)
        except requests.exceptions.RequestException as err:
            print(colorama.Fore.RED, 'Something went wrong! ',
                  err, colorama.Style.RESET_ALL)
            with open('Errors.txt', 'a', encoding='utf-8') as f:
                f.write(dt_string_time + ' Searching For: ' +
                        option.capitalize() + ' ' + str(err) + '\n\n')
            if name_of_file in os.listdir(source):
                os.remove(name_of_file)
            main(option)


def checkFile(src, filename, country):
    record_path = src + 'Records/' + year + '/' + month + '/'
    if not country.casefold() in table.options_container:
        print(colorama.Fore.RED, '\n\nInvalid input\n\nRestarting...',
              colorama.Style.RESET_ALL)
        time.sleep(2)
        os.system('python CovidMonitor.py')
        quit()
    else:
        if os.path.exists(record_path + filename):
            print(colorama.Fore.LIGHTYELLOW_EX, "\n'" + filename +
                  "' exists.. Proceeding to Data Collection!\n", colorama.Style.RESET_ALL)
        else:
            print(colorama.Fore.LIGHTYELLOW_EX, "\nFile Created named: '" +
                  filename + "'\n", colorama.Style.RESET_ALL)
            with open(filename, 'w', encoding='utf-8') as f:
                headers = "Country, Date, Cases, Deaths, Recoveries, Active Cases\n"
                f.write(headers)


def writeFile(src, filename, locator, country):
    dst = src + 'Records/' + year + '/' + month + '/'

    # if destination folder does not exist, Create directory
    if not os.path.exists(dst):
        os.makedirs(dst)

    def scrape_write(pointer):
        with open(pointer + filename, 'a', encoding='utf-8') as f:
            # Write all contents
            for container in locator.findAll('div', {'class': 'content-inner'})[0:]:
                records = [records.text.strip().replace(',', '') for records in container.findAll(
                    'div', {'class': 'maincounter-number'})[0:]]

                total_cases = records[0].replace('N/A', '0')
                total_deaths = records[1].replace('N/A', '0')
                total_recoveries = records[2].replace('N/A', '0')
                active_cases = int(total_cases) - \
                    int(total_recoveries) - int(total_deaths)

                f.write(country.capitalize() + ', ' + dt_string + ', ' +
                        total_cases + ', ' + total_deaths + ', ' + total_recoveries + ', ' + str(active_cases) + '\n')
            f.close()
            # Listing all Data from csv file in Console
            update = pd.read_csv(pointer + filename, encoding='utf-8')
            pd.set_option('display.max_rows', None)
            print('\n\nUpdated Data Frame:\n')
            print(update)

    if os.path.exists(dst + filename):
        scrape_write(dst)
    else:
        scrape_write(src)

    if not os.path.exists(dst + filename):
        # move .csv file
        for f in os.listdir(src)[0:]:
            if os.path.splitext(f)[1] == '.csv':
                shutil.move(src + f, dst)

    createChart(src, locator, country)


def createChart(src, locator, country):
    colors = ['#66b3ff', '#ff9999', '#99ff99', '#f98aff']
    for container in locator.findAll('div', {'class': 'content-inner'})[0:]:
        records = [records.text.strip() for records in container.findAll(
            'div', {'class': 'maincounter-number'})[0:]]
        plt.figure(figsize=(6, 3))
        plt.gcf().canvas.set_window_title('Coronavirus ' + country.capitalize() + ' View')

        total_cases = records[0].replace(',', '').replace('N/A', '0')
        total_deaths = records[1].replace(',', '').replace('N/A', '0')
        total_recoveries = records[2].replace(',', '').replace('N/A', '0')
        active_cases = int(total_cases) - \
            int(total_deaths) - int(total_recoveries)

        labels = ["Cases: " + records[0].replace('N/A', '0'), "Deaths: " + records[1].replace(
            'N/A', '0'), "Recoveries: " + records[2].replace('N/A', '0'), "Active Cases: " + str(":,".format(active_cases))]
        values = [total_cases, total_deaths, total_recoveries, active_cases]
        explode = (0.05, 0.05, 0.05, 0.05)

        plt.pie(values, colors=colors, startangle=90, shadow=True,
                explode=explode, pctdistance=0.85, autopct='%1.1f%%')
        plt.legend(labels=labels)
        plt.xlabel('Date: ' + dt_string)

        center_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)

        plt.axis('equal')
        plt.title(country.capitalize() + ' Coronavirus Chart')
        plt.savefig(dt_string + '__' + country.capitalize() +
                    '.png', bbox_inches='tight')

        # plt.show(block=False)
        # plt.pause(1)
        plt.close()

    transferPhoto(src, country)


def transferPhoto(src, country):
    destination = src + "Covid Pie Charts/" + country.capitalize() + "/" + year + \
        "/" + month + "/"

    # If directory/Month does not exist, create new directory
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Transfer Image to Destination Directory
    for f in os.listdir(src)[0:]:
        if os.path.splitext(f)[1] == '.png':
            shutil.move(src + f, destination)

            # check if file has been transferred successfully
            try:
                if os.path.exists(destination + f):
                    print(colorama.Fore.GREEN,
                          '\n\n' + f + ' has been successfully transferred to:\n' + destination, colorama.Style.RESET_ALL)
            except FileNotFoundError as ioerr:
                print(colorama.Fore.RED, f, ioerr, colorama.Style.RESET_ALL)


def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d:%02d" % (hour, min, sec)


def getInfo(locator):
    for container in locator.findAll('div', {'class': 'content-inner'})[0:]:
        records = [records.text for records in container.findAll(
            'div', {'class': 'maincounter-number'})[0:]]
        print(colorama.Fore.LIGHTMAGENTA_EX, '{' + dt_string_time + '} | Cases: ' + records[0].strip().replace('N/A', '0') + ' | Deaths: ' + records[1].strip(
        ).replace('N/A', '0') + ' | Recoveries: ' + records[2].strip().replace('N/A', '0'), colorama.Style.RESET_ALL)


if __name__ == '__main__':
    #countries = ['Worldwide', 'Philippines', 'USA', 'India']
    #for key in table.options_container:
    #   print(key.capitalize() + '\n')

    #option = input('Select View Options: ')
    start = time.time()
    i = 0
    colorama.init()
    sorted_dict = OrderedDict(sorted(table.options_container.items()))
    total_countries = len(sorted_dict)
    for country in sorted_dict:
        i += 1
        print(colorama.Fore.CYAN, '\n' + str(i) + ' of ' +
              str(total_countries) + '\n', colorama.Style.RESET_ALL)
        now = datetime.now()
        year, month = now.strftime('%Y'), now.strftime('%B')
        dt_string, dt_string_time = now.strftime(
            "%B %d-%Y"), now.strftime("%B %d-%Y | %H:%M:%S")
        main(country)
    end = time.time()
    read_all_records.read()
    print(colorama.Fore.GREEN, '\n\nWhole Program ran for: ' +
          convert(end-start) + '\n\n', colorama.Style.RESET_ALL)
