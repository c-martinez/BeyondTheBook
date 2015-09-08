'''
Created on Aug 5, 2014

@author: carlosm
'''

'''
Percentage of contribution from each country to the total number of edits in english Wikipedia.
Taken from http://stats.wikimedia.org/wikimedia/squids/SquidReportPageEditsPerLanguageBreakdown.htm
Generated on Thu, Jan 8, 2015 21:01 (bottom of page)
'''
__totalEdits__ = {
    'en': {
        'US':  0.367,
        'UK':  0.131,
        'IN':  0.067,
        'CA':  0.054,
        'AU':  0.031,
        'PH':  0.024,
        'DE':  0.015,
        'BR':  0.012,
        'NL':  0.011,
        'PK':  0.010,
        'IT':  0.010,
        'FR':  0.009,
        'MY':  0.009,
        'IE':  0.009,
        'ID':  0.008,
        'ES':  0.007,
        'PT':  0.006,
        'MX':  0.006,
        'TR':  0.006,
        'GR':  0.006,
        'NZ':  0.005,
        'SE':  0.005,
        'TH':  0.005,
        'IL':  0.005,
        'SG':  0.005,
        'CN':  0.004,# China and Russia disappeared! So I'll assume they dropped below 0.5%
        'RU':  0.004,
    },
    'nl': {
        'NL':	0.665,
        'BE':	0.151
    },
    'fr': {
        'FR':	0.685,
        'BE':	0.057,
        'CA':	0.047,
        'CH':	0.015,  # Switzerland
        'DZ':	0.011,  # Algeria
        'MA':	0.010,  # Morocco
        'ES':	0.008,
        'DE':	0.008,
        'US':	0.006,
        'TN':	0.006,
        'UK':	0.005
    },
    'es': {
        'ES':	0.251,
        'AR':	0.159,
        'MX':	0.151,
        'CL':	0.090,
        'CO':	0.077,
        'PE':	0.053,
        'VE':	0.045,
        'EC':	0.039,
        'UY':	0.018,
        'US':	0.017,
        'CR':	0.011,
        'PY':	0.010,
        'DO':	0.008,
        'BO':	0.007,
        'GT':	0.006,
        'BR':	0.005
    }
}


def getTotalContributions(lang='en'):
    '''
    Returns the percentage of contribution from each country to the total number
    of edits in the Wikipedia of the desired language.
    '''
    return __totalEdits__[lang].copy()


def isAnon(rev):
    '''
    Determine whether a given revision is anonimous or not.
    Anonimous revision elements MUST contain an 'anon' element.
    '''
    return 'anon' in rev.keys()


def getContributionsForPage(wiki, pageTitle):
    '''
    Retrieve revision history of a given page.

    Returns a list of IP's (anon revisions) and user names (registred
    users) which contributed to the given page, plus a total number of
    revisions (user revisions + anon revisions)

    Parameters:
    wiki         wikiclient.Site object used for performing query
    pageTitle    Title of the target page.

    Returns:
    anonIPs      IP addresses of anonimous revisions
    users        Username of registered users which contributed revisions
    nRevs        Total number of revisions
    '''
    nRevs = 0
    anonIPs = []
    users = []

    somePage = wiki.Pages[pageTitle]
    somePage = somePage.resolve_redirect()

    if not somePage.exists:
        return [], [], 0

    revs = somePage.revisions(prop='user', limit=500)
    for rev in revs:
        nRevs += 1
        try:
            if isAnon(rev):
                anonIPs.append(rev['user'])
            else:
                users.append(rev['user'])
        except:
            # User tag is not found on revs -- no info can be obtained for this
            # revision
            pass
    return anonIPs, users, nRevs


def getAllBots(wiki):
    '''
    Create a set of all known bots in the given wiki.

    Parameters:
    wiki         wikiclient.Site object used for performing query

    Returns:
    bots         A set of all known bots.
    '''
    wikiId = wiki.site['wikiid']
    botsFile = wikiId + '_bots.pkl'
    try:
        import pickle
        bots = pickle.load(open(botsFile, 'r'))
        return bots
    except:
        wikiBots = wiki.allusers(group='bot')
        bots = set()
        for bot in wikiBots:
            bots.add(bot['name'])
        bots = pickle.dump(bots, open(botsFile, 'w'))
        return bots


def countExternalLinks(wikiPage):
    '''
    Count number of links to external pages (outside wikipedia)

    wikiPage:   mwclient.page object
    '''
    links = wikiPage.extlinks()
    return sum(1 for link in links)


def countLinksToPage(wikiPage):
    '''
    Count number of pages that link to the given wiki page.

    wikiPage:   mwclient.page object
    '''
    links = wikiPage.backlinks(filterredir='nonredirects', namespace=0)
    return sum(1 for link in links)


def countLinksFromPage(wikiPage):
    '''
    Count number of pages that are linked from the given wiki page.
    wikiPage:   mwclient.page object
    '''
    links = wikiPage.links(namespace=0)
    return sum(1 for link in links)


def countLanguageLinks(wikiPage):
    '''
    Count the number of links to equivalent page in other languages

    wikiPage:   mwclient.page object
    '''
    links = wikiPage.langlinks()
    return sum(1 for link in links)


def countRevisions(wikiPage):
    '''
    Count the number of revisions for the given wiki page.

    wikiPage:   mwclient.page object
    '''
    revs = wikiPage.revisions()
    return sum(1 for rev in revs)

if __name__ == '__main__':
    pass
