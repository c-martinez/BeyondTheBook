"""Summarize book.

Usage: inlScript.py <data>
                    [--langModel MODEL] [--liwcFile LIWCFile]
                    [--min-commonness <minc>] [ -h | --help]

Options:
  --langModel MODEL        Semanticizer language model [default: nl.model]
  --liwcFile LIWCFile      LIWC word file [default: LIWC2007_Dutch.dic.html]
  --min-commonness <minc>  Minimum commonness of semanticized entities
                           for them to be considered [default: 0.1]

"""
from __future__ import division

import BeautifulSoup
import pickle
import nltk
import glob

from collections import defaultdict
from semanticizest import Semanticizer
from docopt import docopt

def loadLIWCDic(dicFile):
    dic = open(dicFile).read()
    dicSoup = BeautifulSoup.BeautifulSoup(dic)

    cats = {}
    for div in dicSoup.findAll('div'):
        h2 = div.findNext('h2')
        catTitle = h2.text
        ps = div.findAll('p')
        assert len(ps)>=2
        wCount = ps[0].text.split(':')[1]
        wordBag = ps[1].text.split(' ')
        wordBag = [ word for word in wordBag if len(word)>0 ]
        cats[catTitle] = wordBag
        assert int(wCount)==len(wordBag)
    return cats

def invertSearchDict(liwcDict):
    wordCategory = defaultdict(list)
    for cat in liwcDict:
        for word in liwcDict[cat]:
            wordCategory[word].append(cat)
    return dict(wordCategory)

def processTeiFile(teiFile, liwcListFile, semListFile, countsListFile, commonnessThreshold, sent_tokenize):
    tei = open(teiFile).read()
    teiSoup = BeautifulSoup.BeautifulSoup(tei)

    print 'Processing book...',teiFile
    nPara = 0
    semList = []
    liwcList = []
    countsList = []
    paras = teiSoup.findAll('p')

    # Book as a list of paragraphs
    # For each paragraph

    print 'Begin iterate paragraphs: ',len(paras)
    for para in paras:
        pText = para.getText(separator=' ')
        nPara += 1
        pId = para.get('xml:id')
        pId = pId if pId is not None else nPara
        print '\r  paragraph: ',pId,

        # Count total words in paragraph -- Initialize
        wordCount = 0

        sents = sent_tokenize.tokenize(pText)
        for sent in sents:
            tokens = nltk.word_tokenize(sent)

            # Count total words in paragraph -- Increment
            wordCount += len(tokens)

            # Semanticize and keep list of words
            candidates = sem.all_candidates(tokens)
            for i0,i1,wikiTitle,commonness in candidates:
                if commonness>commonnessThreshold:
                    word = ' '.join(tokens[i0:i1])
                    semList.append((pId, word, wikiTitle, commonness))

            # Identify and count LIWC words
            for word in tokens:
                word = word.lower()
                if word in wordDict:
                    liwcList.append((pId, word, wordDict[word]))

        # Count total words in paragraph -- save
        countsList.append((pId, wordCount))
    print ''

    # Save in some format
    print 'Saving summary lists'
    print '  %d LIWC entries created'%(len(liwcList))
    print '  %d Semanticizer entries created'%(len(semList))
    print '  %d Paragraph count entries created'%(len(countsList))
    pickle.dump(liwcList, open(liwcListFile, 'w'))
    pickle.dump(semList, open(semListFile, 'w'))
    pickle.dump(countsList, open(countsListFile, 'w'))

if __name__ == '__main__':
    arguments = docopt(__doc__, version='NLeSc book summarization')
    # teiFile = arguments['<teiFile>']
    langModel = arguments['--langModel']
    liwcFile = arguments['--liwcFile']
    commonnessThreshold = arguments['--min-commonness']
    dataDir = arguments['<data>']
    commonnessThreshold = float(commonnessThreshold)

    liwcDict = loadLIWCDic(liwcFile)
    wordDict = invertSearchDict(liwcDict)
    sem = Semanticizer(langModel)
    print 'Language model loaded'

    sent_tokenize = nltk.data.load('tokenizers/punkt/dutch.pickle')

    for teiFile in glob.glob(dataDir + '*.xml'):
        outFile = teiFile.replace(dataDir, 'output/')
        liwcList = outFile.replace('.xml', '.liwc.pkl')
        semList  = outFile.replace('.xml', '.sem.pkl')
        countsList= outFile.replace('.xml', '.count.pkl')
        processTeiFile(teiFile, liwcList, semList, countsList, commonnessThreshold, sent_tokenize)
