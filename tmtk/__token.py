import re
import os
import json
from .__unifier import Unifier


MONGOLIAN_PUNCTUATIONS = [chr(w) for w in range(0x1800, 0x180a)]
MONGOLIAN_DIGISTS = [chr(w) for w in range(0x1810, 0x181a)]
MONGOLIAN_CONTROL_CHAR = [chr(w) for w in range(
    0x180b, 0x180f)] + ["\u200c", "\u200d", "\u202f"]
MONGOLIAN_WORD_CHAR = [chr(a) for a in range(
    0x1820, 0x18ab)] + MONGOLIAN_CONTROL_CHAR

default_suffix_pattern = (
    # [ae]jvu
    (
        ("动"),
        (
            # sqv
            (665, 704, 250),
            # lhu
            (659, 523),
            # biju
            (358, 710, 250),
            # ij[vu]
            (239, 710, 250),
            # gulbe
            (516, 659, 351),
            # l[ae]
            (660, 216),
            # deg
            (685, 212, 494,),
            # [ae]bel
            (212, 350, 660),
            # l[ae]n
            (659, 212, 214),
            # rqu
            (727, 704, 250),
            # 
            (212, 710, 250),
            # gvljv
            (489, 248, 659, 710, 250),
            # gsan
            (212, 212, 665, 212, 214),
            # gsen
            (634, 212, 214),
            # gad
            (489, 212, 248, 214),
            # ged
            (212, 499, 248, 214),
            # dag
            (685, 212, 492),
            # gulhu
            (516, 659, 523),
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
            # gdahv
            (212, 212, 685, 212, 212, 212, 250),
            # dahv
            (685, 212, 212, 212, 250),
            # qiheged
            (704, 239, 499, 499, 248, 214),
            # gdeg
            (637, 212, 494),
            # gdeged
            (637, 212, 499, 248, 214),
            # r[ae]j[vu]
            (727, 212, 710, 250),
            # eged
            (710, 212, 499, 248, 214),
            # gheju
            (499, 710, 250),
            # j[ae]i
            (710, 212, 243),
            # lvn
            (489, 248, 659, 248, 214),
            # l[ae]b[ae]
            (659, 212, 351),
            # ghuju
            (516, 710, 250),
            # baju
            (350, 710, 250),
            # baqv
            (350, 704, 250),
            # vjv
            (248, 710, 250),
            # gar[ae]i
            (489, 212, 727, 212, 243),
            # lvn_a
            (659, 248, 312, 216),
            # bvjv
            (362, 710, 250),
            # hijv
            (507, 710, 250),
            # qan
            (659, 704, 212, 214),
            # ged
            (499, 248, 214),
            # gsagar
            (212, 212, 665, 212, 489, 212, 728),
            # gulun
            (516, 659, 248, 214),
            # n_[ae]
            (312, 216),
            # lju
            (659, 710, 250),
            # vlba
            (248, 659, 351),
            # lahv
            (659, 212, 212, 212, 250),
            # hahv
            (212, 212, 212, 212, 212, 250),
            # gahv
            (489, 212, 212, 212, 250),
            # gaba
            (489, 212, 351),
            # ihaba
            (239, 212, 212, 212, 351),
            # bvy_a
            (362, 243, 216),
            # dqv
            (248, 212, 704, 250),
            # b[ae]l
            (248, 350, 660),
            # [ae]y_[ae]
            (212, 243, 216)
        )
    ), (
        ("形"),
        (
            # [ae]t[ae]i
            (212, 685, 212, 243),
            # t[ae]i
            (685, 212, 243),
            # lig
            (659, 239, 492),
            # gatv
            (489, 212, 685, 250),
            # Nhei
            (490, 499, 243),
            # lig 阴性
            (659, 239, 494),

        )
    ), (
        ("副"),
        (
            # lgui
            (659, 516, 243),
            # lehi
            (212, 659, 212, 509)

        )
    ), (
        ("名"),
        (
            # [ae]mji
            (212, 652, 710, 243),
            # lt[ae]
            (212, 659, 685, 214),
            (685, 212, 660),
            # lvlta
            (659, 248, 659, 685, 214),
            # bagatvr
            (350, 489, 212, 685, 248, 728),
            # gqi
            (212, 639, 243),
            # g_a
            (493, 216),
            # qid
            (704, 239, 248, 214),
            # qvd
            (704, 248, 248, 214),
            # r[ae]l
            (727, 212, 660),
            # mji
            (652, 710, 243),
            # dvgan
            (685, 248, 489, 212, 214),
            # lelgen
            (659, 212, 659, 499, 214),
            # bayar
            (350, 719, 212, 728),
            # suhe
            (665, 248, 239, 501),
            # lelge
            (396, 212, 659, 501),
            # gdvrji
            (248, 727, 710, 243),
            # gdel
            (637, 212, 660),
            # gdal
            (212, 212, 685, 212, 660),
            # gal
            (489, 212, 660),
            # gan
            (489, 212, 214),
            # ugqi 阴性
            (248, 639, 243),
            # gqi 阳性
            (212, 212, 704, 243),
            # 不知道是什么
            (659, 212, 660)
        )
    )
)


class Tokenizer():
    __ptrn1_u = re.compile("([{0}]+)".format("".join(MONGOLIAN_WORD_CHAR)))
    __ptrn2_u = re.compile("(\u202f[^\u202f ]+)")

    __ptrn1_m = re.compile(r"([\ue263-\ue34f]+)")
    __ptrn2_m = re.compile(r"(\ue263[^\ue263 ]+)")

    __dictionary = {}

    def __init__(self, code_type=0):
        """[summary]
        Keyword Arguments:
            code_type {int} -- [description] (default: {0}, Unicode:0, Menkcode 1)
        """

        this_dir, this_filename = os.path.split(__file__)
        dictionary_path = os.path.join(
            this_dir,
            "dictionary_garray.jl"
        )
        self.__unifier = Unifier()
        if code_type == 0:
            self.__ptrn1 = self.__ptrn1_u
            self.__ptrn2 = self.__ptrn2_u
        else:
            self.__ptrn1 = self.__ptrn1_m
            self.__ptrn2 = self.__ptrn2_m

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
               word_list, word2garray=None,
               match_suffix_pattern=True,
               external_suffix_pattern=None):

        suffix_pattern = None
        if match_suffix_pattern:
            suffix_pattern = default_suffix_pattern
            if external_suffix_pattern:
                suffix_pattern += external_suffix_pattern

        for token in word_list:
            garray = None
            garray_str = None
            if word2garray:
                garray = word2garray.get(token, None)

            if not garray:
                garray = self.__unifier.get_garray(token)

            # assert not isinstance(garray, str)
            garray_str = json.dumps(garray)

            words = self.__dictionary.get(garray_str, None)

            taglist = []
            if words:
                for word in words:
                    taglist += word["pos"]

            if suffix_pattern:
                for (tag, patterns) in suffix_pattern:
                    for ptrn in patterns:
                        if tuple(garray[-len(ptrn):]) == ptrn:
                            taglist += [t + "_" for t in tag]
                            break

            yield (token, garray, list(set(taglist)))
