from bs4 import BeautifulSoup as bs

import requests

from methods import get_type

class location():
    def __init__(self, url, pkmn_s, types_s):
        self.__url = url
        self.__html = requests.get(self.__url).text
        self.__soup = bs(self.__html, 'html.parser')

        self.name = str(self.__soup.find('h1'))[4:-5]
        self.pokemon_name_list = []
        self.pokemon_list = []

        self.__pkmn_s = pkmn_s
        self.__types_s = types_s

        self.unique_matches = 0
        self.matches = []

        #create list for counting of matches per type
        for t in self.__types_s:
            self.matches.append(0)

        #get all Pokemon in the area
        for name in self.__soup.find_all('a'):
            name = str(name)
            if 'href=\"#id=' in name:
                name = name[name.rindex('<br/>')+5:-4].lower()

                if name != self.__pkmn_s and name not in self.pokemon_name_list:
                    self.pokemon_name_list.append(name)
                    self.pokemon_list.append(pokemon(name))

        #calculate unique matches (total number of matches)
        for pkmn in self.pokemon_list:
            for t in pkmn.types:
                if t in self.__types_s:
                    self.unique_matches += 1
                    break

        #calculate matches per type
        for pkmn in self.pokemon_list:
            for t in pkmn.types:
                for i in range(len(self.__types_s)):
                    if t == self.__types_s[i]:
                        self.matches[i] += 1


class pokemon():
    def __init__(self, name):
        self.name = name
        
        self.__url = 'https://www.serebii.net/pokedex-sv/' + name.replace(' ', '')
        self.__html = requests.get(self.__url).text
        self.__soup = bs(self.__html, 'html.parser')
        
        self.types = get_type(self.name, self.__soup)