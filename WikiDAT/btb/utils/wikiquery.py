'''
Created on Aug 5, 2014

@author: carlosm
'''

'''
Percentage of contribution from each country to the total number of edits in english Wikipedia.
Taken from http://stats.wikimedia.org/wikimedia/squids/SquidReportPageEditsPerLanguageBreakdown.htm
'''
__totalEdits__ = {}
__totalEdits__['US'] = 0.383
__totalEdits__['UK'] = 0.132
__totalEdits__['IN'] = 0.069
__totalEdits__['CA'] = 0.054
__totalEdits__['AU'] = 0.036
__totalEdits__['PH'] = 0.026
__totalEdits__['DE'] = 0.015
__totalEdits__['BR'] = 0.011
__totalEdits__['IT'] = 0.01
__totalEdits__['IE'] = 0.01
__totalEdits__['PK'] = 0.009
__totalEdits__['FR'] = 0.008
__totalEdits__['MY'] = 0.008
__totalEdits__['NL'] = 0.008
__totalEdits__['ID'] = 0.008
__totalEdits__['CN'] = 0.007
__totalEdits__['NZ'] = 0.007
__totalEdits__['ES'] = 0.007
__totalEdits__['IR'] = 0.007
__totalEdits__['MX'] = 0.005
__totalEdits__['SE'] = 0.005
__totalEdits__['RU'] = 0.005
__totalEdits__['GR'] = 0.005
__totalEdits__['TR'] = 0.005

def getTotalContributions():
    '''
    Returns the percentage of contribution from each country to the total number 
    of edits in english Wikipedia.
    '''
    return __totalEdits__.copy()

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
    revs = somePage.revisions(prop='user', limit=500)
    for rev in revs:
        nRevs += 1
        try:
            if isAnon(rev):
                anonIPs.append(rev['user'])
            else:
                users.append(rev['user'])
        except:
            # User tag is not found on revs -- no info can be obtained for this revision
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
    wikiBots = wiki.allusers(group='bot')
    bots = set()
    for bot in wikiBots:
        bots.add(bot['name'])
    return bots

if __name__ == '__main__':
    pass
