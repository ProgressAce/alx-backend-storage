#!/usr/bin/env python3
"""Defines a function that inserts a new document in a collection."""

import pymongo


def insert_school(mongo_collection, **kwargs) -> str:
    """Inserts a new document in a mongodb collection based on kwargs."""

    doc_id: str = mongo_collection.insert_one(kwargs).inserted_id

    return doc_id
