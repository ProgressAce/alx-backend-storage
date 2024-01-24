#!/usr/bin/env python3
"""Lists all documents in a mongodb collection."""

import pymongo


def list_all(mongo_collection):
    """Lists all documents of the MongoDB collection."""

    docs = []
    for doc in mongo_collection.find():
        docs.append(doc)

    return docs
