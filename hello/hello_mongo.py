# coding=utf-8

import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://10.40.100.16:27017/')

db = client.test  # new a database

peoples = db.people.find().sort('_id', pymongo.ASCENDING).limit(3)  # new a table
for people in peoples:
    print people

muser = db.user
muser.save({'id':1, 'name':'cctest'}) # add a record
muser.insert({'id':2, 'name':'hello'}) # add a record
print muser.find_one() # find a record
print muser.find_one({'id':2}) # find a record by query
muser.create_index('id')
muser.find().sort('id', pymongo.ASCENDING) # DESCENDING
# muser.drop() delete table
muser.find({'id':1}).count() # get records number
print list(muser.find({'id':1}).limit(3).skip(2)) # start index is 2 limit 3 records
muser.remove({'id':1}) # delet records where id = 1
muser.update({'id':2}, {'$set':{'name':'haha'}}) # update one recor
print muser.find_one({'id':2}) # find a record by query
