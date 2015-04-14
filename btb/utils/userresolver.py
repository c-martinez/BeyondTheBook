'''
Created on Jul 29, 2014

@author: carlosm
'''

import mwclient
import pickle
import os

__DATAFILE__ = 'usernames_LANG.pkl'


def __getAllUsers__(cat):
    '''
    Produce a list of user & subcategories found under the given Category object

    Parameters:
    cat      A mwclient.Category object

    Returns
    users    A list of users registered in the given category
    cats     A list of categories registered in the given category
    '''
    users = []
    cats = []
    for user in cat:
        if user.namespace == 2:    # isUser
            users.append(user)
        elif user.namespace == 14:  # isCategory
            cats.append(user)
        # We just ignore other namespaces
    return users, cats


def __fetchUsersCategory__(cats, log, visited):
    '''
    Fetch all the users on the given seed categories (and their subcategories)

    Parameters:
    cats       seed categories
    log        logging element to keep record of subcategories of each category
    visited    SET of previouly visited categories

    Returns:
    allUsers
    '''
    allUsers = []
    while len(cats) > 0:
        cat = cats.pop()
        if cat.name in visited:
            print '   SKIPPING ', cat.name, ' - previously visited'
        else:
            print 'Fetching ', cat.name, '...'

            catUsers, subCats = __getAllUsers__(cat)
            cats = cats + subCats
            if len(subCats) > 0:
                for subCat in subCats:
                    log.append((cat.name, subCat.name))

            log.append((cat.name, len(catUsers)))
            allUsers = allUsers + catUsers
            visited.add(cat.name)
    return allUsers


def __getCountrySeeds__(lang='en'):
    '''
    Return seed country categories (manually defined). These seeds correspond to the
    subcategories listed on Wikipedians_by_location category and Wikipedians_by_ethnicity_and_nationality,
    for highest contributing countries.

    For lang='en', Wikipedians_by_location category found here:
        http://en.wikipedia.org/wiki/Category:Wikipedians_by_location
        http://en.wikipedia.org/wiki/Category:Wikipedians_by_ethnicity_and_nationality

    Highest contributing countries found here:
        http://stats.wikimedia.org/wikimedia/squids/SquidReportPageEditsPerLanguageBreakdown.htm

    For lang='nl', Wikipedia:Gebruiker_nl-M category found here:
        http://nl.wikipedia.org/wiki/Categorie:Wikipedia:Gebruiker_nl-M

    Parameter:
    lang     Language Wikipedia for which categories are requested. (Default: english)
    '''
    countrySeeds = {}
    if lang == 'en':
        countrySeeds["US"] = ["Wikipedians in U.S.A.", "Wikipedians in United States", "Wikipedians in United States Of America",
                              "Wikipedians in United States of America", "Wikipedians in US", "Wikipedians in USA",
                              "Wikipedians in the United States", "Wikipedians in the United States of America",
                              "American Wikipedians"]
        countrySeeds["UK"] = ["Wikipedians in UK", "Wikipedians in United Kingdom", "Wikipedians in the United Kingdom",
                              "Wikipedians in the UK", "British Wikipedians"]
        countrySeeds["IN"] = ["Wikipedians in India", "Wikipedians in the India", "Wikipedians in the Republic of INDIA",
                              "Indian Wikipedians"]
        countrySeeds["CA"] = ["Wikipedians in Canada", "Canadian Wikipedians"]
        countrySeeds["AU"] = ["Wikipedians in the Australia", "Wikipedians in AUSTRALIA", "Wikipedians in Australia",
                              "Australian Wikipedians"]
        countrySeeds["PH"] = ["Wikipedians in the Philippines",
                              "Wikipedians in Philippines", "Filipino Wikipedians"]
        countrySeeds["DE"] = ["Wikipedians in Germany", "German Wikipedians"]
        countrySeeds["BR"] = ["Wikipedians in Brazil", "Brazilian Wikipedians"]
        countrySeeds["IT"] = ["Wikipedians in Italy", "Italian Wikipedians"]
        countrySeeds["IE"] = ["Wikipedians in Ireland", "Wikipedians in the Republic of Ireland",
                              "Irish Wikipedians", "Scotch-Irish Wikipedians"]
        countrySeeds["PK"] = ["Wikipedians in Pakistan",
                              "Wikipedians in the Pakistan", "Pakistani Wikipedians"]
        countrySeeds["FR"] = ["Wikipedians in France", "French Wikipedians"]
        countrySeeds["MY"] = [
            "Wikipedians in Malaysia", "Malaysian Wikipedians"]
        countrySeeds["NL"] = [
            "Wikipedians in the Netherlands", "Dutch Wikipedians"]
        countrySeeds["ID"] = [
            "Wikipedians in Indonesia", "Indonesian Wikipedians"]
        countrySeeds["CN"] = ["Wikipedians in China", "Wikipedians in Mainland China",
                              "Wikipedians in the People's Republic of China", "Wikipedians in the People's Republic of China/",
                              "Wikipedians in the Republic of China", "Chinese Wikipedians"]
        countrySeeds["NZ"] = ["Wikipedians in New Zealand"]
        countrySeeds["ES"] = [
            "Wikipedians in Spain", "Wikipedians in in Spain", "Spanish Wikipedians"]
        countrySeeds["IR"] = [
            "Wikipedians in the Iran", "Wikipedians in Iran", "Iranian Wikipedians"]
        countrySeeds["MX"] = ["Wikipedians in Mexico", "Mexican Wikipedians"]
        countrySeeds["SE"] = ["Wikipedians in Sweden", "Swedish Wikipedians"]
        countrySeeds["RU"] = ["Wikipedians in Russia", "Russian Wikipedians"]
        countrySeeds["GR"] = ["Wikipedians in Greece", "Greek Wikipedians"]
        countrySeeds["TR"] = ["Wikipedians in Turkey", "Turkish Wikipedians"]
    elif lang == 'nl':
        countrySeeds["NL"] = ["Wikipedia:Gebruiker nl-M"]
    return countrySeeds


