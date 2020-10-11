import unittest
from hw3.json_pony import *
import os.path as osp

class PonyJsonTest(unittest.TestCase):
    def test_Word_Clean(self):
        my_str = 'U<+1234> Hello World. Today is WAPWAPWAP!~__'
        cleaned_str = words_cleanning(my_str)
        self.assertEqual(cleaned_str,'U 1234 Hello World Today is WAPWAPWAP __')
    def test_UnicodeToSpace(self):
        my_str = 'U 1234 Hello World'
        processed_str = UnicodeToSpace(my_str)
        self.assertEqual(processed_str, 'U  Hello World')

    def test_preprocess(self):
        toy_df = pd.DataFrame({'pony' : ['Twilight Sparkle','Twilight Sparkle','Applejack'],
                              'dialog' : ['Hi','Hello','What the hell'],
                              'title': ['A WAP','A WAP', 'Cardi B']})
        toy_df = preprocess(toy_df)
        verify_df =  pd.DataFrame({'pony' : ['Twilight Sparkle','Applejack'],
                              'dialog' : ['Hi Hello','What the hell']})
        pd.testing.assert_frame_equal(toy_df, verify_df)

    def test_preprocess2(self):
        toy_df = pd.DataFrame({'pony': ['Twilight Sparkle', 'Twilight Sparkle', 'Applejack'],
                               'dialog': ['Hi', 'Hello', 'What the hell'],
                               'title': ['A WAP', 'Cardi B', 'Cardi B']})
        toy_df = preprocess(toy_df)
        verify_df = pd.DataFrame({'pony': ['Twilight Sparkle', 'Twilight Sparkle', 'Applejack'],
                                  'dialog': ['Hi', 'Hello', 'What the hell']})
        pd.testing.assert_frame_equal(toy_df, verify_df)

    def test_Verb1(self):
        toy_df = pd.DataFrame({'pony': ['Twilight Sparkle', 'Twilight Sparkle', 'Applejack'],
                               'dialog': ['Hi Pinkie', 'Hello Pie', 'What the hell Dash']})
        toy_dict = {}
        getVerb(toy_df,toy_dict)
        self.assertTrue(0.99<=sum(toy_dict.values())<=1.01)

    def test_Verb2(self):
        toy_df = pd.DataFrame({'pony': ['Twilight Sparkle', 'Rarity', 'Applejack', 'Cardi B'],
                               'dialog': ['Hi Pinkie', 'Hello Pie', 'What the hell Dash','He bought a phone just for pics of this WAP']})
        toy_dict = {}
        getVerb(toy_df, toy_dict)
        self.assertEqual(list(toy_dict.values()),[0.33, 0.33, 0.33, 0.0, 0.0, 0.0])

    def test_Ment1(self):
        toy_df = pd.DataFrame({'pony': ['Rainbow Dash','Pinkie Pie','Fluttershy','Twilight Sparkle', 'Rarity', 'Applejack', 'Cardi B'],
                               'dialog': ['Dash sucks Rarity is good ','I like Twilight and Sparkle and Dash','Pie is delicious Apple pie is very very good','Hi Pinkie', 'Hello Pie',
                                          'What the hell Dash', 'He bought a phone just for pics of this WAP']})
        toy_dict = {}
        getMention(toy_df, toy_dict)
        self.assertEqual(toy_dict['twilight'],{'applejack': 0.0, 'rarity': 0.0, 'pinkie': 1.0, 'rainbow': 0.0, 'fluttershy': 0.0})

    def test_Ment2(self):
        toy_df = pd.DataFrame(
            {'pony': ['Rainbow Dash', 'Pinkie Pie', 'Fluttershy', 'Twilight Sparkle', 'Rarity', 'Applejack', 'Cardi B'],
             'dialog': ['Dash sucks Rarity is good ', 'I like Twilight and Sparkle and Dash',
                        'Pie is delicious Apple pie is very very good', 'Hi Pinkie', 'Hello Pie',
                        'What the hell Dash', 'He bought a phone just for pics of this WAP']})
        toy_dict = {}
        getMention(toy_df, toy_dict)
        self.assertEqual(toy_dict['pinkie'], {'twilight': 0.67, 'applejack': 0.0, 'rarity': 0.0, 'rainbow': 0.33, 'fluttershy': 0.0})


    def test_Foll1(self):
        toy_df = pd.DataFrame(
            {'pony': ['Rainbow Dash', 'Pinkie Pie', 'Fluttershy', 'Twilight Sparkle', 'Rarity', 'Applejack', 'Cardi B'],
             'dialog': ['Dash sucks Rarity is good ', 'I like Twilight and Sparkle and Dash',
                        'Pie is delicious Apple pie is very very good', 'Hi Pinkie', 'Hello Pie',
                        'What the hell Dash', 'He bought a phone just for pics of this WAP']})
        toy_dict = {}
        getFoll(toy_df, toy_dict)
        self.assertEqual(toy_dict['fluttershy'],
                         {'twilight': 0.0, 'applejack': 0.0, 'rarity': 0.0, 'pinkie': 1.0, 'rainbow': 0.0, 'other': 0.0})

    def test_Foll2(self):
        toy_df = pd.DataFrame(
            {'pony': ['Rainbow Dash', 'Pinkie Pie', 'Fluttershy', 'Twilight Sparkle','Fluttershy', 'Rarity', 'Applejack', 'Cardi B'],
             'dialog': ['Dash sucks Rarity is good ', 'I like Twilight and Sparkle and Dash',
                        'Pie is delicious Apple pie is very very good', 'Hi Pinkie', 'Yum', 'Hello Pie',
                        'What the hell Dash', 'He bought a phone just for pics of this WAP']})
        toy_dict = {}
        getFoll(toy_df, toy_dict)
        self.assertEqual(toy_dict['fluttershy'],
                         {'twilight': 0.5, 'applejack': 0.0, 'rarity': 0.0, 'pinkie': 0.5, 'rainbow': 0.0, 'other': 0.0})

    def test_Non_dict1(self):
        dire = osp.dirname(__file__)
        dict_words_path = osp.join(dire, "..", "..", "..", "data", "words_alpha.txt")
        dict_words_k = open(dict_words_path)
        dict_words = set(dict_words_k.read().split('\n'))
        dict_words_k.close()
        toy_df = pd.DataFrame(
            {'pony': ['Rainbow Dash', 'Pinkie Pie', 'Fluttershy', 'Twilight Sparkle', 'Rarity',
                      'Applejack', 'Cardi B'],
             'dialog': ['HellO', 'I like Twilight and Sparkle and Dash',
                        'Pie is delicious Apple pie is very very good', 'Hi Pinkie', 'Hello Pie',
                        'What the hell Dash', 'He bought a phone just for pics of this WAP']})
        toy_dict = {}
        getNon_dict(toy_df, toy_dict, dict_words)
        self.assertEqual(toy_dict['rainbow'], [])

    def test_Non_dict2(self):
        dire = osp.dirname(__file__)
        dict_words_path = osp.join(dire, "..", "..", "..", "data", "words_alpha.txt")
        dict_words_k = open(dict_words_path)
        dict_words = set(dict_words_k.read().split('\n'))
        dict_words_k.close()
        toy_df = pd.DataFrame(
            {'pony': ['Rainbow Dash', 'Pinkie Pie', 'Fluttershy', 'Twilight Sparkle', 'Rarity',
                      'Applejack', 'Cardi B'],
             'dialog': ['haha awww awww awww bbibbi kvsadf', 'I like Twilight and Sparkle and Dash',
                        'Pie is delicious Apple pie is very very good', 'Hi Pinkie', 'Hello Pie',
                        'What the hell Dash', 'He bought a phone just for pics of this WAP']})
        toy_dict = {}
        getNon_dict(toy_df, toy_dict, dict_words)
        self.assertEqual(toy_dict['rainbow'], ['awww', 'bbibbi', 'kvsadf'])
