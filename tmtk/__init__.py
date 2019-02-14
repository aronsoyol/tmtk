
# from .shaper import Shaper

from .__shaper2 import Shaper2

from .__unifier import Unifier

from .__token import Tokenizer

from hashlib import md5
import json
# from . convert2unicode import Converter

unifier = Unifier()
tokenizer = Tokenizer()
shaper = Shaper2()

__version__ = "0.0.1"

def convert2unicode(text_m, converter="aronnote"):

    if converter == "aronnote":
        from .__converter2 import convert2unicode_aron
        return convert2unicode_aron(text_m)
    else:
        from .__converter import convert2unicode_imu
        return convert2unicode_imu(text_m)


class Uniqode():
    __word = ""

    # python 没有函数重载的原因：
    # python函数灵活的参数传递方式已经不要重载了
    def __init__(self, word=None, garray=None):
        """[使用一种方式初始化]

        Keyword Arguments:
            word {[str]} -- [使用单词] (default: {None})
            garray {[list]} -- [使用garray] (default: {None})

        Raises:
            Exception -- [garray可能使用了str类型，必须使用list类型]
        """

        if word:
            self.__garray = unifier.get_garray(word)
        elif garray:
            if isinstance(garray, list):
                self.__garray = garray
            else:
                raise Exception("garray is not a list")
        else:
            raise Exception("please initialise with "
                            "at least one word or garray")

    def md5(self):
        md5_ = md5()
        byte_array = json.dumps(self.__garray).encode()
        md5_.update(byte_array)
        return md5_.hexdigest()

    def uniqode(self):
        return "".join([chr(0xf000 + g) for g in self.__garray])

    def __hash__(self):
        return hash(str(self.__garray))

    def __eq__(self, other):
        return self.__garray == other.__garray

    def __str__(self):
        return str(self.__garray)

    def glyph_array(self):
        return self.__garray