def __fetchData__(lang='en'):
    '''
    Use Wikimedia API to download a list of users from the given seed categories
    for selected countries. User country resolution will be limited to the selected countries
    and users in each country will be limited to users in one of the seed categories
    (or its subcategories) given for each country.

    Downloaded data is preserved to __DATAFILE__ pickle file

    Parameters:
    lang      Language of Wikipedia site from which user data is downloaded.

    Returns:
    Usernames   A dictionary of countries -> sets, where the entry of a given country,
                contains a Set of users registered on that country.
    log         A list of parent-child tuples, where the parent indicates a given category
                explored, and the child represents a sub-category found for the given parent.
    '''
    wiki = mwclient.Site(lang + '.wikipedia.org')
    countrySeeds = __getCountrySeeds__(lang)

    log = []      # Log records parent-child tuples
    users = {}
    visited = set()

    for country in countrySeeds:
        seeds = countrySeeds[country]
        cats = [wiki.Categories[seed] for seed in seeds]
        log = log + [(country, seed) for seed in seeds]
        users[country] = __fetchUsersCategory__(cats, log, visited)

    usernameSets = {}
    for country in users:
        usernameSets[country] = set()
        for user in users[country]:
            usernameSets[country].add(user.name)

    return usernameSets, log


def __loadData__(lang='en'):
    '''
    Load data from existing pickled __DATAFILE__.
    Different file used for each language Wikipedia.

    Returns:
    Usernames   A dictionary of countries -> sets, where the entry of a given country,
                contains a Set of users registered on that country.
    log         A list of parent-child tuples, where the parent indicates a given category
                explored, and the child represents a sub-category found for the given parent.
    '''
    path = os.path.dirname(__file__)
    dataFile = path + '/' + __getDataFileName__(lang)
    usernameSets, log = pickle.load(open(dataFile, 'r'))
    return usernameSets, log


def getUserCountry(user, lang='en'):
    '''
    Search for the given username and return its country code.

    user    Wikipedia username.
    lang    Language of Wikipedia (default: english)

    Returns
    The country of the given user (or None, if no country information is known).
    '''
    if lang == 'en':
        uUser = 'User:' + user
    elif lang == 'nl':
        uUser = 'Gebruiker:' + user
    else:
        uUser = user

    userMap, log = __getUserMap__(lang)
    for country in userMap:
        if uUser in userMap[country]:
            return country
    return None


def __getDataFileName__(lang):
    '''
    Retrieve the name of the pickle file to be used for the given
    language category.

    Parameters:
    lang     Language of the pickle file.
    '''
    return __DATAFILE__.replace('LANG', lang)


def __getUserMap__(lang):
    '''
    Load the pickled user names the first time they are required.
    If no pickle file exists, a fresh one is generated.

    Parameters:
    lang      Language of the usernames to be loaded

    Returns:
    Usernames   A dictionary of countries -> sets, where the entry of a given country,
                contains a Set of users registered on that country.
    log         A list of parent-child tuples, where the parent indicates a given category
                explored, and the child represents a sub-category found for the given parent.
    '''
    if lang in __langUserMaps__:
        usernameSets, log = __langUserMaps__[lang]
        return usernameSets, log
    else:
        try:
            usernameSets, log = __loadData__(lang)
            __langUserMaps__[lang] = (usernameSets, log)
            return usernameSets, log
        except:
            dataFile = __getDataFileName__(lang)
            print 'Unable to find ' + dataFile + ' -- new one will be created'
            usernameSets, log = __fetchData__(lang)
            print 'Preserving data to ' + dataFile + '...'
            path = os.path.dirname(__file__)
            dataFile = path + '/' + dataFile
            pickle.dump((usernameSets, log), open(dataFile, 'w'))
            __langUserMaps__[lang] = (usernameSets, log)
        return usernameSets, log

# When module is first loaded, init language maps...
__langUserMaps__ = {}

if __name__ == '__main__':
    assert getUserCountry('Alaney2k') == 'CA'  # Random canadian user
