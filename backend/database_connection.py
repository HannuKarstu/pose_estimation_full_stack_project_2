import os

from bson.objectid import ObjectId
from bson.errors import InvalidId

import backend.database

dir_path = os.path.dirname(os.path.realpath(__file__))


class DBConnection:
    def __init__(self, collection):
        self.collection = collection

    def insert_item(self, item):
        print(f"Saving item to database")

        backend.database.mongo.db[self.collection].insert_one(item)

        if item.get("_id"):
            item["_id"] = str(item["_id"])
            db_status = "saved"
            print(f"- Saved: ({item['_id']})")

        else:
            raise Exception("Item not saved to database.")

        return item, db_status

    def get_all_items(self):
        print("Fetching all items from database")

        try:
            cursor = backend.database.mongo.db[self.collection].find({})
            items = list(cursor)

            if items:
                for i, item in enumerate(items):
                    items[i]["_id"] = str(item["_id"])
                db_status = "found"

                print(f"- Fetched {len(items)} documents")
            else:
                db_status = "not_found"

        except Exception as err:
            print(f"- Error occurred: '{err}'")
            db_status = "error"

        return items, db_status

    def find_item_by_id(self, db_id):
        print(f"Fetching item by id ({db_id})")
        item = {}

        try:
            item = backend.database.mongo.db[self.collection].find_one(
                {"_id": ObjectId(db_id)}
            )
            if item:
                print(f"- Fetched item")
                item["_id"] = str(item["_id"])
                db_status = "found"
            else:
                db_status = "not_found"

        except InvalidId as err:
            db_status = "invalid_id"

        except Exception as err:
            db_status = "error"
            print(f"- Error occurred: '{err}'")

        return item, db_status

    def update_item(self, db_id, update):
        print(f"Updating item by id ({db_id}). Update {update}")
        item = {}

        filter = {'_id': ObjectId(db_id)}
        new_values = {'$set': update}

        try:
            item = backend.database.mongo.db[self.collection].find_one_and_update(
                filter,
                new_values,
                upsert=False,
                return_document="after"
            )

            if item:
                item["_id"] = str(item["_id"])
                print(f"- Updated item {item['_id']}")
                db_status = "updated"

            else:
                db_status = "not_found"

        except InvalidId as err:
            db_status = "invalid_id"

        except Exception as err:
            db_status = "error"
            print(f"- Error occurred: '{err}'")

        return item, db_status

    def delete_item(self, db_id):
        print(f"Deleting item by id ({db_id}).")
        item = {}

        try:
            item = backend.database.mongo.db[self.collection].find_one_and_delete(
                {'_id': ObjectId(db_id)}
            )

            if item:
                db_status = "deleted"
                item["_id"] = str(item["_id"])
                print(f"- Deleted item: {item}")
            else:
                db_status = "not_found"

        except InvalidId as err:
            db_status = "invalid_id"

        except Exception as err:
            db_status = "not_deleted"
            print(f"- Error deleting: '{err}'")

        return item, db_status
