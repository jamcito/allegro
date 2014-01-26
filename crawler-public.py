#-*- coding: utf-8 -*-

from suds.client import Client
import base64
import logging
import hashlib
import sys
from kitchen.text.converters import getwriter
import cPickle as pickle

UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

url = 'PRIVATE'
webapiKey = 'PRIVATE'
userLogin = 'PRIVATE'
userHashPassword = base64.b64encode(hashlib.sha256(b'PRIVATE').digest())
countryCode = 1
countryId = 1

logging.getLogger('suds.client').setLevel(logging.CRITICAL)
client = Client('https://webapi.allegro.pl/service.php?wsdl')
service = client.service
versions = {}

for row in service.doQueryAllSysStatus(**{"countryId": countryId, "webapiKey": webapiKey}).item:
    versions[row.countryId] = row

sessionId = service.doLoginEnc(**{'userLogin': userLogin, 'userHashPassword': userHashPassword, 'countryCode': countryCode, 'webapiKey': webapiKey, 'localVersion': versions[1].verKey}).sessionHandlePart

client = Client(url)

categories_names = {}
categories_tree = {}
items_categories = []

def load_obj_from_file(filename):
    with open(filename, 'rb') as output:
        obj = pickle.load(output)
        return obj

def saveObjToFile (obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def getCategoriesList (categoryId, acc):
    if categoryId == 0 or categoryId not in categories_tree.keys():
        return acc
    acc.append(categoryId)
    return getCategoriesList (categories_tree[categoryId], acc)

def printCategories (cats):
    print 'Categories: '
    for c in cats:
        print '- ' + categories_names[c]

def printItemsWithCategories ():
    for (name, categories) in items_categories.iteritems():
        print name
        printCategories(categories)

def getItemsChunk (searchString, chunkId, chunkSize):
    params = client.factory.create('SearchOptType')
    params.searchString = searchString
    params.searchLimit = chunkSize
    params.searchOffset = chunkId
    params.searchOptions = 16 #include finished auctions
    query = {'sessionHandle': sessionId, 'searchQuery': params}
    result =  service.doSearch(**query)

    if result.searchCountFeatured > 0:
        for item in result['searchArray'].item:
            items_categories.append ([item.sItName,  getCategoriesList (item.sItCategoryId, [])])
    return result.searchCount

def getItems (searchString = 'prezent'):
    chunkSize = 100 # maximal amount allowed
    maxChunkId = getItemsChunk (searchString, 0, chunkSize) / chunkSize;
    i = 1
    previousLen = 0
    zerosInARow = 0
    while i < maxChunkId:
        maxChunkId = getItemsChunk (searchString, i, chunkSize) / chunkSize;
        i = i + 1
        print len(items_categories), 'items found so far, iteration ', i ,'of', maxChunkId
        if previousLen == len (items_categories):
            zerosInARow = zerosInARow + 1
        else:
            zerosInARow = 0
        previousLen = len (items_categories)
        if zerosInARow == 10:
            return

def getCategories ():
    categories_result = service.doGetCatsData(**{'countryId': countryId, 'localVersion': versions[1].verKey, 'webapiKey': webapiKey})
    cats = categories_result.catsList.item
    for cat in cats:
        categories_names [cat.catId] = cat.catName.encode('utf-8','replace')
        if cat.catParent > 0:
            categories_tree [cat.catId] = cat.catParent


CATEGORIES_NAMES = "categories_names.dat"
CATEGORIES_TREE = "categories_tree.dat"
ITEMS_CATEGORIES = "items_categories.dat"
try:
    categories_names = load_obj_from_file (CATEGORIES_NAMES)
    categories_tree = load_obj_from_file (CATEGORIES_TREE)
except IOError:
    getCategories()
    saveObjToFile(categories_names, CATEGORIES_NAMES)
    saveObjToFile(categories_tree, CATEGORIES_TREE)
try:
    items_categories = load_obj_from_file(ITEMS_CATEGORIES)
except IOError:
    items_categories = []
getItems(u'urządzenie')
saveObjToFile(items_categories, ITEMS_CATEGORIES)
