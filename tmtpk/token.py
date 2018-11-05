import re


MONGOLIAN_PUNCTUATIONS = [chr(w) for w in range(0x1800, 0x180a)]
MONGOLIAN_DIGISTS = [chr(w) for w in range(0x1810, 0x181a)]
MONGOLIAN_CONTROL_CHAR = [chr(w) for w in range(
    0x180b, 0x180f)] + ["\u200c", "\u200d", "\u202f"]
MONGOLIAN_WORD_CHAR = [chr(a) for a in range(
    0x1820, 0x18ab)] + MONGOLIAN_CONTROL_CHAR


class Tokenizer():
    __ptrn2 = re.compile("(\u202f[^\u202f ]+)")
    __ptrn1 = re.compile("([{0}]+)".format("".join(MONGOLIAN_WORD_CHAR)))

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
