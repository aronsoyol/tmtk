import json
import unittest

from tqdm import tqdm

from tmtk import shaper, tokenizer, unifier

tqdm.monitor_interval = 0

# from timu import timu

undusuten_list = [
    "ᠦᠨᠳ᠋ᠤᠰᠤᠳ᠋ᠡᠨ", "ᠦᠨᠳ᠋ᠦᠰᠣᠳ᠋ᠡᠨ", "ᠦᠨᠲᠤᠰᠤᠲᠠᠨ", "ᠥᠨᠳ᠋ᠣᠰᠣᠳ᠋ᠡᠨ", "ᠦᠨᠳ᠋ᠤᠰᠤᠳ᠋ᠠᠨ",
    "ᠥᠨᠳ᠋ᠥᠰᠥᠲᠡᠨ", "ᠦᠨᠳ᠋ᠤᠰᠣᠳ᠋ᠠᠨ", "ᠦᠨᠳ᠋ᠦᠰᠦᠳ᠋ᠠᠨ", "ᠦᠨᠳ᠋ᠣᠰᠣᠳ᠋ᠡᠨ", "ᠦᠨᠳᠤᠰᠦᠲᠡᠨ",
    "ᠦᠨᠳᠣᠰᠣᠳᠡᠨ", "ᠦᠡᠳᠦᠰᠤᠳᠡᠨ", "ᠦᠨᠳᠤᠰᠤᠲᠡᠨ", "ᠦᠡᠳᠦᠰᠦᠳᠡᠨ", "ᠥᠨᠳᠣᠰᠣᠳᠡᠨ",
    "ᠦᠨᠳᠤᠰᠦᠳᠡᠨ", "ᠦᠨᠳᠤᠰᠤᠲᠡᠠ", "ᠦᠨᠳᠤᠰᠤᠲᠠᠨ", "ᠦᠨᠳᠦᠰᠤᠲᠡᠨ", "ᠦᠨᠳᠦᠰᠤᠳᠡᠨ",
    "ᠥᠨᠳᠦᠰᠦᠲᠡᠨ", "ᠦᠨᠲᠦᠰᠦᠲᠠᠨ", "ᠦᠨᠲᠦᠰᠦᠲᠡᠨ", "ᠥᠨᠳᠥᠰᠥᠲᠠᠨ", "ᠦᠨᠲᠦᠰᠦᠲᠡᠡ",
    "ᠦᠨᠲᠦᠰᠦᠲᠠᠠ", "ᠦᠨᠳᠦᠰᠤᠳᠠᠠ", "ᠦᠨᠳᠦᠰᠦᠳᠠᠠ", "ᠦᠨᠲᠤᠰᠤᠲᠡᠨ", "ᠦᠨᠳᠤᠰᠤᠳᠠᠨ",
    "ᠦᠨᠳᠤᠰᠤᠳᠡᠨ", "ᠦᠡᠳᠤᠰᠤᠳᠡᠨ", "ᠦᠨᠳᠦᠰᠦᠲᠠᠨ", "ᠦᠨᠳᠦᠰᠤᠳᠠᠨ", "ᠥᠨᠳᠤᠰᠤᠳᠡᠨ",
    "ᠦᠨᠳᠦᠰᠦᠳᠡᠨ", "ᠦᠠᠳᠤᠰᠤᠳᠠᠨ", "ᠥᠡᠳᠦᠰᠦᠳᠡᠨ", "ᠦᠨᠳ᠋ᠦᠰᠦᠲᠡᠨ", "ᠦᠨᠳᠦᠰᠦᠳᠠᠨ",
    "ᠦᠨᠳ᠋ᠣᠰᠦᠳ᠋ᠡᠨ", "ᠦᠨᠳ᠋ᠦᠰᠦᠳ᠋ᠡᠨ", "ᠦᠨᠳᠦᠰᠦᠲᠡᠨ"
]


class TestTimu(unittest.TestCase):
    # def setUp(self):

    def testTokenizer(self):
        text = ('ᠰᠠᠷ\u180eᠠ aᠭᠠᠵᠠᠷ ᠤᠰᠤᠨ\u202fᠣasdfᠪᠦᠷᠢᠳᠭᠡᠯ好'
                ' ᠬᠢᠵᠦ᠃ᠬᠢᠵᠦ ᠤᠰᠤᠨ\u202fᠣ\u202fᠣ\u202fᠣ')

        expected = ['ᠰᠠᠷ\u180eᠠ', 'ᠭᠠᠵᠠᠷ', 'ᠤᠰᠤᠨ', '\u202fᠣ',
                    'ᠪᠦᠷᠢᠳᠭᠡᠯ', 'ᠬᠢᠵᠦ', 'ᠬᠢᠵᠦ', 'ᠤᠰᠤᠨ',
                    '\u202fᠣ', '\u202fᠣ', '\u202fᠣ']

        result = tokenizer.tokenize(
            text,
            split_suffix=True,
            only_mongolian=True
        )

        self.assertEqual(result, expected)

    def test_one(self):
        # self.assertEqual(len(unsusuten_list), 40)
        for undusuten in undusuten_list[1:]:
            self.assertEqual(
                unifier.get_uniq_gid_list(undusuten_list[0]),
                unifier.get_uniq_gid_list(undusuten),
            )

    def testShpaer2(self):
        with open("test/test_words.txt", "r") as file:
            result = [token for token in file if token[0]
                      not in ["\u202f", "\u200d"]]

        word2garray = {}

        for token in result:
            garray = unifier.get_uniq_gid_list(token)
            word2garray[token] = garray

        with open("test_resulr2.txt", "w") as file:
            json.dump(word2garray, fp=file)
        self.assertEqual(1, 1)

    def test_two(self):
        self.assertEqual(
            unifier.get_uniq_gid_list("ᠠᠷᠢᠭᠤᠨᠰᠤᠶᠤᠯ"),
            [209, 727, 239, 489, 248, 212, 665, 248, 719, 248, 660]
        )

    def test_3(self):
        word = 'ᠪᠥᠬᠥᠢᠢᠯᠡ'
        garray1 = unifier.get_uniq_gid_list(word)
        garray2 = shaper.shape(word)

        self.assertTrue(garray1 == [370, 516, 239, 239, 659, 214])
        self.assertTrue(garray2 == [370, 519, 241, 239, 659, 226])
