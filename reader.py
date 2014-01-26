#-*- coding: utf-8 -*-

import sys
from kitchen.text.converters import getwriter
import cPickle as pickle
import sys, string, re
from collections import Counter, defaultdict
from plp import PLP
from gensim import corpora, models, similarities
from sets import Set

UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

def load_obj_from_file(filename):
    with open(filename, 'rb') as output:
        obj = pickle.load(output)
        return obj

items_categories = load_obj_from_file('items_categories.dat') 
categories_tree = load_obj_from_file('categories_tree.dat')
categories_names = load_obj_from_file('categories_names.dat')

translation_table_1 = dict.fromkeys(map(ord, string.punctuation), None)
stoplist = set('w i z na od do a o u ta ten to okazja kup teraz złotówki przesyłka gratis kurier wysyłka natychmiastowa'.split())

class SimilaritiesFinder:

    def transformText (self, original):
        words = original.translate(translation_table_1).split()
        text = ""
        for word in words:
            labels = self.p.rec(word)
            if labels:
                text = text + self.p.bform(labels[0]).encode("utf8")
            text = text + " "
        return text

    def splitAndTrim (self, transformed_text):
        return [word for word in transformed_text.lower().split() if word not in stoplist]

    def __init__(self, input):
        self.p = PLP()
        self.documents = []
        self.input_texts = []
        self.word_count = {}
        for d in [word.lower() for word in input]:
            self.documents.append(self.transformText(d))

        texts = [self.splitAndTrim(document) for document in self.documents]

        cnt = Counter()
        [cnt.update(text) for text in texts]
        tokens_once = [word for word, occ in cnt.items() if occ == 1]
        texts = [[word for word in text if word not in tokens_once] for text in texts]

        self.input_texts = zip (input, texts)
        
        for original, text in self.input_texts:
            for word in text:
                if word not in self.word_count:
                    self.word_count[word] = 1
                else:
                    self.word_count[word] = self.word_count[word] + 1

    def calculateWordScore(self, word):
        return float(1) / self.word_count[word]

    def find(self, auction):
        pattern = self.splitAndTrim(self.transformText(auction.lower()))
        title_scores = {}
        for original, title in self.input_texts:
            score = 0
            for word in pattern:
                if word in title:
                    score = score + self.calculateWordScore(word)
            title_scores[original] = score
        winner =  max (title_scores, key=lambda k: title_scores[k])
        print 'Similar Auction:'
        print '    ', winner
        for (name, cats) in items_categories:
            if name == winner:
                printCategories(cats)
                break
        

def printCategories (cats):
    print 'Categories: '
    for c in cats:
        print '    - ' + categories_names[c]

def printItemsWithCategories ():
    for (name, categories) in items_categories:
        print name
        printCategories(categories)
    print 'TOTAL OF ' + str(len(items_categories)) + ' ITEMS READ.'

    
auctions = [
u'interaktywna kotka w mobilnym barze, świetny prezent dla dziewczynki',
u'pluszowy miś 60cm szary',
u'"sezon burz", najnowsza powieść Sapkowskiego, twarda oprawa',
u'zestaw: bransoletka, obrączka, naszyjnik, złoto 12 karatów',
u'zestaw: bransoletka, obrączka, naszyjnik, masa perłowa! przesyłka natychmiastowa!',
u'wielofunkcyjny robot kuchenny zelmer 173842']

finder = SimilaritiesFinder([name for name, categories in items_categories])

for auction in auctions:
    print
    print 'Query:'
    print '    ', auction
    finder.find(auction)
    print
    print '**************'
