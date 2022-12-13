from taste_funcs import *

from psychotropics.utterance_transformers.odd_parenthetical import add_odd_parenthetical
from psychotropics.utterance_transformers.doubt import add_doubt
from psychotropics.character_transformers import light_lucience
from psychotropics.prompts import juan_crystalsmith


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
                    "function":add_odd_parenthetical,
                    "type":"transform_utterance",
                    "prob":0.9,
                    "step":0.02,
                    'taste_func':tf1,
                    "chem":"bisephontinol-3",
                    'after_wordcount':1,#0000,
                    },
    "1950 Château Lafleur":{
                    "function":add_doubt,
                    "type":"transform_utterance",
                    "prob":0.9,
                    "step":0.3,
                    'taste_func':tf2,
                    "chem":"3-hydroxafoam-butane",
                    'after_wordcount':1,#30000,
                    },

    "1962 La Tâche":{
                    "function":light_lucience,
                    "type":"transform_character",
                    "prob":0.9,
                    "step":0.3,
                    'taste_func':tf2,
                    "chem":"hot-luxatinoid",
                    'after_wordcount':1,#30000,
                    },

    "1996 Haut-Brion Blanc":{
                    "function":juan_crystalsmith,
                    "type":"utterance",
                    "prob":0.9,
                    "step":0.3,
                    'taste_func':tf2,
                    "chem":"hot-luxatinoid",
                    'after_wordcount':1,#30000,
                    },

}