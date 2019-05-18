from typing import Callable
from types import SimpleNamespace
from json import dumps
from random import random, randint, choice, sample
from string import ascii_letters
from functools import partial
import re
import rstr


# Helpers
def is_json_serializable(obj):
    try:
        dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False


def return_self(*args):
    return set(*args)


def create(source):
    """
    Function that recursively creates an object based on the source.
    If constant -> returns a constant
    If dict -> returns a dict
    If callable -> calls the source
    """
    if hasattr(source, "items"):
        obj = SimpleNamespace()
        for k, v in source.items():
            if type(v) is dict:
                #  handles nested objects
                setattr(obj, k, create(v))
            elif is_json_serializable(v):
                #  handles constants and other serializable objects
                setattr(obj, k, v)
            elif callable(v):
                #  evaluates and sets values for functions
                setattr(obj, k, v())
            else:
                continue

        return obj.__dict__
    elif callable(source):
        return source()
    else:
        return source


# Basic Primitives
def Int(lower: int = 0,
        upper: int = 10):

    def func():
        return randint(lower, upper)

    return func


def Float(lower: float = 0,
          upper: float = 10,
          dp: int = None):
    def func():
        return round(random() * (upper - lower) + lower, dp)

    return func


def Str(length: int = 10,
        pattern: str = None,
        formatter: Callable[[str], str] = lambda x: x):
    def func():
        if pattern is None or re.compile(pattern) is False:
            rv = ''.join(choice(ascii_letters) for _ in range(length))
        else:
            rv = rstr.xeger(pattern)

        return formatter(rv)

    return func


# Collections
def Enum(collection: list = []):
    def func():
        return choice(collection)

    return func


def Boolean():
    def func():
        return Enum([True, False])

    return func


def List(item: dict,
         limit: int = 10):
    def func():
        make = partial(return_self, item)
        if isinstance(item, dict):
            make = partial(create, source=item)
        elif callable(item):
            make = item

        return [make() for _ in range(randint(0, limit))]

    return func


def Set(collection: set = set(),
        min_count: int = 0,
        max_count: int = 0):

    max_count = len(collection)

    def func():
        selected_set = sample(collection, randint(min_count, max_count))
        return selected_set

    return func


def Optional(return_obj):
    """
    Randomly returns null or the return_obj
    """
    def func():
        if choice([True, False]):
            return create(return_obj)
        else:
            return None
    return func
