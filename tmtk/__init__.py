
# from .shaper import Shaper

from .__shaper2 import Shaper2

from .__converter import convert2unicode
from .__unifier import Unifier

from .__token import Tokenizer

# from . convert2unicode import Converter

unifier = Unifier()
tokenizer = Tokenizer()
shaper = Shaper2()


class Uniqode():
    __word = ""

    def __init__(self, word):
        self.__word = word
        self.__garray = unifier.get_garray(word)

    def __hash__(self):
        return hash(str(self.__garray))

    def __eq__(self, other):
        return self.__garray == other.__garray

    def __str__(self):
        return str(self.__garray)
