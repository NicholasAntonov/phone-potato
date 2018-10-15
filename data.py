from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.phonedb
db.drop_collection('numbers')

# If this is the first call with a phrase, register the number as the owner,
# otherwise, add it to the list of callers if its a unique call.
def register_call(keyphrase, caller_number):
    existing = db.numbers.find_one({'owner_phrase': keyphrase})
    if existing:
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
        db.numbers.insert_one({
            'owner_phrase': keyphrase,
            'owner_number': caller_number,
            'submitters': [caller_number],
            'numbers_redeemed': 0,
        })

print(register_call('a', 1))
print(register_call('a', 1))
print(register_call('a', 2))
print(register_call('a', 2))
print(register_call('b', 1))
print(db.numbers.find_one({'owner_phrase': 'a'}))
print(db.numbers.find_one({'owner_phrase': 'b'}))

