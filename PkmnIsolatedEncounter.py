#PkmnIsolatedEncounter created by Dario B. aka Lord of D.
#The Isolated Eencounter Method was coined by the YouTuber 'Austin John Plays'
#For reference/tutorial watch: https://www.youtube.com/watch?v=y9zO9LiFF2Y
#
#This program calculates which areas have the least amount of matches for any given Pokemon (as long as it is available in Scarlet and Violet)
#This is done by automatically accessing and processing data from https://serebii.net
#
#Since their website is subject to change this program might not work in the future
#Also this program might not work for any Pokemon added through DLCs or updates
#I will try to keep this as up to date as possible
#
#Current version released on December 05
#
#Feel free to use this code as is or modify it as long as you credit me. Thanks.

from msvcrt import getch
from bs4 import BeautifulSoup as bs

import requests
import os

from classes import location
from methods import get_type

print('For instructions read the \'read me\' file\n')

name = ''

while name == '':
    print('Enter the name of the Pokemon:\n')
    name = input().lower()

url = 'https://www.serebii.net/pokedex-sv/' + name
html = requests.get(url).text
soup = bs(html, 'html.parser')

locations = []
location_links = []

PATH_INVALID = 'path.txt does not contain a valid path\nText file cannot be saved\n'

if 'Page Not Found' in str(soup):
    print('Page not found - Please try again')

else:
    #get types
    types = get_type(name, soup)
    print(f'{types}\n')

    #get path
    with open('path.txt', 'r') as p:
        path = p.read()#.replace('\\', '/')
        p.close()

    #if path is empty change to default folder
    if path == '':
        path = f'{os.getcwd()}\\Text files'

    elif path[-1] == '\\':
            path = path[:-1]

    else:
        print(PATH_INVALID+'1')

    #get location links
    for link in soup.find_all('a'):
        link = str(link)
        if '/pokearth/paldea/' in link:
            link = 'https://www.serebii.net' + link[link.index('/'):link.index('>')-1]

            if link not in location_links:
                location_links.append(link)

    #create locations and add them to list 'locations'
    counter = 1
    for link in location_links:
        print(f'Processing location {counter}/{len(location_links)}')
        locations.append(location(link, name, types))
        counter += 1

    print('')

    #prepare text for text file and print out matches
    textfile = ''
    
    for loc in locations:
        text = f'{loc.name} has {loc.unique_matches} matches ('
        for i in range(len(types)):
            text += f'{loc.matches[i]} {types[i]}, '
        text = text[:-2] + ')'

        print(text)
        textfile += f'\n{text}'

    #if path is valid
    if os.path.exists(path) or os.access(os.path.dirname(path), os.W_OK):
        try:
            #create path if it doesn't exist
            if not os.path.exists(path):
                os.makedirs(path)

            #write text file
            with open(f'{path}\\{name}.txt', 'w', encoding='utf-8') as f:
                f.write(f'{name}\n{types}\n{textfile}')
                f.close()
        except:
            print(PATH_INVALID+'2')

    else:
        print(PATH_INVALID+'3')
            
#end
print('\nPress any key to close . . .')
getch()