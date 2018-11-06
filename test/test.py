import unittest
from tmtpk import Unifier

from tmtpk import Tokenizer

from tmtpk import Shaper2
from tqdm import tqdm
import json
tqdm.monitor_interval = 0

unifier = Unifier()
tokenizer = Tokenizer()
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
shaper = Shaper2()


class TestTimu(unittest.TestCase):
    # def setUp(self):

    def testTokenizer(self):
        text = 'ᠰᠠᠷ\u180eᠠ aᠭᠠᠵᠠᠷ ᠤᠰᠤᠨ\u202fᠣasdfᠪᠦᠷᠢᠳᠭᠡᠯ好 ᠬᠢᠵᠦ᠃ᠬᠢᠵᠦ ᠤᠰᠤᠨ\u202fᠣ\u202fᠣ\u202fᠣ'

        expected = ['ᠰᠠᠷ\u180eᠠ', 'ᠭᠠᠵᠠᠷ', 'ᠤᠰᠤᠨ', '\u202fᠣ',
                    'ᠪᠦᠷᠢᠳᠭᠡᠯ', 'ᠬᠢᠵᠦ', 'ᠬᠢᠵᠦ', 'ᠤᠰᠤᠨ',
                    '\u202fᠣ', '\u202fᠣ', '\u202fᠣ']

        result = tokenizer.tokenize(
            text,
            split_suffix=True,
            only_mongolian=True)

        self.assertEqual(result, expected)

    def test_one(self):
        # self.assertEqual(len(unsusuten_list), 40)
        for undusuten in undusuten_list[1:]:
            self.assertEqual(
                unifier.get_uniq_gid_list(undusuten_list[0]),
                unifier.get_uniq_gid_list(undusuten),
            )

    # def testShpaer1(self):
    #     with open("test/test_words.txt", "r") as file:
    #         result = [token for token in file if token[0]
    #                   not in ["\u202f", "\u200d"]]

    #     word2garray = {}
        
    #     for token in tqdm(result):
    #         garray = unifier.get_uniq_gid_list(token)
    #         word2garray[token] = garray

    #     with open("test_resulr1.txt", "w") as file:
    #         json.dump(word2garray, fp=file)

    def testShpaer2(self):
        with open("test/test_words.txt", "r") as file:
            result = [token for token in file if token[0]
                      not in ["\u202f", "\u200d"]]

        word2garray = {}

        for token in tqdm(result):
            garray = unifier.get_uniq_gid_list(token, shaper=shaper)
            word2garray[token] = garray

        with open("test_resulr2.txt", "w") as file:
            json.dump(word2garray, fp=file)

    def testShpaer3(self):
        with open("test/test_words.txt", "r") as file:
            result = [token for token in file if token[0]
                      not in ["\u202f", "\u200d"]]

        word2garray = {}

        for token in tqdm(result):
            garray1 = unifier.get_uniq_gid_list(token.strip(), shaper=shaper)
            garray2 = unifier.get_uniq_gid_list(token.strip())
            self.assertEqual(garray1, garray2)

    def test_two(self):
        self.assertEqual(
            unifier.get_uniq_gid_list("ᠠᠷᠢᠭᠤᠨᠰᠤᠶᠤᠯ"),
            [209, 727, 239, 489, 248, 212, 665, 248, 719, 248, 660]
        )
    
    def test_3(self):
        word = 'ᠪᠥᠬᠥᠢᠢᠯᠡ'
        garray = unifier.get_uniq_gid_list(word)
        print("="*100)
        print(word, garray)

    def test_4(self):
        word = 'ᠪᠥᠬᠥᠢᠢᠯᠡ'
        
        print("$"*100)
        print(shaper.shape(word))
        print("$"*100)
