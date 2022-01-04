def print_records(mongo):
    # test is collection name
    results = mongo.db.test.find({})
    for r in results:
        print(r)
