import requests
from bs4 import BeautifulSoup as soup


def main():
    name_of_file = 'table.py'
    try:
        req = requests.get(
            'https://www.worldometers.info/coronavirus/', timeout=1
        )
        req.raise_for_status()
        page_soup = soup(req.text, 'html.parser')
        writeLinks(name_of_file, page_soup)
    except requests.exceptions.HTTPError as err:
        print('Something went wrong! ', err)

    print('\n\n----------Successfully Created Python Script----------\n\n')


def writeLinks(filename, locator):
    i = 0
    with open('lib/' + filename, 'w') as f:
        f.write('options_container = {\n')
        f.write("\t\t'worldwide' : '',\n")
        for row in locator.findAll('table', {'id': 'main_table_countries_today'})[0:]:
            for link in row.findAll('a', {'class': 'mt_a'})[0:]:
                i += 1
                country_names = link.text.strip().lower()
                country_links = link['href']
                f.write("\t\t'" + country_names +
                        "' : '" + country_links + "',\n")

        f.write("\t\t'' : 'None'\n\t}")
    print('\nTotal Links of Countries: ' + str(i))


if __name__ == '__main__':
    main()
