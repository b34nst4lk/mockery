from typing import Callable, Union
from types import SimpleNamespace
from json import dumps
from random import random, randint, choice
from string import ascii_letters
from functools import partial
import re, rstr

class Primitive:
    def __init__(self, primitive_type):
        self.type = primitive_type

    def get_value(self):
        raise NotImplemented


def is_json_serializable(obj):
    try:
        dumps(obj)
        return True
    except :
        return False


def create(source, return_json=True):
    obj = SimpleNamespace()
    for k, v in source.items():
        if isinstance(v, Primitive):
            setattr(obj, k, v.get_value())
        elif type(v) is dict:
            setattr(obj, k, create(v, return_json=False))
        elif is_json_serializable(v):
            setattr(obj, k, v)
        else:
            continue

    if return_json:
        return dumps(obj.__dict__)
    else:
        return obj.__dict__


class PrimitiveInt(Primitive):
    def __init__(self, lower:int=0, upper:int=10):
        super(int)
        self.lower = lower
        self.upper = upper

    def get_value(self):
        return randint(self.lower, self.upper)


class PrimitiveFloat(Primitive):
    def __init__(self, lower:float=0, upper:float=10, dp:int=None):
        super(float)
        self.lower = lower
        self.upper = upper

    def get_value(self):
        value = random() * self.higher - self.lower + self.lower
        return value


class PrimitiveStr(Primitive):
    def __init__(
            self, 
            length:int=10, 
            pattern:str=None, 
            formatter:Callable[[str], str] = lambda x: x
        ):
        """
        pattern will take priority over length. Randomly gnenerated strings 
        from a regex pattern can exceed the specified length.

        formatter is a lambda that takes in a str and returns a str.
        """
        super(str)
        self.length = length
        self.pattern = pattern
        self.formatter = formatter

    def get_value(self):
        if self.pattern is None or re.compile(self.pattern) is False:
            rv = ''.join(choice(ascii_letters) for _ in range(self.length))
        else:
            rv = rstr.xeger(self.pattern)

        return self.formatter(rv)


class PrimitiveEnum(Primitive):
    def __init__(self, collection:list=[]):
        super(list)
        self.collection = collection

    def get_value(self):
        return choice(self.collection)


class PrimitiveBoolean(PrimitiveEnum):
    def __init__(self):
        super().__init__(collection=[True, False])


class Collection(Primitive):
    def __init__(self, item:Union[dict, Primitive], limit:int=10):
        super(list)
        self.item = item
        self.limit = limit

    def get_value(self):
        make = lambda x: x
        if isinstance(self.item, dict):
            make = partial(create, source=self.item, return_json=False)
        elif isinstance(self.item, Primitive):
            make = self.item.get_value

        return [make() for _ in range(self.limit)]

