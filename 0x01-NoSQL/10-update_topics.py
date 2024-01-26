#!/usr/bin/env python3
"""Defines a function that updates a document in a mongodb collection."""

import pymongo


def update_topics(mongo_collection, name, topics) -> None:
    """Changes all topics of a school mongodb document, based on the name.

    Args:
        mongo_collection: the pymongo collection object.
        name (str): the school name to update
        topics (list of str): the list of topics approached in the school."""

    updated_value = {"$set": {"topics": topics}}
    mongo_collection.update_one({"name": name}, updated_value)
