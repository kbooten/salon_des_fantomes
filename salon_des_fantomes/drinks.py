from taste_funcs import *

from psychotropics.utterance_transformers import odd_parenthetical
from psychotropics.utterance_transformers import doubt
from psychotropics.utterance_transformers import expand_into_simple_words
from psychotropics.utterance_transformers import juan
from psychotropics.character_transformers import light_lucience




drinks2psycho = {
    "water":None,
    "port":None,
    "calvados":None,
    "chablis":None,
    "sherry":None,
    "amontillado":None,
    "madeira":None,
    "dry vermouth":None,
    "sweet vermouth":None,
    "scotch":None,
    "brandy":None,
    "1961 Pétrus":{
                    "function":odd_parenthetical,
                    "type":"transform_utterance",
                    "prob":0.9,
                    "step":0.02,
                    'taste_func':tf0,
                    "chem":"bisephontinol-3",
                    },
    "1950 Château Lafleur":{
                    "function":doubt,
                    "type":"transform_utterance",
                    "prob":0.9,
                    "step":0.3,
                    'taste_func':tf1,
                    "chem":"3-hydroxafoam-butane",
                    },

    "1962 La Tâche":{
                    "function":expand_into_simple_words,
                    "type":"transform_utterance",
                    "prob":0.9,
                    "step":0.3,
                    'taste_func':tf2,
                    "chem":"hot-luxatinoid",
                    },

    "1996 Haut-Brion Blanc":{
                    "function":juan,
                    "type":"transform_utterance",
                    "prob":0.9,
                    "step":0.3,
                    'taste_func':tf3,
                    "chem":"hot-luxatinoid",
                    },

    "1997 HCHANGE":{
                    "function":light_lucience,
                    "type":"transform_character",
                    "prob":0.9,
                    "step":0.3,
                    'taste_func':tf4,
                    "chem":"hot-luxatinoid",
                    },
}