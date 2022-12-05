def get_type(name, soup):
    types = []

    if 'tauros' in name:
        types = ['fighting', 'fire', 'water']

    elif 'wooper' in name:
        types = ['poison', 'ground']

    else:
        for t in soup.find_all('a'):
            t = str(t)

            if '/pokedex-bw/type/' in t and 'loading=' in t and ('class=\"typeimg\"' in t or 'border=\"0\"' in t):
                t = t[21:t.index('.')]

                if t in types:
                    break

                else:
                    types.append(t)

    return types