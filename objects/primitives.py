from typing import Callable
from types import SimpleNamespace
from json import dumps
from random import random, randint, choice
from string import ascii_letters
from functools import partial
import re, rstr

def is_json_serializable(obj):
    try:
        dumps(obj)
        return True
    except :
        return False


def create_obj_from_definition(source, return_json=True):
    obj = SimpleNamespace()
    for k, v in source.items():
        if type(v) is dict:
            #  handles nested objects
            setattr(obj, k, create(v, return_json=False))
        elif is_json_serializable(v):
            #  handles constants and other serializable objects
            setattr(obj, k, v)
        elif callable(v):
            #  evaluates and sets values for functions
            setattr(obj, k, v())
        else:
            continue

    if return_json:
        return dumps(obj.__dict__)
    else:
        return obj.__dict__


def PrimitiveInt(lower:int=0, upper:int=10):
    def func():
        return randint(lower, upper)

    return func

def PrimitiveFloat(lower:float=0, upper:float=10, dp:int=None):
    def func():
        return random() * self.higher - self.lower + self.lower

    return func

def PrimitiveStr(
        length:int=10, 
        pattern:str=None, 
        formatter:Callable[[str], str]=lambda x: x
    ):
    def func():
        if pattern is None or re.compile(pattern) is False:
            rv = ''.join(choice(ascii_letters) for _ in range(length))
        else:
            rv = rstr.xeger(pattern)

        return formatter(rv)

    return func

def PrimitiveEnum(collection:list=[]):
    def func():
        return choice(collection)

    return func

def PrimitiveBoolean():
    def func():
        return PrimitiveEnum([True, False])

    return func

def Collection(item:dict, limit:int=10):
    def func():
        make = lambda: item
        if isinstance(item, dict):
            make = partial(create, source=item, return_json=False)
        elif callable(item):
            make = item

        return [make() for _ in range(limit)]

    return func
