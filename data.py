#! /env/python3

from pymongo import MongoClient

POTATO_SKIP = 3

client = MongoClient('mongodb://localhost:27017')
db = client.phonedb
db.drop_collection('numbers')

def current_users():
    return db.numbers.count_documents({})

# If this is the first call with a phrase, register the number as the owner,
# otherwise, add it to the list of callers if its a unique call.
def register_call(keyphrase, caller_number):
    existing = db.numbers.find_one({'owner_phrase': keyphrase})
    if existing:
        if existing['has_potato']:
            return
        if not caller_number in existing['submitters']:
            db.numbers.update({
                'owner_phrase': keyphrase,
            },
            {
                '$push': {
                    'submitters': caller_number,
                },
            })
    else:
        is_hot_potato = (current_users() != 0) and ((current_users() % POTATO_SKIP) == 0)
        db.numbers.insert_one({
            'owner_phrase': keyphrase,
            'owner_number': caller_number,
            'submitters': [caller_number],
            'numbers_redeemed': 0,
            'has_potato': is_hot_potato,
        })

register_call('x', -1)
register_call('y', -2)
register_call('a', 1)
register_call('a', 1)
register_call('a', 2)
register_call('a', 2)
register_call('b', 1)
for doc in db.numbers.find({}):
    print(doc)

