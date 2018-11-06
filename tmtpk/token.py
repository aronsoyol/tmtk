import re
import os
import json
from .unifier import Unifier


MONGOLIAN_PUNCTUATIONS = [chr(w) for w in range(0x1800, 0x180a)]
MONGOLIAN_DIGISTS = [chr(w) for w in range(0x1810, 0x181a)]
MONGOLIAN_CONTROL_CHAR = [chr(w) for w in range(
    0x180b, 0x180f)] + ["\u200c", "\u200d", "\u202f"]
MONGOLIAN_WORD_CHAR = [chr(a) for a in range(
    0x1820, 0x18ab)] + MONGOLIAN_CONTROL_CHAR

default_verb_suffix_pattern = (
    # gvljv
    (489, 248, 659, 710, 250),
    # gsan
    (212, 212, 665, 212, 214),
    # lagsan
    (659, 212, 212, 212, 665, 212, 214),
    # leegsen
    (659, 212, 634, 212, 214),
    # lehu
    (659, 212, 523),
    # lahv
    (659, 212, 212, 250),
    # gdehu
    (637, 212, 523),
    # dahv
    (685, 212, 212, 212, 250),
    # qiheged
    (704, 239, 499, 499, 699),
)


class Tokenizer():
    __ptrn2 = re.compile("(\u202f[^\u202f ]+)")
    __ptrn1 = re.compile("([{0}]+)".format("".join(MONGOLIAN_WORD_CHAR)))
    __dictionary = {}

    def __init__(self):
        this_dir, this_filename = os.path.split(__file__)
        dictionary_path = os.path.join(
            this_dir,
            "dictionary_garray.jl"
        )
        with open(dictionary_path, "r") as file:
            for line in file:
                item = json.loads(line)
                garray_str = json.dumps(item["garray"])
                self.__dictionary[garray_str] = item["words"]

    def tokenize(self, text, split_suffix=False, only_mongolian=True):
        level1 = self.__ptrn1.split(text)
        if only_mongolian:
            level1 = level1[1::2]

        if not split_suffix:
            return level1

        level2 = []
        for item in level1:
            level2_sub = self.__ptrn2.split(item)
            level2 += [item for item in level2_sub if item]
        return level2

    def tagger(self,
               word_list, word2garray,
               external_verb_suffix_pattern=None):

        unifier = Unifier()
        for token in word_list:
            garray = word2garray.get(token, None)
            garray_str = ""

            if not garray:
                garray = unifier.get_uniq_gid_list(token)

            if isinstance(garray, list):
                garray_str = json.dumps(garray)
            else:
                garray_str = garray
                garray = json.loads(garray_str)

            words = self.__dictionary.get(garray_str, None)

            taglist = []
            if words:
                for word in words:
                    taglist += word["pos"]

            if garray[-3:] == [659, 212, 660]:
                taglist += ["名"]

            for suffix in default_verb_suffix_pattern:
                if tuple(garray[-len(suffix):]) == suffix:
                    taglist += ["动"]

            if external_verb_suffix_pattern:
                for suffix in external_verb_suffix_pattern:
                    if tuple(garray[-len(suffix):]) == suffix:
                        taglist += ["动"]

            yield (token, garray, list(set(taglist)))
