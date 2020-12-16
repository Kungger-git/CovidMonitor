import requests
import time
import shutil
import os
from bs4 import BeautifulSoup as soup
from pathlib import Path
from datetime import datetime
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

    # for key in table.options_container:
    #	print(key.capitalize() + '\n')

    #option = input('Select View Options: ')

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

            print('\nCollecting Data...\n')
            time.sleep(1)

            getInfo(page_soup)
            writeFile(source, name_of_file, page_soup, option)

            end = time.time()
            print('\nScraping took ' + convert(end - start) + '\n')

            createChart(page_soup, option)
        except requests.exceptions.RequestException as err:
            print('Something went wrong! ', err)
            with open('Errors.txt', 'a', encoding='utf-8') as f:
                f.write(dt_string_time + ' Searching For: ' +
                        option.capitalize() + ' ' + str(err) + '\n\n')
            if name_of_file in os.listdir(source):
                os.remove(name_of_file)
            main(option)

    transferPhoto(source, option)


def checkFile(src, filename, country):
    record_path = src + 'Records/' + year + '/' + month + '/'
    if not country.casefold() in table.options_container:
        print('\n\nInvalid input\n\nRestarting...')
        time.sleep(2)
        os.system('python CovidMonitor.py')
        quit()
    else:
        if Path(record_path + filename).exists():
            print("\n'" + filename + "' exists.. Proceeding to Data Collection!\n")
        else:
            print("\nFile Created named: '" + filename + "'\n")
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


def createChart(locator, country):
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
            'N/A', '0'), "Recoveries: " + records[2].replace('N/A', '0'), "Active Cases: " + str(active_cases)]
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
                    print(
                        '\n\n' + f + ' has been successfully transferred to:\n' + destination)
            except FileNotFoundError as ioerr:
                print(f, ioerr)


def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d:%02d" % (hour, min, sec)


def getInfo(locator):
    for container in locator.findAll('div', {'class': 'content-inner'})[0:]:
        records = [records.text for records in container.findAll(
            'div', {'class': 'maincounter-number'})[0:]]
        print('{' + dt_string_time + '} | Cases: ' + records[0].strip().replace('N/A', '0') + ' | Deaths: ' + records[1].strip(
        ).replace('N/A', '0') + ' | Recoveries: ' + records[2].strip().replace('N/A', '0'))


if __name__ == '__main__':
    #countries = ['Worldwide', 'Philippines', 'USA', 'India']
    start = time.time()
    for country in table.options_container:
        now = datetime.now()
        year, month = now.strftime('%Y'), now.strftime('%B')
        dt_string, dt_string_time = now.strftime(
            "%B %d-%Y"), now.strftime("%B %d-%Y | %H:%M:%S")
        main(country)
    read_all_records.read()
    end = time.time()
    print('\n\nWhole Program ran for: ' + convert(end-start) + '\n\n')
